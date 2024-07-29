import os
from dotenv import load_dotenv

from tools.tools import search_profile_url_tavily

load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain import hub

def look_up(name: str) -> str:
    """
    Look up a LinkedIn profile by name
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    template = """given the full name: {name_of_person}, 
    I want you to find the LinkedIn profile of the person. 
    Your answer should only contain the url."""

    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=search_profile_url_tavily,
            description="useful for finding the linkedin page url of a person",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

    linkedin_profile_url = result["output"]

    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = look_up(name="Kharisma Rizki Wijanarko")
    print(linkedin_url)