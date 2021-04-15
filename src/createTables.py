import sqlite3
from sqlite3 import Error


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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object"./database/10.000.db"
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "./database/interactionFocus.db"

    sql_create_user_table = """CREATE TABLE IF NOT EXISTS user (
                                        user_id integer PRIMARY KEY AUTOINCREMENT,
                                        username text NOT NULL,
                                        latitude real,
                                        longitude real,
                                        city text
                                    ); """

    sql_create_category_table = """CREATE TABLE IF NOT EXISTS category (
                                    category_id integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    cat_description text 
                                );"""

    sql_create_post_table = """CREATE TABLE IF NOT EXISTS post (
                                    post_id integer PRIMARY KEY AUTOINCREMENT,
                                    timestamp text NOT NULL,
                                    title text,
                                    description text,
                                    votes int NOT NULL,
                                    author integer NOT NULL,
                                    category integer NOT NULL,
                                    FOREIGN KEY(author) REFERENCES user(user_id),
                                    FOREIGN KEY(category) REFERENCES category(category_id)
                                );"""

    sql_create_comment_table = """CREATE TABLE IF NOT EXISTS comment (
                                    comment_id integer PRIMARY KEY AUTOINCREMENT,
                                    content text NOT NULL,
                                    comment_time text NOT NULL,
                                    commenter integer NOT NULL,
                                    comment_target integer NOT NULL,
                                    FOREIGN KEY(commenter) REFERENCES user(user_id),
                                    FOREIGN KEY(comment_target) REFERENCES post(post_id)
                                );"""

    sql_create_vote_table = """CREATE TABLE IF NOT EXISTS vote (
                                    vote_id integer PRIMARY KEY AUTOINCREMENT,
                                    vote_value integer NOT NULL,
                                    vote_time text NOT NULL,
                                    voter integer NOT NULL,
                                    vote_target integer NOT NULL,
                                    FOREIGN KEY(voter) REFERENCES user(user_id),
                                    FOREIGN KEY(vote_target) REFERENCES post(post_id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_post_table)
        create_table(conn, sql_create_category_table)
        create_table(conn, sql_create_comment_table)
        create_table(conn, sql_create_vote_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
