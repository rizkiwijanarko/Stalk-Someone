from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="Brief analysis about the person's weakness and strength of the LinkedIn profile.")
    facts: List[str] = Field(description="Actionable feedback to improve the person's LinkedIn profile.")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}

summary_parser = PydanticOutputParser(pydantic_object=Summary)
