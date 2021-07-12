from src.PredictionAlgorithms import getTopPredictions
from surprise import Reader, Dataset, SVD, NMF, SVDpp
from surprise import accuracy
import time
import pandas as pd


# To actually recommend not rated Items
# (full rating data ist trainset, all other pairs are testset to recommend)
def calculate_predictions_svd(dataset, amount_factors, amount_epochs):
    """
    calculate the predictions SVD
        :param dataset: from csv file created dataset
        :param amount_factors: factors
        :param amount_epochs: epochs
        :return: predictions
    """
    trainset = dataset.build_full_trainset()
    svd = SVD(random_state=0, n_factors=amount_factors, n_epochs=amount_epochs, verbose=True)

    start = time.time()
    svd.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = svd.test(testset)

    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    return predictions


def calculate_predictions_svdpp(dataset, amount_factors, amount_epochs):
    """
    calculate the predictions SVD++
        :param dataset: from csv file created dataset
        :param amount_factors: factors
        :param amount_epochs: epochs
        :return: predictions
    """

    trainset = dataset.build_full_trainset()
    svdpp = SVDpp(random_state=0, n_factors=amount_factors, n_epochs=amount_epochs, verbose=True)

    start = time.time()
    svdpp.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = svdpp.test(testset)

    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    return predictions


def calculate_predictions_nmf(dataset, amount_factors, amount_epochs):
    """
    calculate the predictions NMF
        :param dataset: from csv file created dataset
        :param amount_factors: factors
        :param amount_epochs: epochs
        :return: predictions
    """

    trainset = dataset.build_full_trainset()
    nmf = NMF(random_state=0, n_factors=amount_factors, n_epochs=amount_epochs, verbose=True)

    start = time.time()
    nmf.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = nmf.test(testset)

    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    return predictions


if __name__ == '__main__':

    # set parameters
    factors = 200
    epochs = 30

    # generate Dataset for predictions -> choose path of desired Dataset
    # if location should be included run sortByLocation.py first and use dedicated csv (.dataset/location)
    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("../datasets/location/dataset-location-reduced.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    # choose which predictions from which algorithm should be displayed
    # from calculate_predictions_svd or from calculate_predictions_nmf
    calculated_predictions = calculate_predictions_svd(data, factors, epochs)
    # how many predictions are to be displayed per person
    top_n = getTopPredictions.get_top_n(calculated_predictions, 10)
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])









