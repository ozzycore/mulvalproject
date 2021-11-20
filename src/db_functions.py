import mysql.connector
from mysql.connector import errorcode
from configparser import ConfigParser



def create_database(cursor, db_name):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def read_db_config(config_filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(config_filename)
    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception('{} not found in the {}'.format(section, config_filename))

    return db_config


def get_connection():
    try:
        db_config = read_db_config()
        conn = mysql.connector.connect(
            host = db_config['host'],
            user = db_config['user'],
            password = db_config['password']
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            print(err)
            exit(1)
        else:
            print(err)
            exit(1)

    return conn


def check_db_connection(verbose=False):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        if verbose:
            for database in cursor:
                print(database)
        print("Successful database connection..")
    except mysql.connector.Error as err:
        print(err)
        exit(1)

