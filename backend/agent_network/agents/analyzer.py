
from langchain_core.prompts import ChatPromptTemplate
from agent_network.static.instructions import ANALYZER_AGENT_INSTRUCTIONS
from langchain.schema import SystemMessage, HumanMessage
from agent_network.static.llm import llm
import json
from langgraph.graph import END
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
    AIMessage
)

def analyzer_node(state, tools):
    """Analyzer Node to analyze the results of the SQL query execution and choose the appropriate tool to analyze the query results."""
    print("is tool called? ", state.get("tool_called", "no"))
    print("HEY IM IN ANALYZER NODE")

    if state["tool_called"] == True:
        # The user has already called a tool, so we don't need to analyze the results again
        state["next"] = "END"
        return state

    

    system_message = f"\nUser query: {state['user_query'].content}\nResult: {state['execution_result']['result']} \n"


    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=ANALYZER_AGENT_INSTRUCTIONS),
            SystemMessage(content=system_message),
            HumanMessage(content="Here are the tools available for you to use: {tool_names}. If you are done using the tools, have you response start with FINAL_ANSWER, otherwise do not"),  
        ]
    )

    formated = prompt.format_messages(system_message=system_message, tool_names=", ".join([tool.name for tool in tools]))


    bound_llm = llm.bind_tools(tools)
    response = bound_llm.invoke(formated)

    state["analyzer_tool_calls"] = response.tool_calls
    state["analyzer_response_content"] = response.content

    # Prepare messages for the ToolNode
    state["analyzer_messages"] = [AIMessage(content=state["analyzer_response_content"], tool_calls=state["analyzer_tool_calls"])]

    # Determine the next node based on whether there are tool calls
    if response.tool_calls:
        state["tool_called"] = True
        state["next"] = "Analyzer_Tools"
    else:
        state["next"] = "END"
    state["sender"] = "Analyzer"

    return state



    
