from src import createDataframes
from surprise import KNNWithMeans, Reader, Dataset
from surprise import BaselineOnly
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
from surprise import SVD
import time


def calculate_predictions_svd():
    reader = Reader(rating_scale=(1, 4))
    df = createDataframes.rating_reduced()
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.25)

    svd_model = SVD()
    svd_model.fit(trainset)
    predictions = svd_model.test(testset)

    accuracy.rmse(predictions)

    predict1 = svd_model.predict(uid=27, iid=1)
    print(predict1)
    predict2 = svd_model.predict(uid=27, iid=11)
    print(predict2)
    predict3 = svd_model.predict(uid=27, iid=35)
    print(predict3)


if __name__ == '__main__':
    calculate_predictions_svd()
    top_n = getTopPredictions.get_top_n(calculated_predictions, 10)
    print(top_n)
