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
    database = "./database/LLDatabase.db"

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
        location_cluster = 1000
        locations_per_cluster = 10
        # groesste moegliche useranzahl
        user_count = location_cluster*locations_per_cluster
        max_num_votes = 20

        for i in range(location_cluster):
            # faker.local_latlng returns an array with location details like
            # ('34.95303', '-120.43572', 'Santa Maria', 'US', 'America/Los_Angeles')
            lat_long = faker.local_latlng(country_code='DE', coords_only=False)

            # calculates a random float between 0.01 and 0.1 to fake 10 users at a similar location
            for j in range(locations_per_cluster):
                name = faker.name()
                random_distance_long = randrange(10)/100
                random_distance_lat = randrange(10)/100
                user = (name, float(lat_long[0]) - random_distance_lat, float(lat_long[1]) - random_distance_long,
                        lat_long[2])

                # primary key from user, can be used as foreign key in different tables
                user_id = create_user(conn, user)
                print(user_id)

                # titel, zeitpunkt und beschreibung mit entsprechender faker funktion erstellen
                timestamp = faker.date_this_decade()
                title = faker.word()
                description = faker.paragraph()
                # muss entsprechend vielen vote datenbankelemente erzeugen
                votes = randrange(max_num_votes)
                # es wird eine zufällige user_ID zugeodnet entsprechend der User Anzahl
                # randrage(100) geht von 0-99 also als grenzen 1 und 101 festlegen
                author = randrange(1, user_count+1)
                # es wird eine der Kategorie_ID's zufällig gewählt
                category = randrange(1, 6)
                post = (timestamp, title, description, votes, author, category)
                post_id = create_post(conn, post)

                # user in Liste packen und diese vermischen -> user kann post nur 1x voten
                choices = list(range(1, user_count + 1))
                random.shuffle(choices)

                # entsprechende anzahl an votes, wie zuvor fuer post generiert wurden, wird erzeugt
                for k in range(votes):
                    vote_value = randint(0, 1)
                    vote_time = faker.date_this_decade() #sollte neuer als post sein
                    voter = choices.pop()
                    vote_target = post_id

                    vote = (vote_value, vote_time, voter, vote_target)
                    create_vote(conn, vote)

                # !!! auffällig ist dass Kategorien bei sql ausgabe ab 1 gezählt werden aber ab 0 reingeschrieben werden

                # zufaellige Anzahl an Kommentaren pro post
                max_comments = randrange(10)
                for l in range(max_comments):
                    content = faker.paragraph()
                    comment_time = faker.date_this_decade()  # sollte neuer als post sein
                    commenter = randrange(1, user_count+1)
                    comment_target = post_id

                    comment = (content, comment_time, commenter, comment_target)
                    create_comment(conn, comment)


if __name__ == '__main__':
    main()
