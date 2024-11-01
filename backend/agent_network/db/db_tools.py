import mysql.connector
from mysql.connector import Error
import json 
import os

# helper function to create the connection to the database
# based on credentials in db_credentials.json
def create_connection():
    connection = None

    if not os.path.abspath('agent_network/db/db_credentials.json'):
        print("no db credentials found")
        return None
    
    with open('agent_network/db/db_credentials.json') as f:
        data = json.load(f)
        host_name = data["host_name"]
        user_name = data["user_name"]
        user_password = data["user_password"]
        port = data["port"]
        db_name = data["db_name"]
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                port=port,
                database=db_name
            )
            print("Connection to MySQL DB successful")
            if connection:
                return connection
            else:
                return None
        except Error as e:
            print(f"The error '{e}' occurred")
            return None

    return connection

# helper function that checks whether the db connection is valid
# and saves it in db_credentials.json
# !!! for now, ssl has to be disabled on the database side
def check_and_add_db_credentials(host_name, user_name, user_password, port, db_name): 
    connection = None 
    try:
        print("connecting")
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            port=port,
            database=db_name,
        )
        if connection:
            print("Connection to MySQL DB successful")
            with open("agent_network/db/db_credentials.json", "w") as f:
                json.dump({"host_name": host_name, 
                           "user_name": user_name, 
                           "user_password": user_password, 
                           "port": port, 
                           "db_name": db_name}, 
                        f)
            close_connection(connection)
            return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False

# helper function to close the connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connection closed")

# helper function to grab all schemas from the database
# it will return a dictionary of the format
# {
# table_name: [ {}'column_name': 'example_name', 'data_type': 'example_data_type' ],
# table_name2: [ 'column_name_2': 'example_name', 'data_type': 'example_data_type' ],
# }
def get_all_schemas():
    conn = create_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s", 
            [conn.database]
        )
        schemas = cursor.fetchall()
    finally:
        cursor.close() 
        conn.close() 

    if schemas:
        dict_of_data_schema = {}
        for schema in schemas:
            db_name = schema[0]  # Database name
            table_name = schema[1]  # Table name
            column_name = schema[2]  # Column name
            data_type = schema[3]  # Data type

            # Check if the database name is already in the dictionary
            if db_name not in dict_of_data_schema:
                dict_of_data_schema[db_name] = {}  # Add the database name as a key with an empty dictionary

            # Check if the table name exists within the current database
            if table_name not in dict_of_data_schema[db_name]:
                dict_of_data_schema[db_name][table_name] = []  # Add the table name as a key with an empty list

            # Add column details to the table's list
            dict_of_data_schema[db_name][table_name].append({
                "column_name": column_name,
                "data_type": data_type
            })

        return dict_of_data_schema
    else:
        return {}
