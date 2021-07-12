from src import calculatePrecisionRecall
from surprise import Reader, Dataset, KNNBasic, KNNWithMeans, KNNWithZScore
import pandas as pd
from surprise.model_selection import cross_validate
from surprise.model_selection import KFold


if __name__ == '__main__':

    """CONFIGURE AND RUN MEMORY BASED ALGORITHMS"""
    # choose similarity measurement and user or item-based
    sim_options = {
        "name": "pearson",
        "user_based": True,  # Compute  similarities between users
    }

    # generate Dataset for predictions -> choose path of desired Dataset
    reader = Reader(rating_scale=(1, 4))
    df = pd.read_csv("datasets/dataset4-100k-movielens.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)
    # data = Dataset.load_builtin(name='ml-10m')

    knnBasic = KNNBasic(random_state=0, sim_options=sim_options, verbose=True)
    knnMeans = KNNWithMeans(random_state=0, sim_options=sim_options, verbose=True)
    knnZScore = KNNWithZScore(random_state=0, sim_options=sim_options, verbose=True)

    """CROSS VALIDATION RMSE & MAE"""
    print("\n\n________________________________________________________________\n")
    print("Cross Validations\n")
    # cross validation for KNNBasic
    resultsBasic = cross_validate(
        algo=knnBasic, data=data, measures=['RMSE', 'MAE'],
        cv=5, return_train_measures=True
    )
    print("\nResults of Basic KNN:")
    print(resultsBasic)
    print("\n")

    # cross validation for KNNWithMeans
    resultsMeans = cross_validate(
        algo=knnMeans, data=data, measures=['RMSE', 'MAE'],
        cv=5, return_train_measures=True
    )
    print("\nResults of KNNWithMeans:")
    print(resultsMeans)
    print("\n")

    # cross validation for KNNWithZScore
    resultsZScore = cross_validate(
        algo=knnZScore, data=data, measures=['RMSE', 'MAE'],
        cv=5, return_train_measures=True
    )
    print("\nResults of KNNWithZScore:")
    print(resultsZScore)
    print("\n")

    """PRECISION AND RECALL"""
    kf = KFold(n_splits=5)

    # Precision and Recall for KNNBasic
    print("\n\n________________________________________________________________\n")
    print("Precision and Recall for KNNBasic\n")
    for trainset, testset in kf.split(data):
        knnBasic.fit(trainset)
        predictions = knnBasic.test(testset)
        precisions, recalls = calculatePrecisionRecall.precision_recall_at_k(predictions, k=10, threshold=3)

        # Precision and recall can then be averaged over all users
        print("----precision----")
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print("----recall----")
        print(sum(rec for rec in recalls.values()) / len(recalls))
        print("\n")

    # Precision and Recall for KNNWithMeans
    print("\n\nPrecision and Recall for KNNWithMeans\n")
    for trainset, testset in kf.split(data):
        knnMeans.fit(trainset)
        predictions = knnMeans.test(testset)
        precisions, recalls = calculatePrecisionRecall.precision_recall_at_k(predictions, k=10, threshold=3)

        # Precision and recall can then be averaged over all users
        print("----precision----")
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print("----recall----")
        print(sum(rec for rec in recalls.values()) / len(recalls))
        print("\n")

    # Precision and Recall for KNNWithZScore
    print("\n\nPrecision and Recall for KNNWithZScore\n")
    for trainset, testset in kf.split(data):
        knnZScore.fit(trainset)
        predictions = knnZScore.test(testset)
        precisions, recalls = calculatePrecisionRecall.precision_recall_at_k(predictions, k=10, threshold=3)

        # Precision and recall can then be averaged over all users
        print("----precision----")
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print("----recall----")
        print(sum(rec for rec in recalls.values()) / len(recalls))
        print("\n")





