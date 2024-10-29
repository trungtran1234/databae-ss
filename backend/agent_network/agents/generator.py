from langchain_core.prompts import ChatPromptTemplate
from agent_network.static.instructions import QUERY_GENERATOR_INSTRUCTIONS
from agent_network.static.llm import llm
from langchain.schema import SystemMessage, HumanMessage


def generator_node(state):
    """Query Generator Agent to return an SQL query based on user's natural language input"""
    
    system_message =  QUERY_GENERATOR_INSTRUCTIONS + f"""
                The following is the schema of the database: {state['schema']}.
                Additionally, here are specialized instructions based on the user query: {state['manager_instructions']}
                Use these details to generate an SQL query that fulfills the user's request.
                """
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=QUERY_GENERATOR_INSTRUCTIONS),
            SystemMessage(content=system_message),
            HumanMessage(content=state["user_query"].content), 
        ]   
    )
    prompt = prompt.partial(system_message=system_message)

    response = llm.invoke(prompt.format())
    
    sql_query = response.content.strip()
    
    state["sql_query"] = sql_query

    state["next"] = "Checker"

    print('generated sql query: ', state['sql_query'])
    return state

