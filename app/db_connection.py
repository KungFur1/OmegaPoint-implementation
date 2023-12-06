import mysql.connector
from mysql.connector import Error
from decouple import config

_host_name = config("db_host_name", default="localhost")
_user_name = config("db_user_name", default="root")
_user_password = config("db_user_password", default="")
_db_name = config("db_name")
_port = config("db_port", default=3306, cast=int)


# Use this function in your module to get access to database
def mysql_connection():
    """
    Connect to a MySQL database and return the connection object.
    If connection fails, return None.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=_host_name,
            user=_user_name,
            passwd=_user_password,
            database=_db_name,
            port=_port
        )
    except Error as e:
        connection = None
    return connection
