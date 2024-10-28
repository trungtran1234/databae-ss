
import os
from agent_network.agents.generator import generator_node
from agent_network.agents.manager import manager_node
from agent_network.agents.executor import executor_node
from agent_network.agents.checker import checker_node
from agent_network.agents.respondent import respondent_node
from langgraph.graph import END, START, StateGraph
from agent_network.agents.agent_helper import AgentState, agent_node
from IPython.display import Image, display


# def router(state):
#     messages = state["messages"]
#     last_message = messages[-1]
    
#     # If the query requires SQL generation, route to the query generator
#     if "IS_QUERY" in last_message.content:
#         return "query_generator"
    
#     # Continue the conversation if undecided
#     return "continue"


def run_graph():
    """Run the graph to get the SQL query"""
    # manager_agent = create_manager(llm, user_message, schema)
    # print('manager agent created', manager_agent)
    # manager_node = functools.partial(agent_node, agent=manager_agent, name="Manager Agent")
    # print('manager node created')
    # query_generator_agent = create_query_generator(llm, manager_agent, user_message, schema)
    # print('generator agent created')
    # query_generator_node = functools.partial(agent_node, agent=query_generator_agent, name="Query Generator Agent")
    # print('generator node created')

    workflow = StateGraph(AgentState)
    workflow.add_edge(START, "Manager")
    workflow.add_node("Manager", manager_node)
    workflow.add_node("Generator", generator_node)
    workflow.add_node("Executor", executor_node)
    workflow.add_node("Checker", checker_node)
    workflow.add_node("Respondent", respondent_node)
    workflow.add_edge("Manager", "Generator")
    workflow.add_edge("Generator", "Checker")
    workflow.add_edge("Checker", "Manager")
    workflow.add_edge("Manager", "Respondent")
    workflow.add_edge("Checker", "Executor")
    workflow.add_edge("Respondent", END)
    
    graph = workflow.compile()
