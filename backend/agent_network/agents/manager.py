from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph
from agent_network.static.instructions import MANAGER_AGENT_INSTRUCTIONS
from agent_network.static.llm import llm
from agent_network.db.db_tools import get_all_schemas
from agent_network.agents.agent_helper import agent_node
from langchain.schema import SystemMessage


def create_manager(llm, user_message: str, schema: str):
    """Manager Agent to return if the user query is requesting SQL query or general information"""
    
    system_message = f"The following is the schema of the database: {schema}. Use this schema to interpret the user query."

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=MANAGER_AGENT_INSTRUCTIONS),
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]   
    )
    
    message_payload = prompt.format_prompt(messages=[{
        "role": "user",
        "content": user_message 
    }]).to_messages()
    
    response = llm.invoke(message_payload)
    
    manager_response = response.content.strip()
    
    return manager_response