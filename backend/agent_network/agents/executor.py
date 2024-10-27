from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent_network.static.llm import llm

def create_executor(llm, sql_query: str, system_message: str):
    return "This is a placeholder response from the executor agent."