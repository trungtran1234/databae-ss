import os
from typing import Annotated
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
import matplotlib.pyplot as plt
import base64
from io import BytesIO

repl = PythonREPL()

plt.switch_backend('Agg')

output_dir = "generated_analysis"

os.makedirs(output_dir, exist_ok=True)

@tool
def generate_bar_chart(
    code: Annotated[str, "The python code to execute to generate your bar chart."]
):
    """Use this tool to generate a bar chart from Python code and save it to a file."""
    try:
        repl.run(code)
        print("bar chart code executed")

        file_name = "bar_chart.png" 
        file_path = os.path.join(output_dir, file_name)

        plt.savefig(file_path)
        plt.close()

        
        return f"Successfully generated bar chart and saved to {file_path}"

    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
