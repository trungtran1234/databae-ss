from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph
from agent_network.static.instructions import CHECKER_AGENT_INSTRUCTIONS
from agent_network.static.llm import llm
from agent_network.db.db_tools import get_all_schemas
from agent_network.agents.agent_helper import agent_node


def checker_node(state):
    """Checker Node to validate the SQL query before execution."""
    # Properly format the schema to be passed to the LLM
    formatted_schema = format_schema_for_llm(state['schema'])

    # Create the prompt that the checker agent will use to validate the SQL query
    prompt = CHECKER_AGENT_INSTRUCTIONS + f"\nUser query: {state['user_query']}\nSchema:\n{formatted_schema}\nSQL Query: {state['sql_query']}"

    # Invoke the LLM with the formatted prompt
    response = llm.invoke(prompt)

    # Get the response from the LLM
    checker_response = response.content.strip()
    state["checker_status"] = checker_response

    print('checker response: ', state['checker_status'])

    # If the checker fails, return to manager node, otherwise move to execution
    if state["checker_status"] == "CHECKER_FAILED":
        state["next"] = "manager"
        state["checkerCount"] += 1
        state["sender"] = "Checker"
        print("Checker failed, returning to manager.")
    else:
        print("Checker passed, moving to executor.")
        state["next"] = "executor"

    return state


def format_schema_for_llm(schema):
    """Format the schema in a human-readable form for the LLM to understand."""
    formatted_schema = ""
    for table_name, table_data in schema['data'].items():
        formatted_schema += f"Table: {table_name}\n"
        for column in table_data['columns']:
            formatted_schema += f" - {column['column_name']} ({column['data_type']})\n"
    return formatted_schema
