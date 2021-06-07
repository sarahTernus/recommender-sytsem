from src import PrecisionRecall
from surprise import Reader, Dataset, SVD, SVDpp, NMF
import pandas as pd
from surprise.model_selection import cross_validate
from surprise.model_selection import KFold


if __name__ == '__main__':

    """CONFIGURE AND RUN MODEL BASED ALGORITHMS"""
    # generate Dataset for predictions -> choose path of desired Dataset
    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("./datasets/dataset-1k.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    # set parameters
    factors = 200
    epochs = 30

    svd = SVD(n_factors=factors, n_epochs=epochs, verbose=False)
    nmf = NMF(n_factors=factors, n_epochs=epochs, verbose=False)

    """CROSS VALIDATION RMSE & MAE"""
    print("\n\n________________________________________________________________\n")
    print("Cross Validations\n")
    # cross validation for KNNBasic
    resultsBasic = cross_validate(
        algo=svd, data=data, measures=['RMSE', 'MAE'],
        cv=5, return_train_measures=True
    )
    print("\nResults of SVD:")
    print(resultsBasic)
    print("\n")

    # cross validation for KNNWithMeans
    resultsMeans = cross_validate(
        algo=nmf, data=data, measures=['RMSE', 'MAE'],
        cv=5, return_train_measures=True
    )
    print("\nResults of NMF:")
    print(resultsMeans)
    print("\n")

    """PRECISION AND RECALL"""
    kf = KFold(n_splits=5)

    # Precision and Recall for SVD
    print("\n\n________________________________________________________________\n")
    print("Precision and Recall for SVD\n")
    for trainset, testset in kf.split(data):
        svd.fit(trainset)
        predictions = svd.test(testset)
        precisions, recalls = PrecisionRecall.precision_recall_at_k(predictions, k=10, threshold=3)

        # Precision and recall can then be averaged over all users
        print("----precision----")
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print("----recall----")
        print(sum(rec for rec in recalls.values()) / len(recalls))
        print("\n")

    # Precision and Recall for NMF
    print("\n\nPrecision and Recall for NMF\n")
    for trainset, testset in kf.split(data):
        nmf.fit(trainset)
        predictions = nmf.test(testset)
        precisions, recalls = PrecisionRecall.precision_recall_at_k(predictions, k=10, threshold=3)

        # Precision and recall can then be averaged over all users
        print("----precision----")
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print("----recall----")
        print(sum(rec for rec in recalls.values()) / len(recalls))
        print("\n")




