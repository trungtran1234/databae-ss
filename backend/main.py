import functools
import os
from agent_network.agents.generator import generator_node
from agent_network.agents.manager import manager_node
from agent_network.agents.executor import executor_node
from agent_network.agents.checker import checker_node
from agent_network.agents.respondent import respondent_node
from agent_network.agents.analyzer import analyzer_node
from langgraph.graph import END, START, StateGraph
from agent_network.agents.agent_helper import AgentState
from IPython.display import Image, display
from langgraph.prebuilt import ToolNode
from agent_network.tools.pie_chart_tool import generate_pie_chart
from agent_network.tools.table_tool import generate_table
from agent_network.tools.bar_chart_tool import generate_bar_chart


def router(state):
    """
    Routes the workflow to the next node based on the 'next' field in the state.
    This field should be set by each node to indicate where to go next.
    """
    next_node = state.get("next")

    
    if next_node:
        # Route to the node specified in the 'next' field
        return next_node
    
    
    
    # if no 'next' field is set
    return "no next field"

tools = [generate_table, generate_pie_chart, generate_bar_chart]
# tool_node = ToolNode(tools)

workflow = StateGraph(AgentState)
workflow.add_edge(START, "Manager")
workflow.add_node("Manager", manager_node)
workflow.add_node("Generator", generator_node)
workflow.add_node("Executor", executor_node)
workflow.add_node("Checker", checker_node)
workflow.add_node("Respondent", respondent_node)
workflow.add_node("Analyzer", functools.partial(analyzer_node, tools=tools))
# workflow.add_node("Tools", tool_node)

# Manager go to Generator or respondent
workflow.add_conditional_edges(
    "Manager", router, {
        "Generator": "Generator",
        "Respondent": "Respondent",
    }
)

# Generator goes to checker
workflow.add_conditional_edges(
    "Generator", router, {
        "Checker": "Checker",
    }
)

# Checker can go to Executor or back to Manager
workflow.add_conditional_edges(
    "Checker", router, {
        "Executor": "Executor",
        "Manager": "Manager",
    }
)

workflow.add_conditional_edges(
    "Executor", router, {
        "Analyzer": "Analyzer",
    }
)

# workflow.add_conditional_edges(
#     "Analyzer", router, {
#         "Tools": "Tools",
#         "END": END,
#     }
# )

# workflow.add_conditional_edges(
#     "Tools", router, {
#         "Analyzer": "Analyzer",
#     }
# )

#end at executor for now
workflow.add_edge("Analyzer", END)

#uncomment this when entire flow is implemented
#workflow.add_edge("Respondent", END)

graph = workflow.compile()

graph_image_path = os.path.join(os.getcwd(), "graph", "agent_network.png")

# Generate and save the graph as an image
png_data = graph.get_graph(xray=True).draw_mermaid_png()

# Ensure the directory exists (create if not)
os.makedirs(os.path.dirname(graph_image_path), exist_ok=True)

# Save the image data to the defined path
with open(graph_image_path, "wb") as file:
    file.write(png_data)

print(f"Updated graph saved to {graph_image_path}")