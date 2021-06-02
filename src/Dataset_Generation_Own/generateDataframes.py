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
    database = "../database/dataset-10k-dense.db"

    # create a database connection
    conn = create_connection(database)
    # create dataframe from database (with ratings 1-9)
    df = pd.read_sql_query("SELECT user_id, post_id, rating_value FROM rating", conn)
    df.drop_duplicates()
    print(df)

    conn.close()
    # change voting-values to get a Gaussian distribution
    df["rating_value"].replace({6: 2}, inplace=True)
    df["rating_value"].replace({7: 3}, inplace=True)
    df["rating_value"].replace({8: 3}, inplace=True)
    df["rating_value"].replace({9: 4}, inplace=True)

    # df = df.head(100000)
    df.to_csv("../datasets/dataset-10k.csv")

    return df


if __name__ == '__main__':
    dataset = create_dataframe()
