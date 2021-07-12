from src.PredictionAlgorithms import getTopPredictions
from surprise import KNNWithMeans, Reader, Dataset, KNNBasic, KNNWithZScore
from surprise import accuracy
import time
import pandas as pd


# To actually recommend not rated Items
# (full rating data ist trainset, all other pairs are testset to recommend)
def calculate_predictions_knn(dataset, similarity):
    """
    calculate the predictions with KNNBasic
        :param dataset: from csv file created dataset
        :param similarity: similarity dictionary
        :return: predictions
    """
    trainset = dataset.build_full_trainset()
    knn = KNNBasic(random_state=0, sim_options=similarity)

    start = time.time()
    knn.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = knn.test(testset)

    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    return predictions


def calculate_predictions_knn_means(dataset, similarity):
    """
    calculate the predictions with KNNWithMeans (mean-centered knn)
        :param dataset: from csv file created dataset
        :param similarity: similarity dictionary
        :return: predictions
    """

    trainset = dataset.build_full_trainset()
    knn_m = KNNWithMeans(random_state=0, sim_options=similarity)

    start = time.time()
    knn_m.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = knn_m.test(testset)

    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    return predictions


def calculate_predictions_knn_zscore(dataset, similarity):
    """
    calculate the predictions with KNNWithZScore
        :param dataset: from csv file created dataset
        :param similarity: similarity dictionary
        :return: predictions
    """

    trainset = dataset.build_full_trainset()
    knn_z = KNNWithZScore(random_state=0, sim_options=similarity)

    start = time.time()
    knn_z.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = knn_z.test(testset)

    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    return predictions


if __name__ == '__main__':

    # choose similarity measurement (name) and user or item-based (user_based)
    sim_options = {
        "name": "cosine",
        "user_based": True,
    }

    # generate Dataset for predictions -> choose path of desired Dataset
    # if location should be included run sortByLocation.py first and use dedicated csv (.dataset/location)
    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("../datasets/location/dataset-location-reduced.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    # choose which predictions from which algorithm should be displayed
    # from calculate_predictions_knn_means or calculate_predictions_knn_means or calculate_predictions_knn_zscore
    calculated_predictions = calculate_predictions_knn(data, sim_options)
    # how many predictions are to be displayed per person
    top_n = getTopPredictions.get_top_n(calculated_predictions, 10)
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])







