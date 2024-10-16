from typing import Tuple

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import look_up as linkedin_lookup_agent
import os
from output_parser import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile

def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_username, mock=True)

    summary_template = """""
        given the LinkedIn information {information} about a person, I want you to create:
        1. A brief critique of the the way the profile is written
        2. 3 crucial actionable feedback to improve the the person's profile. Specify which part of the profile you are referring to.
        
        Your answer should be in the following format:
        \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables = {"format_instructions": summary_parser.get_format_instructions()}
    )

    model = "gemini-1.5-flash"
    llm = ChatGoogleGenerativeAI(model=model)

    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter!")
    ice_break_with(name="Kharisma Rizki Wijanarko")

