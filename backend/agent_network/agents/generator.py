from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph
from agent_network.static.instructions import QUERY_GENERATOR_INSTRUCTIONS
from agent_network.static.llm import llm
import functools
from agent_network.agents.agent_helper import agent_node


def create_query_generator(llm, system_message: str, user_message: str):
    """Query Generator Agent to return an SQL query based on user's natural language input"""
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                QUERY_GENERATOR_INSTRUCTIONS,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    prompt = prompt.partial(system_message=system_message)
    
    message_payload = prompt.format_prompt(messages=[{
        "role": "user",
        "content": user_message 
    }]).to_messages()
    
    response = llm.invoke(message_payload)
    
    sql_query = response.content.strip()
    
    return sql_query

query_generator = create_query_generator(
    llm=llm,
    system_message="This is where the instruction from the manager agent will be placed",
    user_message="This is where the user's natural language query will be placed",
)
query_generator_node = functools.partial(agent_node, agent=query_generator, name="Query Generator")
