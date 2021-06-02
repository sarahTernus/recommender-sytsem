from src import getTopPredictions
from surprise import KNNWithMeans, Reader, Dataset
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
from surprise import SVD
import pandas as pd
from surprise.model_selection import GridSearchCV
import random


def get_grid_search():
    reader = Reader(rating_scale=(1, 5))
    # df = createReducedDataframes.create_dataframe()
    df = pd.read_csv("../datasets/dataset3.csv")
    data = Dataset.load_from_df(df[['userId', 'postId', 'rating']], reader)

    raw_ratings = data.raw_ratings
    random.shuffle(raw_ratings)

    # A = 90% of the data, B = 10% of the data
    threshold = int(.9 * len(raw_ratings))
    a_raw_ratings = raw_ratings[:threshold]
    b_raw_ratings = raw_ratings[threshold:]

    data.raw_ratings = a_raw_ratings  # data is now the set A

    # Select your best algo with grid search.
    print('Grid Search...')
    param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005]}
    grid_search = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
    grid_search.fit(data)

    algo = grid_search.best_estimator['rmse', 'mae']

    # retrain on the whole set A
    trainset = data.build_full_trainset()
    algo.fit(trainset)

    # Compute biased accuracy on A
    predictions = algo.test(trainset.build_testset())
    print('Biased accuracy on A,', end='   ')
    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    # Compute unbiased accuracy on B
    testset = data.construct_testset(b_raw_ratings)  # testset is now the set B
    predictions = algo.test(testset)
    print('Unbiased accuracy on B,', end=' ')
    accuracy.rmse(predictions)
    accuracy.mae(predictions)