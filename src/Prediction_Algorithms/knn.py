from src import getTopPredictions
from surprise import KNNWithMeans, Reader, Dataset, KNNBasic, KNNBaseline
from surprise import BaselineOnly
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
import time
import pandas as pd


def calculate_predictions_knn():
    sim_options = {
        "name": "cosine",
        "user_based": True,  # Compute  similarities between users
    }

    knn_rs = KNNBasic(random_state=0, sim_options=sim_options)

    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("../datasets/dataset-1k.csv")
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)

    trainset, testset = train_test_split(data, test_size=0.25, random_state=0)

    start = time.time()

    knn_rs.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")
    predictions = knn_rs.test(testset)
    accuracy.rmse(predictions)
    accuracy.mae(predictions)

    """results = cross_validate(
        algo=knn_rs, data=data, measures=['RMSE'],
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







