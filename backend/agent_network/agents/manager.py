from langchain_core.prompts import ChatPromptTemplate
from agent_network.static.instructions import MANAGER_AGENT_INSTRUCTIONS
from agent_network.static.llm import llm
from langchain.schema import SystemMessage, HumanMessage

def manager_node(state):
    """Manager Agent to handle SQL query generation and manage the checker loop."""
    
    print("Manager node started.")
    print('')
    # check if checker has failed over 3 times
    if state.get("sender") == 'Checker' and state.get("checkerCount") > 3:
        print("Too many checker failures, sending to user respondent.")
        state["sender"] = "Checker"
        state["next"] = "Respondent"
        return state
    
    system_message = f"The following is the schema of the database: {state['schema']}. Use this schema to interpret the user query."

    if state.get("sender") == 'Checker':
        system_message = f"The given SQL query is not correct: {state['sql_query']}, give feedback on how to fix it. \nThe user query is: {state['user_query']}\n The schema is: {state['schema']}"

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=MANAGER_AGENT_INSTRUCTIONS),
            SystemMessage(content=system_message),
            HumanMessage(content=state["user_query"].content), 
        ]   
    )
    prompt = prompt.partial(system_message=system_message)

    response = llm.invoke(prompt.format_messages())
    
    manager_response = response.content.strip()
    state["manager_instructions"] = manager_response

    print('Manager instructions: ', state['manager_instructions'])

    state["sender"] = "Manager"
    if "NOT_QUERY" in state["manager_instructions"]:
        state["next"] = "Respondent"
    else:
        print("Sending to generator.")
        state["next"] = "Generator"

    return state
