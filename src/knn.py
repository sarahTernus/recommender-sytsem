from src import createDataframes
from surprise import KNNWithMeans, Reader, Dataset
from surprise import BaselineOnly
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
import time


def main():
    # To use item-based cosine similarity
    sim_options = {
        "name": "cosine",
        "user_based": True,  # Compute  similarities between users
    }

    algo = KNNWithMeans(sim_options=sim_options)

    reader = Reader(rating_scale=(1, 4))
    df = createDataframes.rating_reduced()
    data = Dataset.load_from_df(df[['user_id', 'post_id', 'rating']], reader)

    trainset, testset = train_test_split(data, test_size=0.25)

    start = time.time()

    algo.fit(trainset)
    print("-- The script took: ", time.time() - start, " seconds --")

    predictions = algo.test(testset)

    accuracy.rmse(predictions)

    pred = algo.predict(7609, 9886, r_ui=4, verbose=True)

    results = cross_validate(
        algo=algo, data=data, measures=['RMSE'],
        cv=5, return_train_measures=True
    )
    print(results)


if __name__ == '__main__':
    main()




