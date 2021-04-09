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


def main():
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
    # print(df_vote_merge)
    df_vote_merge.insert(7, "commented", 0)
    # print(df_vote_merge)

    for index, row in df_comment.iterrows():
        post_id = row["comment_target"]
        user_id = row["commenter"]
        print(user_id, post_id)
        df_vote_merge["commented"] = np.where((df_vote_merge.post_id == post_id) & (df_vote_merge.user_id == user_id), 1, df_vote_merge.commented)
    print(df_vote_merge.to_string())

    # data2_count = df_vote_merge.groupby(['vote_id', 'ItemId']).agg({'Timestamp': 'count'}).reset_index()
    # data2_count.columns = ['UserId', 'ItemId', 'Affinity']
    conn.close()


if __name__ == '__main__':
    main()
