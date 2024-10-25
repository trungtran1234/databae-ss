from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, START, StateGraph
from langgraph.static.instructions import QUERY_GENERATOR_INSTRUCTIONS
from langgraph.static.llm import llm


def query_generator(llm, tools, system_message: str, user_message: str):
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
    
    response = llm(message_payload)
    
    sql_query = response["choices"][0]["message"]["content"].strip()
    
    return sql_query
