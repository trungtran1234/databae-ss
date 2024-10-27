from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph
from agent_network.static.instructions import RESPONDENT_AGENT_INSTRUCTION
from agent_network.static.llm import llm
from agent_network.db.db_tools import get_all_schemas
from agent_network.agents.agent_helper import agent_node

def respondent_node(state):
    """User Respondent Node to respond to the user with appropriate messages."""
    
    # Craft the response based on the state
    if state.get("checkerCount", 0) > 3:
        # If there were too many checker failures, respond accordingly
        response = "We encountered too many issues validating your query. Please try rephrasing your request or contact support."
    elif "NOT_QUERY" in state["manager_instructions"]:
        prompt = RESPONDENT_AGENT_INSTRUCTION + f" \nThe user query is: {state['user_query']}\n The schema is: {state['schema']}"
        response = llm.invoke(prompt)
    else:
        # If the process succeeded, respond with the query results or success message
        response = "Your query was successful! Here are the results:\n" + str(state.get("execution_result", "No results found."))

    # Store the response in the state for further use
    state["response"] = response
    state["next"] = END  # End the flow after responding to the user

    print("Response: ", response)
    return state
