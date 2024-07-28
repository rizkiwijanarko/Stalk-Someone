from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms import HuggingFacePipeline
import os

from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()
    print("Hello LangChain!")
    os.getenv("GOOGLE_API_KEY")

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
    linkedin_data = scrape_linkedin_profile(profile_url="https://www.linkedin.com/in/rizki-wijanarko/", mock=True)
    res = chain.invoke(input={"information": linkedin_data})

    print(res)

