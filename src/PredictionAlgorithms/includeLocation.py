from collections import defaultdict
import pandas as pd
import sqlite3
from sqlite3 import Error
import numpy as np
import math


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


def calculate_distance(lat_u, long_u, lat_p, long_p):
    """
    Calculated the distance of user and post though their latitudes and longitudes
    :param lat_u: latitude of the user
    :param long_u: longitude of the user
    :param lat_p: latitude of the post
    :param long_p: longitude of the post
    :return: distance of user and post
    """
    R = 6373.0

    lat1 = math.radians(lat_u)
    lon1 = math.radians(long_u)

    lat2 = math.radians(lat_p)
    lon2 = math.radians(long_p)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    # print(distance)
    return distance


def sort_out_by_location(connection):
    """
    Creates a CVS where recommendations that are too far away are excluded
    :param connection: database connection to get user and post coordinates
    """

    df = pd.read_csv("../datasets/location/dataset-location.csv", index_col=0)
    # df = pd.read_sql_query("SELECT user_id, post_id FROM rating", connection)

    df_user = pd.read_sql_query("SELECT user_id, latitude, longitude FROM user", connection)
    df_user = df_user.rename(columns={"latitude": "latitude_user", "longitude": "longitude_user"})
    print(df_user)

    df_post = pd.read_sql_query("SELECT post_id, latitude, longitude FROM post", connection)
    df_post = df_post.rename(columns={"latitude": "latitude_post", "longitude": "longitude_post"})
    print(df_post)

    df = df.join(df_user.set_index('user_id'), on='user_id')
    df = df.join(df_post.set_index('post_id'), on='post_id')

    print(df)

    allowed_distance = 400.0
    for index, row in df.iterrows():
        x = index
        # print(x)
        lat_u = row['latitude_user']
        long_u = row['longitude_user']
        lat_p = row['latitude_post']
        long_p = row['longitude_post']
        distance = calculate_distance(lat_u, long_u, lat_p, long_p)

        if distance > allowed_distance:
            df = df.drop(labels=x, axis=0)

    df = df.reset_index(drop=True)
    print(df)
    df.to_csv("../datasets/location/dataset-location-reduced.csv")


def main():
    # create a database connection and fill database
    database = "../database/location.db"
    conn = create_connection(database)
    sort_out_by_location(conn)


if __name__ == '__main__':
    # df_rating_reduced = main()
    main()