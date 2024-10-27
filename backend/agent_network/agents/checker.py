from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent_network.static.llm import llm
from agent_network.agents.agent_helper import agent_node

def create_checker(llm, sql_query: str, system_message: str):
    return "This is a placeholder response from the checker agent."  