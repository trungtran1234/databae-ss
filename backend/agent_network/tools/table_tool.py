from langchain_core.tools import tool
from typing import List, Dict, Union

@tool
def table_generator(query_result: List[Dict[str, Union[str, int, float]]]) -> str:
    return "Tool not created yet."