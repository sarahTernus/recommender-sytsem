import sqlite3
from sqlite3 import Error
from faker import Faker
from random import randrange
from random import randint
import random
import pandas as pd


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_user(conn, user):
    """
    Create a new project into the projects table
    :param user:
    :param conn:
    :return: user id
    """
    sql = ''' INSERT INTO user(latitude, longitude)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def create_post(conn, post):
    """
    Create a new project into the projects table
    :param post:
    :param conn:
    :return: user id
    """
    sql = ''' INSERT INTO post(title, description)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, post)
    conn.commit()
    return cur.lastrowid


def create_rating(conn, rating):
    """
    Create a new project into the projects table
    :param rating:
    :param conn:
    :return: user id
    """
    sql = ''' INSERT INTO rating(user_id, post_id, rating_value, rating_timestamp)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, rating)
    conn.commit()
    return cur.lastrowid


def create_df():
    """
    Create the rating dataframe from the rating.csv and adjust to fit our case
    :return: df
    """

    df_movie = pd.read_csv("./dataframes/ratings.csv")
    df_movie = df_movie[(df_movie.rating != 0.5) & (df_movie.rating != 1.5) &
                        (df_movie.rating != 2.5) & (df_movie.rating != 3.5) & (df_movie.rating != 4.5)]
    df = df_movie.rename(columns={'movieId': 'postId'}, inplace=False)
    df.drop('timestamp', inplace=True, axis=1)
    print(df)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    df = df.head(100000)

    index = df.index
    number_of_rows = len(index)
    print(number_of_rows)

    return df, number_of_rows


def fill_table(conn):
    ratings, df_size = create_df();

    faker = Faker('de_DE')
    posts_per_location = 1000000
    locations = df_size / posts_per_location

    # calculates a random float between 0.01 and 0.1 to fake 10 users at a similar location
    for i in range(locations):
        lat_long = faker.local_latlng(country_code='DE', coords_only=True)

        for j in range(posts_per_location):
            # !creating USERs!
            random_distance_long = randrange(10) / 100
            random_distance_lat = randrange(10) / 100
            user = (float(lat_long[0]) - random_distance_lat, float(lat_long[1]) - random_distance_long)

            user_id = create_user(conn, user)
            print("user", user_id)

    # sollte aus movielens dataset gelesen werden
    post_amount = 10
    user_count = 10

    for k in range(post_amount):
        post_title = faker.word()
        description = faker.paragraph()

        post = (post_title, description)
        post_id = create_post(conn, post)
        print("post", post_id)

        unique_users = list(range(1, user_count + 1))
        random.shuffle(unique_users)
        # to have a varying number of interactions per post but not to little
        # interaction_amount = randint(30, max_interactions_per_post)
        interaction_amount = user_count
        for m in range(interaction_amount):
            user = unique_users.pop()
            rating_value = randint(1, 4)
            timestamp = faker.date_this_decade()
            rating = (user, post_id, rating_value, timestamp)
            rating_id = create_rating(conn, rating)
            print("rating", rating_id)


if __name__ == '__main__':
    """database = "./database/dataset1.db"
    conn = create_connection(database)"""
    create_df()
    # fill_table(conn)
