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
    database = "./database/LLDatabase.db"

    # create a database connection
    conn = create_connection(database)
    # create multiple dataframes with necessary information and merge them
    df_vote = pd.read_sql_query("SELECT vote_id, vote_value, vote_time, voter, vote_target FROM vote", conn)
    df_vote = df_vote.rename(columns={'voter': 'user_id', 'vote_target': 'post_id'})
    # print(df_vote)

    df_voter_position = pd.read_sql_query("SELECT user_id, latitude, longitude FROM user, vote WHERE user_id = voter",
                                          conn)
    # print(df_voter_position)

    # create comment
    df_comment = pd.read_sql_query("SELECT commenter, comment_target FROM comment, vote "
                                   "WHERE comment_target = vote_target AND commenter = voter", conn)
    # df_comment = df_vote.rename(columns={'comment_target': 'post_id', 'commenter': 'user_id'})
    # print(df_comment)

    df_vote_merge = pd.merge(df_vote, df_voter_position, on=["user_id"])
    df_vote_merge = df_vote_merge.drop_duplicates()
    df_vote_merge.insert(7, "commented", 0)

    # df_comment.reset_index()
    for index, row in df_comment.iterrows():
        post_id = row["comment_target"]
        user_id = row["commenter"]
        # print(user_id, post_id)
        df_vote_merge["commented"] = np.where((df_vote_merge.post_id == post_id) & (df_vote_merge.user_id == user_id), 1, df_vote_merge.commented)
    df_vote_merge = df_vote_merge.reset_index(drop=True)
    # print(df_vote_merge.to_string())

    df_reduced = df_vote_merge
    df_reduced.drop('longitude', inplace=True, axis=1)
    df_reduced.drop('latitude', inplace=True, axis=1)
    df_reduced.drop('vote_time', inplace=True, axis=1)
    # print(df_reduced.to_string())

    conn.close()
    return df_vote_merge, df_reduced


def rating_reduced():
    df, df_reduced = create_dataframe()
    df_reduced.insert(5, "rating", 0)

    for index, row in df_reduced.iterrows():
        vote_value = row["vote_value"]
        commented = row["commented"]
        if vote_value == 0 and commented == 1:
            row["rating"] = 1
        if vote_value == 0 and commented == 0:
            row["rating"] = 2
        if vote_value == 1 and commented == 0:
            row["rating"] = 3
        if vote_value == 1 and commented == 1:
            row["rating"] = 4
    # print(df_reduced.to_string())
    df_reduced.drop('vote_value', inplace=True, axis=1)
    df_reduced.drop('commented', inplace=True, axis=1)
    df_reduced.drop('vote_id', inplace=True, axis=1)
    # print(df_reduced)

    return df_reduced


if __name__ == '__main__':
    df_rating_reduced = rating_reduced()
