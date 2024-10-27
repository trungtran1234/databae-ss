import mysql.connector  # or any other database connector you're using
from agent_network.db.db_tools import create_connection
def executor_node(state):
    """Executor Node to execute the SQL query and return the results."""

    # Get the SQL query from the state
    sql_query = state.get("sql_query")
    
    if not sql_query:
        # Handle the case where no valid SQL query was generated
        state["execution_result"] = {"error": "No SQL query generated"}
        state["next"] = "user_respondent"
        return state

    try:
        # Establish a connection to the database
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)  # Using dictionary=True to return results as a dict
        
        # Execute the query
        cursor.execute(sql_query)
        
        # Fetch all the results
        result = cursor.fetchall()

        # Store the results in the state
        state["execution_result"] = {
            "status": "success",
            "result": result
        }

        # Decide the next node based on execution
        if result:
            state["next"] = "analyzer"  # Proceed to analyze the results
        else:
            state["next"] = "user_respondent"  # If no result, respond to the user

    except mysql.connector.Error as err:
        # Handle any SQL execution errors
        state["execution_result"] = {
            "status": "error",
            "error": str(err)
        }
        state["next"] = "user_respondent"  # If there's an error, return to user with error message

    finally:
        # Close the database connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    print('execution result: ', state["execution_result"]["status"])
    return state["execution_result"]
