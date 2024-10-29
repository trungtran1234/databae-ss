from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END
from agent_network.static.instructions import RESPONDENT_AGENT_INSTRUCTION
from agent_network.static.llm import llm

def respondent_node(state):
    """User Respondent Node to respond to the user with appropriate messages."""

    if state['sender'] == 'Checker' and state.get("checkerCount", 0) > 3:
        # if there were too many checker failures, respond accordingly, edit this
        response = "We encountered too many issues validating your query. Please try rephrasing your request or contact support."
    elif  state['sender'] == 'Manager' and "NOT_QUERY" in state["manager_instructions"]:
        prompt = RESPONDENT_AGENT_INSTRUCTION + f" \nThe user query is: {state['user_query']}\n The schema is: {state['schema']}"
        response = llm.invoke(prompt)
    else:
        response = "Your query was successful! Here are the results:\n" + str(state.get("execution_result", "No results found."))

    state["response"] = response
    state["next"] = END 

    print("Response: ", response)
    return state
