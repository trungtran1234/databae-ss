from fastapi import FastAPI, HTTPException
from agent_network.agents.agent_helper import QueryRequest
from agent_network.static.llm import llm
from pydantic import BaseModel
from agent_network.db.db_tools import check_and_add_db_credentials, get_all_schemas
from agent_network.main import run_workflow

app = FastAPI()

class DbBodyModel(BaseModel):
    host_name: str
    username: str
    password: str
    port: int
    db_name: str

@app.get("/")
def root():
    return "hello world"

@app.post("/submit")
def generate_sql(query_request: QueryRequest):
    try:
        schema = get_all_schemas()
        print(query_request.user_query)
        sql_query = run_workflow(
            user_message=query_request.user_query,
            schema=schema
        )
        return {"sql_query": sql_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# endpoint that takes in database connection details,
# checks if there is the db connection is valid,
# saves it to db_credentials.json
# for now, the db has to have ssl off
# returns 404 if the database is not able to be connected to
@app.post("/input_connection_details")
async def input_connection_details(db: DbBodyModel):
    if check_and_add_db_credentials(db.host_name, db.username, db.password, db.port, db.db_name):
        return "success"
    else: 
        raise HTTPException(status_code=404, detail="Could not connect to database")
    