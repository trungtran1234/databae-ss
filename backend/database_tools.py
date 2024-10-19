import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, port, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=port,
            database=db_name
        )
        print("Connection to DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connection closed")