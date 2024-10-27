import os
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph
from agents.agent_helper import AgentState
from tools.pie_chart_tool import pie_chart_generator
from tools.table_tool import table_generator
from tools.predictive_tool import prediction_model
from static.llm import llm
from agents.agent_helper import agent_node
from agents.manager import create_manager
from agents.respondent import create_respondent
from agents.generator import create_query_generator
from agents.checker import create_checker
from agents.executor import create_executor
from agents.analyzer import create_analyzer
import functools


manager_agent = create_manager(llm, "blank", "blank")
manager_node = functools.partial(agent_node, agent=manager_agent, name="Manager")

respondent_agent = create_respondent(llm, "blank", "blank")
respondent_node = functools.partial(agent_node, agent=respondent_agent, name="Respondent")

generator_agent = create_query_generator(llm, "blank", "blank")
generator_node = functools.partial(agent_node, agent=generator_agent, name="Query Generator")

checker_agent = create_checker(llm, "blank", "blank")
checker_node = functools.partial(agent_node, agent=checker_agent, name="Checker")

executor_agent = create_executor(llm, "blank", "blank")
executor_node = functools.partial(agent_node, agent=executor_agent, name="Executor")

analyzer_agent = create_analyzer(llm, "blank", "blank")
analyzer_node = functools.partial(agent_node, agent=analyzer_agent, name="Analyzer")

tools = [table_generator, pie_chart_generator, prediction_model]
tool_node = ToolNode(tools)

# Define the router function
def router(state):
    # This router checks if a tool call is made by the analyzer
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        return "Respondent"
    return "continue"

# Set up the graph
workflow = StateGraph(AgentState)

# Add nodes to the graph
workflow.add_node("Manager", manager_node)
workflow.add_node("Respondent", respondent_node)
workflow.add_node("Query Generator", generator_node)
workflow.add_node("Checker", checker_node)
workflow.add_node("Executor", executor_node)
workflow.add_node("Analyzer", analyzer_node)
workflow.add_node("call_tool", tool_node)

# Define edges using the router function
# Manager can go to Query Generator or Respondent directly
workflow.add_conditional_edges(
    "Manager", router, {
        "continue": "Query Generator",
        "Respondent": "Respondent",
    }
)

# Query Generator always goes to Checker
workflow.add_conditional_edges(
    "Query Generator", router, {
        "continue": "Checker",
    }
)

# Checker can go to Executor or back to Manager
workflow.add_conditional_edges(
    "Checker", router, {
        "continue": "Executor",
        "Manager": "Manager",
    }
)

# Executor always goes to Analyzer
workflow.add_conditional_edges(
    "Executor", router, {
        "continue": "Analyzer",
    }
)

# Analyzer can go to Respondent or invoke a tool (call_tool)
workflow.add_conditional_edges(
    "Analyzer", router, {
        "continue": "Respondent",
        "call_tool": "call_tool"
    }
)

# Tool node routing (always routes back to the Analyzer after tool execution)
workflow.add_conditional_edges(
    "call_tool", lambda state: "Analyzer", {
        "Analyzer": "Analyzer"
    }
)

# Respondent ends the workflow
workflow.add_edge("Respondent", END)

# Set the start node of the graph
workflow.add_edge(START, "Manager")

# Compile the graph
graph = workflow.compile()

graph_image_path = os.path.join("agent_network", "graph_updated.png")

# Generate and save the graph as an image
png_data = graph.get_graph(xray=True).draw_mermaid_png()

# Ensure the directory exists (create if not)
os.makedirs(os.path.dirname(graph_image_path), exist_ok=True)

# Save the image data to the defined path
with open(graph_image_path, "wb") as file:
    file.write(png_data)

print(f"Updated graph saved to {graph_image_path}")