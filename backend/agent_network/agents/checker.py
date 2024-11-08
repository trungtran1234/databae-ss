from langchain_core.prompts import ChatPromptTemplate
from agent_network.static.instructions import CHECKER_AGENT_INSTRUCTIONS
from agent_network.static.llm import llm
from langchain.schema import SystemMessage, HumanMessage

def checker_node(state):
    """Checker Node to validate the SQL query before execution."""
    print("Checker node started with given state: ", state)

    system_message = f"\nUser query: {state['user_query']}\nSchema:{state['schema']}\nSQL Query: {state['sql_query']}"
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=CHECKER_AGENT_INSTRUCTIONS),
            SystemMessage(content=system_message),
            HumanMessage(content=state["user_query"].content), 
        ]   
    )
    prompt = prompt.partial(system_message=system_message)

    response = llm.invoke(prompt.format_messages())

    checker_response = response.content.strip()
    state['checker_status'] = checker_response

    print('checker response: ', state['checker_status'])
    
    state['sender'] = "Checker"
    # if the checker fails, return to manager node, otherwise move to execution
    if state["checker_status"] == "CHECKER_FAILED":
        print('Checker failed!')
        state['next'] = "Manager"
        state['checkerCount'] += 1 # increment checker count
        print("Checker failed, returning to manager.")
    else:
        print("Checker passed, moving to executor.")
        state['next'] = "Executor"

    return state
