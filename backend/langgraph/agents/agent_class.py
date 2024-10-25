from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_query: str
    system_message: str