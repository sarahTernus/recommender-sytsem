import sqlite3
from sqlite3 import Error
from faker import Faker
from random import randrange
from random import randint
import random
import numpy as np
import pandas as pd


def create_df():
    """
    Create the rating dataframe from the rating.csv and adjust to fit our case
    :return: df
    """

    df_movie = pd.read_csv("./dataframes/ratings.csv")
    df_movie = df_movie[(df_movie.rating != 0.5) & (df_movie.rating != 1.5) &
                        (df_movie.rating != 2.5) & (df_movie.rating != 3.5) & (df_movie.rating != 4.5)]
    df = df_movie.rename(columns={'userId': 'user_id', 'movieId': 'post_id'}, inplace=False)
    df.drop('timestamp', inplace=True, axis=1)
    print(df)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    df_size = 10000000
    df = df.head(df_size)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    return df, number_of_rows


if __name__ == '__main__':
    """database = "./database/dataset1.db"
    conn = create_connection(database)"""
    df, df_size = create_df()
    # fill_table(conn)

    """faker = Faker('de_DE')
    cluster_size = 100000
    cluster = df_size / cluster_size

    latitude = []
    longitude = []

    # calculates a random float between 0.01 and 0.1 to fake 10 users at a similar location
    for i in range(int(cluster)):
        lat_long = faker.local_latlng(country_code='DE', coords_only=True)

        for j in range(cluster_size):
            # !creating USERs!
            random_distance_long = randrange(10) / 100
            random_distance_lat = randrange(10) / 100
            latitude.append((float(lat_long[0]) - random_distance_lat))
            longitude.append((float(lat_long[1]) - random_distance_long))

    print(latitude)
    print(longitude)"""



