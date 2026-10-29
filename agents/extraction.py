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
    driver_drunk: bool = Field(
        description=(
            "True only if the text clearly says the PERSON MAKING THE CLAIM "
            "(the insured driver) was drunk or on drugs. "
            "False if the text says ANOTHER driver was drunk. "
            "False if the claimant is only unsure or says they may have had a drink."
        )
    )
    alcohol_uncertain: bool = Field(
        description=(
            "True if the person making the claim says they may have, or did, have "
            "any alcohol or drugs but is unsure or says it was a small amount. "
            "False if alcohol is not mentioned, or if it is about another driver."
        )
    )
    no_valid_licence: bool = Field(description="True only if text says driver had no valid licence")
    racing_or_stunt: bool = Field(description="True only if text says racing or stunts")
    intentional_damage: bool = Field(
        description=(
            "True only if the text says the PERSON MAKING THE CLAIM, or someone acting "
            "for them, damaged the car on purpose. "
            "False if a thief, vandal, or other person damaged the car."
        )
    )
    other_driver: bool = Field(
        description=(
            "True if the text says someone OTHER than the policyholder was driving "
            "the insured car (brother, friend, driver, etc). "
            "False if the policyholder was driving, or if it does not say."
        )
    )


llm = ChatGroq(model=MODEL_NAME, temperature=0)
extractor = llm.with_structured_output(ExtractedClaim, method="json_schema")


def extract(description: str) -> ExtractedClaim:
    prompt = (
        "Read this insurance claim text. Fill the fields using ONLY what the text says. "
        "If the text does not mention something, answer false. "
        "Be careful about WHO did something: the person making the claim, or someone else.\n\n"
        f"Claim text: {description}"
    )
    last_error = None
    for attempt in range(2):          # try up to 2 times
        try:
            return extractor.invoke(prompt)
        except Exception as e:
            last_error = e
    raise last_error