from langchain_groq import ChatGroq
import os

llm=ChatGroq(temperature=0,
             model_name="llama3-70b-8192",
             api_key=os.getenv("GROQ_API_KEY"))
