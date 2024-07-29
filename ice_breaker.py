from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import look_up as linkedin_lookup_agent
import os

from third_parties.linkedin import scrape_linkedin_profile

def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_username, mock=True)

    summary_template = """""
        given the LinkedIn information {information} about a person, I want you to create:
        1. a short description of the person
        2. two interesting facts about the person
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    model = "gemini-1.5-flash"
    llm = ChatGoogleGenerativeAI(model=model)
    chain = summary_prompt_template | llm
    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter!")
    ice_break_with(name="Kharisma Rizki Wijanarko")

