from src import createDataframes
from src import getTopPredictions
from src import createReducedDataframes
from surprise import KNNWithMeans, Reader, Dataset, KNNBasic, KNNBaseline
from surprise import BaselineOnly
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
import time


def calculate_predictions_knn():
    sim_options = {
        "name": "pearson_baseline",
        "user_based": True,  # Compute  similarities between users
    }

    algo = KNNBaseline(random_state=0, sim_options=sim_options)

    reader = Reader(rating_scale=(1, 4))
    df = createReducedDataframes.create_dataframe()
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    trainset, testset = train_test_split(data, test_size=0.25)

    start = time.time()

    algo.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")
    predictions = algo.test(testset)
    accuracy.rmse(predictions)

    """for x in testset:
        print(x)
    # print(testset)
    print("_________________________________________________________________")
    print(predictions)

    print("_________________________________________________________________")
    with open('predictions_knn.txt', 'w') as f:
        for item in predictions:
            f.write(str(item))
    f.close()"""

    # predict() function:
    # uid – (Raw) id of the user
    # iid – (Raw) id of the item
    # r_ui (float) – The true rating rui. Optional, default is None.
    # clip (bool) – Whether to clip the estimation into the rating scale. For example,
    # if r^ui is 5.5 while the rating scale is [1,5], then r^ui is set to 5. Same goes if r^ui<1. Default is True.
    # verbose (bool) – Whether to print details of the prediction. Default is False.
    # neighbours = algo.get_neighbors(1445, 1)
    # print("neighbours:", neighbours)

    algo.predict(1445, 1, r_ui=1, verbose=True)
    algo.predict(3819, 1, r_ui=2, verbose=True)
    algo.predict(4110, 1, r_ui=3, verbose=True)
    algo.predict(4579, 100, r_ui=4, verbose=True)

    """results = cross_validate(
        algo=algo, data=data, measures=['RMSE'],
        cv=5, return_train_measures=True
    )
    print(results)"""
    return predictions


if __name__ == '__main__':
    calculated_predictions = calculate_predictions_knn()
    """top_n = getTopPredictions.get_top_n(calculated_predictions, 10)
    # print(top_n)
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])"""







