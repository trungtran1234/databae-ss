from langchain_core.tools import tool
from typing import List, Dict, Union

@tool
def pie_chart_generator(query_result: List[Dict[str, Union[str, int, float]]]) -> str:
    """Generates a pie chart from the provided query result."""
    return "Tool not created yet."