from langchain_core.tools import tool
from typing import List, Dict, Union

@tool
def prediction_model(data: List[Dict[str, Union[str, int, float]]]) -> str:
    """Generates a prediction based on the provided data."""
    return "Tool not created yet."