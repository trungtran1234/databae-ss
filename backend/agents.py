from crewai import Agent, LLM, Task, Crew
from dotenv import load_dotenv

load_dotenv()

llm = LLM(model="gpt-4", temperature=0.7)
agent = Agent(
  role='Data Analyst',
  goal='Extract actionable insights',
  backstory="""You're a data analyst at a large company.
    You're responsible for analyzing data and providing insights
    to the business.
    You're currently working on a project to analyze the
    performance of our marketing campaigns.""",

  llm=llm
)

task = Task(
    description='Find and summarize the latest and most relevant news on AI',
    agent=agent,
    expected_output='A bullet list summary of the top 5 most important AI news',
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)