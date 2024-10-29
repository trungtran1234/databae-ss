from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END
from agent_network.static.instructions import RESPONDENT_AGENT_INSTRUCTION
from agent_network.static.llm import llm
from langchain.schema import SystemMessage, HumanMessage

def respondent_node(state):
    """User Respondent Node to respond to the user with appropriate messages."""

    if state['sender'] == 'Checker' and state.get("checkerCount", 0) > 3:
        # if there were too many checker failures, respond accordingly, edit this
        system_message = f"Too many checker failures. The user query is: {state['user_query']} \n The SQL that was generated was {state['sql_query']}"
        human_message = "The system has encountered multiple issues generating the relevant sql query. Create a response to the user explaining the situation and suggesting they rephrase their query."
    elif  state['sender'] == 'Manager' and "NOT_QUERY" in state["manager_instructions"]:
        system_message = f" \nThe user query is: {state['user_query']}\n The schema is: {state['schema']}"
        human_message = "The manager has determined that the user query is not asking for SQL query. Create a general response to the user based on their query."
    elif state['sender'] == 'Executor':
        system_message = f"Here are the context \n User query: {state['user_query']}\n SQL Query: {state['sql_query']}\n Schema: {state['schema']}"
        human_message = "The query was executed successfully but returned no results. Create a response for the user that explains why is this so."
    else:
        system_message = f"Here are the context \n User query: {state['user_query']}\n Schema: {state['schema']} \n Execution Result: {str(state.get('execution_result', 'No results found.'))}"
        human_message = "The query was successful. Explain the execution result to the user."

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=RESPONDENT_AGENT_INSTRUCTION),
            SystemMessage(content=system_message),
            HumanMessage(content=human_message), 
        ]
    )
    prompt = prompt.partial(system_message=system_message, human_message=human_message)

    response = llm.invoke(prompt.format())

    state["response"] = response.content.strip()
    state["next"] = END 

    print("Response: ", state["response"])

    return state
