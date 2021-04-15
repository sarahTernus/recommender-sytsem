import sqlite3
from sqlite3 import Error
from faker import Faker
from random import randrange
from random import randint
import random


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
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
    sql = ''' INSERT INTO user(username, latitude, longitude, city)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def create_category(conn, category):
    """
    Create a new project into the projects table
    :param category:
    :param conn:
    :return: user id
    """
    sql = ''' INSERT INTO category(name, cat_description)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, category)
    conn.commit()
    return cur.lastrowid


def create_post(conn, post):
    """
    Create a new project into the projects table
    :param post:
    :param conn:
    :return: user id
    """
    sql = ''' INSERT INTO post(timestamp, title, description, votes, author, category)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, post)
    conn.commit()
    return cur.lastrowid


def create_comment(conn, comment):
    """
    Create a new project into the projects table
    :param comment:
    :param conn:
    :return: user id
    """
    sql = ''' INSERT INTO comment(content, comment_time, commenter, comment_target)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, comment)
    conn.commit()
    return cur.lastrowid


def create_vote(conn, vote):
    """
    Create a new project into the projects table
    :param vote:
    :param conn:
    :return: user id
    """
    sql = ''' INSERT INTO vote(vote_value, vote_time, voter, vote_target)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, vote)
    conn.commit()
    return cur.lastrowid


def main():
    database = "./database/interactionFocus.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        faker = Faker('de_DE')

        # 4 Kategorien erstellt - aus denen anschließend jeweils eine zufällig gewählt wird
        category1 = ('Essen&Trinken', 'abc')
        category2 = ('Einkaufen', 'def')
        category3 = ('Unterhaltung', 'ghi')
        category4 = ('Mobilitaet', 'jkl')
        category5 = ('Sonstiges', 'mno')
        create_category(conn, category1)
        create_category(conn, category2)
        create_category(conn, category3)
        create_category(conn, category4)
        create_category(conn, category5)

        # groessen-variablen um datensatzgroesse zu beeinflussen
        location_cluster = 1
        locations_per_cluster = 100
        # groesste moegliche useranzahl
        user_count = location_cluster*locations_per_cluster
        max_num_votes = 100

        for i in range(location_cluster):
            # faker.local_latlng returns an array with location details like
            # ('34.95303', '-120.43572', 'Santa Maria', 'US', 'America/Los_Angeles')
            lat_long = faker.local_latlng(country_code='DE', coords_only=False)

            # calculates a random float between 0.01 and 0.1 to fake 10 users at a similar location
            for j in range(locations_per_cluster):
                # !creating USERs!
                name = faker.name()
                random_distance_long = randrange(10)/100
                random_distance_lat = randrange(10)/100
                user = (name, float(lat_long[0]) - random_distance_lat, float(lat_long[1]) - random_distance_long,
                        lat_long[2])

                # primary key from user, can be used as foreign key in different tables
                user_id = create_user(conn, user)
                print(user_id)

                # !creating POSTs!
                # generate title, timestamp and description with faker functions
                timestamp = faker.date_this_decade()
                title = faker.word()
                description = faker.paragraph()
                # a random number of votes per post (maximus defined through max_num_votes)
                votes = randrange(max_num_votes)
                # generate a random number which represents the user_id of the user who voted
                # randrage(100) represents 0-99 -> excludes value and starts at 0 if not defined differently
                # randint includes both values
                author = randint(1, user_count)
                # a random number is generated that represents the category ID -> choose category of post
                category = randint(1, 5)
                post = (timestamp, title, description, votes, author, category)
                post_id = create_post(conn, post)

                # !creating VOTES!
                # put users into a LIST and shuffle them so a user can only vote 1 time
                # user_count + 1 because number would be excluded
                choices = list(range(1, user_count + 1))
                random.shuffle(choices)
                # save the voter and vote_target to increase the posts that got voted AND commented on by users
                number_frequency = randint(1, 5)
                # generate votes corresponding to the number of votes set in POSTS
                for k in range(votes):

                    vote_value = randint(0, 1)
                    vote_time = faker.date_this_decade() #sollte neuer als post sein
                    voter = choices.pop()

                    vote_target = post_id
                    person = 0
                    if number_frequency == 1:
                        person = voter
                        print("person-voter=", person)

                    vote = (vote_value, vote_time, voter, vote_target)
                    create_vote(conn, vote)

                    # !!! auffällig ist dass Kategorien bei sql ausgabe ab 1 gezählt werden aber ab 0 reingeschrieben werden

                    # random number of comments per post
                    max_comments = randrange(5)
                    for m in range(max_comments):
                        content = faker.paragraph()
                        comment_time = faker.date_this_decade()  # sollte neuer als post sein

                        if number_frequency != 1:
                            commenter = randrange(1, user_count + 1)
                        else:
                            commenter = person
                            print("commenter" + format(commenter))

                        comment_target = post_id

                        comment = (content, comment_time, commenter, comment_target)
                        create_comment(conn, comment)


if __name__ == '__main__':
    main()
