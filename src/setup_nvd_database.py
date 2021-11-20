from db_functions import check_db_connection
from db_functions import get_connection
from db_functions import create_database
import mysql.connector
from mysql.connector import errorcode




DB_NAME = "nvd"
TABLE_NAME = "nvd"
TABLES = {}
TABLES['nvd'] = (
    "CREATE TABLE `nvd` ("
    "  `id` varchar(20) NOT NULL,"
    "  `soft` varchar(160) NOT NULL DEFAULT 'undefined'," 
    "  `rng` varchar(100) NOT NULL DEFAULT 'undefined',"
    "  `lose_types` varchar(100) NOT NULL DEFAULT 'undefined',"
    "  `severity` varchar(20) NOT NULL DEFAULT 'undefined',"
    "  `access` varchar(20) NOT NULL DEFAULT 'undefined')")


def setup_nvd_database():
    configure_nvd_database()
    configure_nvd_table()


def configure_nvd_database():
    try:
        check_db_connection()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            print(err)
            exit(1)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {} does not exists.".format(DB_NAME))
            create_database(cursor, DB_NAME)
            print("Database {} created successfully.".format(DB_NAME))
            conn.database = DB_NAME
        else:
            print(err)
            exit(1)


def configure_nvd_table(recreate=False):
    try:
        check_db_connection()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE {}".format(DB_NAME))
        if recreate:
            cursor.execute("DROP TABLE IF EXISTS {}".format(TABLE_NAME))
        nvd_table_description = TABLES['nvd']
        cursor.execute(nvd_table_description)
        cursor.execute("DESCRIBE {}".format(TABLE_NAME))
        print("The defined {} table: ".format(TABLE_NAME))
        for column in cursor:
            print(column)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table '{}' already exists.".format(TABLE_NAME))
        else:
            print(err)
            exit(1)


setup_nvd_database()
