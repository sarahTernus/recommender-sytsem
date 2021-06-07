from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from tabulate import tabulate
from six import iteritems

from surprise import SVD, Reader
import pandas as pd
from surprise import Dataset
from surprise.model_selection import GridSearchCV


"""def get_grid_search():
    reader = Reader(rating_scale=(1, 5))
    # df = createReducedDataframes.create_dataframe()
    df = pd.read_csv("../datasets/dataset-100k-movielens.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

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
    accuracy.mae(predictions)"""

if __name__ == '__main__':
    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("../datasets/dataset-100k-movielens.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    param_grid = {'n_epochs': [5, 10], 'lr_all': [0.002, 0.005],
                  'reg_all': [0.4, 0.6]}
    gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)

    gs.fit(data)

    table = [[] for _ in range(len(gs.cv_results['params']))]
    for i in range(len(gs.cv_results['params'])):
        for key in gs.cv_results.keys():
            table[i].append(gs.cv_results[key][i])

    header = gs.cv_results.keys()
    print(tabulate(table, header, tablefmt="rst"))

    print()

    for key, val in iteritems(gs.cv_results):
        print('{:<20}'.format("'" + key + "':"), end='')
        if isinstance(val[0], float):
            print([float('{:.2f}'.format(f)) for f in val])
        else:
            print(val)


