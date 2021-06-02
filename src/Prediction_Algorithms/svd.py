from src import getTopPredictions
from surprise import KNNWithMeans, Reader, Dataset
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
from surprise import SVD, SVDpp, NMF
import time
from collections import defaultdict
import pandas as pd
from surprise.model_selection import GridSearchCV
import random


def calculate_predictions_svd():
    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("../datasets/dataset-100k.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    trainset, testset = train_test_split(data, test_size=0.25, random_state=0)

    # svd_model = SVD(random_state=0, n_factors=200, n_epochs=30, verbose=True)
    # svd_model = SVDpp(random_state=0, n_factors=200, n_epochs=30, verbose=True)
    svd_model = NMF(random_state=0, n_factors=200, n_epochs=30, verbose=True)
    svd_model.fit(trainset)
    predictions = svd_model.test(testset)

    start = time.time()
    svd_model.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    accuracy.rmse(predictions)
    accuracy.mse(predictions)
    accuracy.mae(predictions)

    results = cross_validate(
        algo=svd_model, data=data, measures=['RMSE', 'MAE'],
        cv=5, return_train_measures=True
    )
    print(results)

    return predictions


def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


if __name__ == '__main__':
    calculated_predictions = calculate_predictions_svd()
    recommendations = get_top_n(calculated_predictions, 10)
    # print(top_n)
    for uid, user_ratings in recommendations.items():
        print(uid, [iid for (iid, _) in user_ratings])
