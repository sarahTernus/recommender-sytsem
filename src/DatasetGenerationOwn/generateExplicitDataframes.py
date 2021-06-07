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
    df = pd.read_csv("../datasets/dataset-100k-dense.csv", index_col=0)
    df = df[df.rating_value != 3]
    df = df.reset_index()
    df = df.drop(columns=['index'])

    df["rating_value"].replace({4.0: 3}, inplace=True)
    df["rating_value"].replace({5.0: 4}, inplace=True)

    df.to_csv("../datasets/explicit-dataset-100k-dense.csv")

    return df


if __name__ == '__main__':
    dataset = create_dataframe()
