from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope
import json
from db_tools import check_and_add_db_credentials

AGENT_ADDRESS = "agent1q2s9fzzvknhuajeplqfp5zeff9ejmraxmcpcqpeup3kajwvkkxxwcqnhwt2"

app = FastAPI()

class TestRequest(Model):
    message: str

class DbBodyModel(BaseModel):
    host_name: str
    username: str
    password: str
    port: int
    db_name: str

async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=5)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["text"]
    return response

@app.get("/")
def read_root():
    return "Hello from the Agent controller"

@app.post("/endpoint")
async def make_agent_call(req: Request):
    model = TestRequest.parse_obj(await req.json())
    try:
        res = await agent_query(model)
        return f"successful call - agent response: {res}"
    except Exception as e:
        return f"unsuccessful agent call: {str(e)}"

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
    
