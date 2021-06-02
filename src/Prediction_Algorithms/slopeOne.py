from surprise import SlopeOne, Reader, Dataset
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
import time
import pandas as pd


def calculate_predictions_slope_one():
    slope_one = SlopeOne()

    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("../datasets/dataset3b.csv")
    data = Dataset.load_from_df(df[['userId', 'postId', 'rating']], reader)

    trainset, testset = train_test_split(data, test_size=0.25, random_state=0)

    start = time.time()

    slope_one.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")
    predictions = slope_one.test(testset)
    accuracy.rmse(predictions)

    results = cross_validate(
        algo=slope_one, data=data, measures=['RMSE'],
        cv=5, return_train_measures=True
    )
    print(results)
    return predictions


if __name__ == '__main__':
    calculated_predictions = calculate_predictions_slope_one()
    """top_n = getTopPredictions.get_top_n(calculated_predictions, 10)
    # print(top_n)
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])"""







