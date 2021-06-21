from src import calculatePrecisionRecall
from surprise import Reader, Dataset, NormalPredictor
import pandas as pd
from surprise.model_selection import cross_validate
from surprise.model_selection import KFold


if __name__ == '__main__':

    """CONFIGURE AND RUN MODEL BASED ALGORITHMS"""
    # generate Dataset for predictions -> choose path of desired Dataset
    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("./datasets/explicit-dataset-100k-movielens.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    # set parameters
    rand = NormalPredictor()

    """CROSS VALIDATION RMSE & MAE"""
    print("\n\n________________________________________________________________\n")
    print("Cross Validations\n")
    # cross validation for KNNBasic
    resultsBasic = cross_validate(
        algo=rand, data=data, measures=['RMSE', 'MAE'],
        cv=5, return_train_measures=True
    )
    print("\nResults of Random:")
    print(resultsBasic)
    print("\n")

    """PRECISION AND RECALL"""
    kf = KFold(n_splits=5)

    # Precision and Recall for Random
    print("\n\n________________________________________________________________\n")
    print("Precision and Recall for Random\n")
    for trainset, testset in kf.split(data):
        rand.fit(trainset)
        predictions = rand.test(testset)
        precisions, recalls = calculatePrecisionRecall.precision_recall_at_k(predictions, k=10, threshold=3)

        # Precision and recall can then be averaged over all users
        print("----precision----")
        print(sum(prec for prec in precisions.values()) / len(precisions))
        print("----recall----")
        print(sum(rec for rec in recalls.values()) / len(recalls))
        print("\n")






