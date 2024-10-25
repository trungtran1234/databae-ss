from fastapi import FastAPI, HTTPException
from agent_network.agents.agent_class import QueryRequest
from agent_network.agents.generator import query_generator
from agent_network.static.llm import llm

app = FastAPI()

@app.get("/")
def root():
    return "hello world"

@app.post("/submit")
def generate_sql(query_request: QueryRequest):
    try:
        sql_query = query_generator(
            llm=llm, 
            system_message=query_request.system_message, 
            user_message=query_request.user_query
        )
        return {"sql_query": sql_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))