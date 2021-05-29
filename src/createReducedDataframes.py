import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np


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


def create_dataframe():
    database = "./database/fakeData.db"

    # create a database connection
    conn = create_connection(database)
    # create multiple dataframes with necessary information and merge them
    df_full = pd.read_sql_query("SELECT user_id, post_id, rating_value, rating_timestamp FROM rating", conn)
    df_position = pd.read_sql_query("SELECT user_id, latitude, longitude FROM user", conn)
    df_full = pd.merge(df_full, df_position, on=["user_id"])
    df_full.drop_duplicates()
    print(df_full)

    df_rating = pd.read_sql_query("SELECT user_id, post_id, rating_value FROM rating", conn)
    print(df_rating)

    conn.close()

    # df_rating.to_pickle("./dataframes/df_reduced_rating_500k.pkl")
    df_rating.to_csv("./dataframes/df_reduced_rating.csv")

    return df_rating


if __name__ == '__main__':
    df = create_dataframe()
