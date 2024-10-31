from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import Annotated, Sequence, List
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
    AIMessage
)
import operator


class QueryRequest(BaseModel):
    user_query: str

class AgentState(TypedDict):
    user_query: HumanMessage
    schema: dict
    manager_instructions: str
    sql_query: str
    checker_status: str
    checkerCount: int
    execution_result: dict
    analysis_result: list
    analyzer_messages: str
    analyzer_tool_calls: List[dict]
    analyzer_response_content: str = ""
    tool_called: bool = False
    response: str
    sender: str
    next: str
