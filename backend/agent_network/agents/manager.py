from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph
from agent_network.static.instructions import MANAGER_AGENT_INSTRUCTIONS
from agent_network.static.llm import llm
from agent_network.db.db_tools import get_all_schemas
from agent_network.agents.agent_helper import agent_node


def manager_node(state):
    """Manager Agent to handle SQL query generation and manage the checker loop."""
    
    # Check if the checker has failed too many times
    if state.get("checkerCount") > 3:
        # Stop retrying and send to user response if too many failures
        print("Too many checker failures, sending to user_respondent.")
        state["next"] = "user_respondent"
        return state
    
    if state.get("sender") == 'Checker':
        prompt = MANAGER_AGENT_INSTRUCTIONS + f"The given SQL query is not correct: {state['sql_query']}, give feedback on how to fix it. \nThe user query is: {state['user_query']}\n The schema is: {state['schema']}"

    # Create the system prompt for the manager agent
    prompt = MANAGER_AGENT_INSTRUCTIONS + f" \nThe user query is: {state['user_query']}\n The schema is: {state['schema']}"
    
    # Invoke the LLM to process the prompt
    response = llm.invoke(prompt)
    
    # Get the LLM response (instructions) and update the state
    manager_response = response.content.strip()
    state["manager_instructions"] = manager_response

    print('Manager instructions: ', state['manager_instructions'])

    # Decide next step based on the instructions
    if "NOT_QUERY" in state["manager_instructions"]:
        # If not a query, send to the user respondent for further handling
        state["next"] = "user_respondent"
    else:
        # If the query needs to be validated, send it back to the checker
        print("Sending to generator.")
        state["next"] = "Generator"  # Go back to the checker for validation

    return state
