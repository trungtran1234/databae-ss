from pydantic import BaseModel
from typing_extensions import TypedDict
from typing import Annotated, Sequence
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
    user_query: str
    schema: dict
    manager_instructions: str
    sql_query: str
    checker_status: str
    checkerCount: int
    execution_result: dict
    analysis_result: dict
    response: str
    sender: str

def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }
