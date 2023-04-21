from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor


def venesa(**inputs):
    db_uri = inputs["db_uri"]
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db)

    agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0), toolkit=toolkit, verbose=False
    )

    query = inputs["query"]

    result = agent_executor.run(query)
    return {"result": result}
