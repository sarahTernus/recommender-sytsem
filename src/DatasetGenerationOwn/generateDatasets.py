import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np


def create_connection(db_file):
    """
    create a database connection to the SQLite database specified by db_file
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


def create_dataset(connection):
    """
    create a pandas dataframe from the db and generate csv file from it
    :param connection: database connection
    :return: pandas dataframe
    """

    # create dataframe from database (with ratings 1-9)
    df = pd.read_sql_query("SELECT user_id, post_id, rating_value FROM rating", connection)
    df.drop_duplicates()
    print(df)

    # change voting-values to get a Gaussian distribution
    df["rating_value"].replace({6: 2}, inplace=True)
    df["rating_value"].replace({7: 3}, inplace=True)
    df["rating_value"].replace({8: 3}, inplace=True)
    df["rating_value"].replace({9: 4}, inplace=True)

    # df = df.head(100000)
    df.to_csv("../datasets/location/dataset-location.csv")

    return df


if __name__ == '__main__':
    # create a database connection
    database = "../database/location.db"
    db_connection = create_connection(database)

    dataframe = create_dataset(db_connection)
    db_connection.close()
