from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import GradientLLM
from chainlit import user_session, langchain_factory

from os import environ


@langchain_factory(use_async=False)
def factory():
    env = user_session.get("env")
    assert env is not None
    llm = GradientLLM(
        model_id=env["GRADIENT_MODEL_ID"],
        model_kwargs={
            "max_generated_token_count": 200,
            "temperature": 0.75,
            "top_p": 0.95,
            "top_k": 20,
            "stop": [],
        },
        gradient_workspace_id=env["GRADIENT_WORKSPACE_ID"],
        gradient_access_token=env["GRADIENT_ACCESS_TOKEN"],
    )
    # llm = ChatOpenAI(
    #     temperature=0,
    #     # We don't have access to GPT-4-32k, so we use GPT-4 instead.
    #     # model="gpt-4-32k",
    #     model="gpt-4",
    #     openai_api_key=env["OPENAI_API_KEY"],
    # )
    tools = load_tools(
        [
            "google-search-results-json",
            "llm-math",
            # requests_all can be used to browse the link, however it would easily exceed GPT-4's context length limit.
            # "requests_all"
        ],
        llm=llm,
        google_api_key=env["GOOGLE_API_KEY"],
        google_cse_id=env["GOOGLE_CSE_ID"],
    )
    agent = initialize_agent(
        tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    return agent
