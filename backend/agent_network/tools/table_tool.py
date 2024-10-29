import os
from typing import Annotated
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
import pandas as pd  
repl = PythonREPL()

output_dir = "generated_analysis"

os.makedirs(output_dir, exist_ok=True)

@tool
def generate_table(
    code: Annotated[str, "The python code to execute to generate your table."]
):
    """Use this tool to generate a table from Python code and save it as HTML in a .txt file."""
    try:
        print(f"Table tool invoked with code:\n{code}")

        result = repl.run(code)
        
        try:
            data = eval(result)
            df = pd.DataFrame(data)
            
            table_html = df.to_html(index=False) 

            file_name = "table_output.txt" 
            file_path = os.path.join(output_dir, file_name)
            
            with open(file_path, "w") as file:
                file.write(table_html)
            
            return f"Successfully generated table and saved to {file_path}"
        
        except Exception as e:
            return f"Code executed, but failed to generate a table. Output was:\n{result}\nError: {repr(e)}"

    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
