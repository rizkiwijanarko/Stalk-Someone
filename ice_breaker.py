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

    summary_template = """ 
        You are an expert LinkedIn profile consultant. Given the LinkedIn information below about a person, please provide the following:

        1. **Profile Critique:**
            - A brief analysis (2-3 sentences) highlighting the strengths and weaknesses of the profile's overall presentation.

        2. **Actionable Feedback:**
            - **Three** specific and actionable suggestions to improve the person's profile.
            - For each suggestion, clearly specify which part of the profile it pertains to (e.g., Headline, Summary, Experience).

        Your answer should be in the following format:
        \n{format_instructions}

        Below is the LinkedIn information to analyze:
        {information}

        Your answer should follow the example format above.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
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

