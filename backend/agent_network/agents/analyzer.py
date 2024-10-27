from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent_network.static.llm import llm
from agent_network.tools.table_tool import table_generator
from agent_network.tools.pie_chart_tool import pie_chart_generator
from agent_network.tools.predictive_tool import prediction_model

def create_analyzer(llm, user_request: str, query_result):
    return "This is a placeholder response from the analyzer agent."