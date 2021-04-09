from src import createDataframes
from surprise import KNNWithMeans, Reader, Dataset
from surprise import BaselineOnly
from surprise.model_selection import cross_validate

# To use item-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": True,  # Compute  similarities between users
}
algo = KNNWithMeans(sim_options=sim_options)

# reader = Reader(line_format='vote_id vote_value vote_time user_id post_id latitude longitude commented', sep='\t')

df = createDataframes.create_dataframe()
dataset = Dataset.load_from_df(df[['vote_id', 'vote_value', 'vote_time', 'user_id', 'post_id', 'latitude', 'longitude',
                         'commented']])

# print(trainingSet)

algo.fit(dataset)
