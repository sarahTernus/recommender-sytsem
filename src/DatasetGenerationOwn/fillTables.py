import sqlite3
from sqlite3 import Error
from faker import Faker
from random import randrange
from random import randint
import random


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


def create_user(conn, user):
    """
    Create a new project into the projects table
    :param user
    :param conn: connection to database
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
    :param post
    :param conn: connection to database
    :return: post id
    """
    sql = ''' INSERT INTO post(latitude, longitude)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, post)
    conn.commit()
    return cur.lastrowid


def create_rating(conn, rating):
    """
    Create a new project into the projects table
    :param rating
    :param conn: connection to database
    :return: rating id
    """
    sql = ''' INSERT INTO rating(user_id, post_id, rating_value, rating_timestamp)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, rating)
    conn.commit()
    return cur.lastrowid


def fill_table(conn):
    """
    Fill the database tables
    :param conn: connection to database
    """
    location_cluster = 4
    locations_per_cluster = 250
    # max possible amount of users
    user_count = location_cluster * locations_per_cluster
    post_amount = 100

    faker = Faker('de_DE')

    for i in range(location_cluster):
        # faker.local_latlng returns an array with location details like
        # ('34.95303', '-120.43572', 'Santa Maria', 'US', 'America/Los_Angeles')
        lat_long = faker.local_latlng(country_code='DE', coords_only=True)

        # calculates a random float between 0.01 and 0.1 to fake 10 users at a similar location
        for j in range(locations_per_cluster):
            # !creating USERs!
            random_distance_lat = randrange(10) / 100
            random_distance_long = randrange(10) / 100
            user = (float(lat_long[0]) - random_distance_lat, float(lat_long[1]) - random_distance_long)

            user_id = create_user(conn, user)
            print("user", user_id)

            unique_posts = list(range(1, post_amount*location_cluster + 1))
            random.shuffle(unique_posts)

            interaction_amount = randint(50, 150)
            for m in range(interaction_amount):
                post = unique_posts.pop()
                rating_value = randint(1, 9)
                timestamp = faker.date_this_decade()
                rating = (user_id, post, rating_value, timestamp)
                rating_id = create_rating(conn, rating)
                print("rating", rating_id)

        for k in range(post_amount):
            distance_lat_post = randrange(10) / 100
            distance_long_post = randrange(10) / 100

            post = (float(lat_long[0]) - distance_lat_post, float(lat_long[1]) - distance_long_post)
            post_id = create_post(conn, post)
            print("post", post_id)


def main():
    # create a database connection and fill database
    database = "../database/location.db"
    conn = create_connection(database)
    fill_table(conn)
    conn.close()


if __name__ == '__main__':
    main()
