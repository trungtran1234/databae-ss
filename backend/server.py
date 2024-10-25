from fastapi import FastAPI, HTTPException
from agent_network.agents.agent_helper import QueryRequest
from agent_network.agents.manager import create_manager
from agent_network.static.llm import llm
from pydantic import BaseModel
from agent_network.db.db_tools import check_and_add_db_credentials, get_all_schemas

app = FastAPI()

@app.get("/")
def root():
    return "hello world"

@app.post("/submit")
def generate_sql(query_request: QueryRequest):
    try:
        schema = get_all_schemas()
        sql_query = create_manager(
            llm=llm, 
            user_message=query_request.user_query,
            schema=schema
        )
        return {"sql_query": sql_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))