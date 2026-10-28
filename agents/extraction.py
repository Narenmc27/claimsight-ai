from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

load_dotenv()

MODEL_NAME = "openai/gpt-oss-120b"  # change here if Groq retires it


class ExtractedClaim(BaseModel):
    incident_type: Literal[
        "accident", "theft", "fire", "natural_disaster", "wear_and_tear", "other"
    ] = Field(
        description=(
            "Pick exactly ONE word. "
            "accident = collision or crash. "
            "theft = car stolen. "
            "fire = fire damage. "
            "natural_disaster = flood, storm, earthquake. "
            "wear_and_tear = old or worn parts, rust, tyres. "
            "other = anything else."
        )
    )
    driver_drunk: bool = Field(description="True only if text says driver was drunk or on drugs")
    no_valid_licence: bool = Field(description="True only if text says driver had no valid licence")
    racing_or_stunt: bool = Field(description="True only if text says racing or stunts")
    intentional_damage: bool = Field(description="True only if text says damage was done on purpose")


llm = ChatGroq(model=MODEL_NAME, temperature=0)
extractor = llm.with_structured_output(ExtractedClaim, method="json_schema")


def extract(description: str) -> ExtractedClaim:
    prompt = (
        "Read this insurance claim text. Fill the fields using ONLY what the text says. "
        "If the text does not mention something, answer false.\n\n"
        f"Claim text: {description}"
    )
    last_error = None
    for attempt in range(2):          # try up to 2 times
        try:
            return extractor.invoke(prompt)
        except Exception as e:
            last_error = e
    raise last_error