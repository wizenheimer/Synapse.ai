import beam

app = beam.App(
    name="venesa",
    cpu=1,
    memory="16Gi",
    python_version="python3.8",
    python_packages=["langchain==0.0.146", "openai==0.27.4"],
)

app.Trigger.RestAPI(
    # Inputs to the API
    inputs={"db_uri": beam.Types.String(), "query": beam.Types.String()},
    # Outputs to the API
    outputs={
        "result": beam.Types.String(),
    },
    # The function to run when the API is invoked
    handler="run.py:venesa",
)
