
from langchain_core.prompts import ChatPromptTemplate
from agent_network.static.instructions import ANALYZER_AGENT_INSTRUCTIONS
from langchain.schema import SystemMessage, HumanMessage
from agent_network.static.llm import llm
import json
from langgraph.graph import END
def analyzer_node(state, tools):
    """Analyzer Node to analyze the results of the SQL query execution and choose the appropriate tool to analyze the query results."""

    

    system_message = f"\nUser query: {state['user_query'].content}\nResult: {state['execution_result']['result']}"


    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=ANALYZER_AGENT_INSTRUCTIONS),
            SystemMessage(content=system_message),
            HumanMessage(content=state["user_query"].content),  
        ]
    )
    
   

    formated = prompt.format_messages(system_message=system_message, tool_names=", ".join([tool.name for tool in tools]))


    bound_llm = llm.bind_tools(tools)
    response = bound_llm.invoke(formated)

    tool_calls = response.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']

            for tool in tools:
                if tool.name == tool_name:
                    tool_result = tool(tool_args['code'])  

                    state["analysis_result"] = tool_result
                    state["next"] = END

                    print(f"Tool {tool_name} executed with result: {tool_result}")
                    break

    return state



    
