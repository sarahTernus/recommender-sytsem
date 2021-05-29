from src import createDataframes
# from src import getTopPredictions
from src import createReducedDataframes
from surprise import KNNWithMeans, Reader, Dataset
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
from surprise import SVD
import time
from collections import defaultdict
import pandas as pd
from surprise.model_selection import GridSearchCV
import random


def calculate_predictions_svd():
    reader = Reader(rating_scale=(1, 4))
    # df = createReducedDataframes.create_dataframe()
    df = pd.read_pickle("./dataframes/df_reduced_rating.pkl")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    # data = Dataset.load_builtin('ml-100k')

    """raw_ratings = data.raw_ratings
    random.shuffle(raw_ratings)

    # A = 90% of the data, B = 10% of the data
    threshold = int(.9 * len(raw_ratings))
    A_raw_ratings = raw_ratings[:threshold]
    B_raw_ratings = raw_ratings[threshold:]

    data.raw_ratings = A_raw_ratings  # data is now the set A

    # Select your best algo with grid search.
    print('Grid Search...')
    param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005]}
    grid_search = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3)
    grid_search.fit(data)

    algo = grid_search.best_estimator['rmse']

    # retrain on the whole set A
    trainset = data.build_full_trainset()
    algo.fit(trainset)

    # Compute biased accuracy on A
    predictions = algo.test(trainset.build_testset())
    print('Biased accuracy on A,', end='   ')
    accuracy.rmse(predictions)

    # Compute unbiased accuracy on B
    testset = data.construct_testset(B_raw_ratings)  # testset is now the set B
    predictions = algo.test(testset)
    print('Unbiased accuracy on B,', end=' ')
    accuracy.rmse(predictions)"""

    trainset, testset = train_test_split(data, test_size=0.25, random_state=0)

    svd_model = SVD(random_state=0, n_factors=200, n_epochs=30, verbose=True)
    svd_model.fit(trainset)
    predictions = svd_model.test(testset)

    predict1 = svd_model.predict(uid=1445, iid=1, r_ui=1)
    print(predict1)
    predict2 = svd_model.predict(uid=3819, iid=1, r_ui=2)
    print(predict2)
    predict3 = svd_model.predict(uid=4110, iid=1, r_ui=3)
    print(predict3)
    predict4 = svd_model.predict(uid=4579, iid=100, r_ui=4)
    print(predict4)

    """trainset = data.build_full_trainset()
    svd_model = SVD(random_state=0, n_factors=200, n_epochs=30, verbose=True)

    start = time.time()
    svd_model.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predictions = svd_model.test(testset)

    predict1 = svd_model.predict(uid=1445, iid=1, r_ui=1)
    print(predict1)
    predict2 = svd_model.predict(uid=3819, iid=1, r_ui=2)
    print(predict2)
    predict3 = svd_model.predict(uid=4110, iid=1, r_ui=3)
    print(predict3)
    predict4 = svd_model.predict(uid=4579, iid=100, r_ui=4)
    print(predict4)"""

    accuracy.rmse(predictions)
    accuracy.mse(predictions)
    accuracy.mae(predictions)

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
    top_n = get_top_n(calculated_predictions, 10)
    # print(top_n)
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])
