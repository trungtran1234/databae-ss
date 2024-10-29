import mysql.connector
from agent_network.db.db_tools import create_connection
from langgraph.graph import END

def executor_node(state):
    """Executor Node to execute the SQL query and return the results."""
    sql_query = state.get("sql_query")
    
    if not sql_query:
        state["execution_result"] = {"error": "No SQL query generated"}
        state["next"] = "Respondent" 
        return state

    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(sql_query)
        
        result = cursor.fetchall()

        # store the results in the state
        state["execution_result"] = {
            "status": "success",
            "result": result
        }

        # End the flow here FOR NOW
        state["next"] = END 

        # uncomment this when you have the analyzer agent implemented
        # if result:
        #     state["next"] = "Analyzer"  # go to analyzer
        # else:
        #     state["next"] = "Manager"  # if no results, go back to manager

    except mysql.connector.Error as err:
        # Handle any SQL execution errors
        state["execution_result"] = {
            "status": "error",
            "error": str(err)
        }
        state["next"] = "Manager" # go back to manager if error

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    print('execution result: ', state["execution_result"])
    return state
