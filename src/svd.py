from src import createDataframes
from src import getTopPredictions
from src import createReducedDataframes
from surprise import KNNWithMeans, Reader, Dataset
from surprise import BaselineOnly
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
from surprise import SVD
import time


def calculate_predictions_svd():
    reader = Reader(rating_scale=(1, 4))
    df = createReducedDataframes.create_dataframe()
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating_value']], reader)
    trainset, testset = train_test_split(data, test_size=0.25)

    svd_model = SVD()
    svd_model.fit(trainset)
    predictions = svd_model.test(testset)

    accuracy.rmse(predictions)

    predict1 = svd_model.predict(uid=1445, iid=1, r_ui=1)
    print(predict1)
    predict2 = svd_model.predict(uid=3819, iid=1, r_ui=2)
    print(predict2)
    predict3 = svd_model.predict(uid=4110, iid=1, r_ui=3)
    print(predict3)
    predict4 = svd_model.predict(uid=4579, iid=100, r_ui=4)
    print(predict4)

    return predictions


if __name__ == '__main__':
    calculated_predictions = calculate_predictions_svd()
    top_n = getTopPredictions.get_top_n(calculated_predictions, 10)
    # print(top_n)
    """for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])"""
