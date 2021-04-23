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
    database = "./database/fakeData.db"

    sql_create_user_table = """CREATE TABLE IF NOT EXISTS user (
                                        user_id integer PRIMARY KEY AUTOINCREMENT,
                                        latitude real,
                                        longitude real
                                    );"""

    sql_create_post_table = """CREATE TABLE IF NOT EXISTS post (
                                    post_id integer PRIMARY KEY AUTOINCREMENT,
                                    title text,
                                    description text                                    
                                );"""

    sql_create_rating_table = """CREATE TABLE IF NOT EXISTS rating (
                                    user_id integer NOT NULL,
                                    post_id integer NOT NULL,
                                    rating_value integer NOT NULL,
                                    rating_timestamp text NOT NULL,
                                    FOREIGN KEY(user_id) REFERENCES user(user_id),
                                    FOREIGN KEY(post_id) REFERENCES post(post_id),
                                    PRIMARY KEY (user_id, post_id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_post_table)
        create_table(conn, sql_create_rating_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    # df_rating_reduced = main()
    main()