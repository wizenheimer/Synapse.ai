import os
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.jira.toolkit import JiraToolkit
from langchain.llms import OpenAI
from langchain.utilities.jira import JiraAPIWrapper

def set_environment(**inputs):
    os.environ["JIRA_API_TOKEN"] = inputs["JIRA_API_TOKEN"]
    os.environ["JIRA_USERNAME"] = inputs["JIRA_USERNAME"]
    os.environ["JIRA_INSTANCE_URL"] = inputs["JIRA_INSTANCE_URL"]

def venesa(**inputs):
    set_environment(**inputs)
    llm = OpenAI(temperature=0)
    jira = JiraAPIWrapper()
    toolkit = JiraToolkit.from_jira_api_wrapper(jira)
    agent = initialize_agent(
        toolkit.get_tools(),
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )   
    query = inputs["query"]
    result = agent.run(query)
    
    return {"result": result}
