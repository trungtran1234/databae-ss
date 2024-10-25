from crewai import Agent, LLM, Task, Crew
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq


load_dotenv()

llm=ChatGroq(temperature=0,
             model_name="llama3-70b-8192",
             api_key=os.getenv("GROQ_API_KEY"))

manager = Agent(
  role='Manager',
  goal='',
  backstory="""You're a data analyst at a large company.
    You're responsible for analyzing data and providing insights
    to the business.
    You're currently working on a project to analyze the
    performance of our marketing campaigns.""",

  llm=llm
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)