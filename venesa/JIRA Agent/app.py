import beam

app = beam.App(
    name="venesa",
    cpu=1,
    memory="16Gi",
    python_version="python3.8",
    python_packages=["langchain==0.0.146", "openai==0.27.4", "atlassian-python-api==3.36.0"],
)

app.Trigger.RestAPI(
    # Inputs to the API
    inputs={
    "query": beam.Types.String(),
    "JIRA_API_TOKEN": beam.Types.String(),
    "JIRA_USERNAME": beam.Types.String(),
    "JIRA_INSTANCE_URL": beam.Types.String()
    },
    # Outputs to the API
    outputs={
        "result": beam.Types.String(),
    },
    # The function to run when the API is invoked
    handler="run.py:venesa",
)
