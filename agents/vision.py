import base64
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class DamageReport(BaseModel):
    is_car: bool = Field(description="True only if the image clearly shows a car or vehicle")
    damage_visible: bool = Field(description="True only if real damage is visible on the vehicle. False if not a vehicle.")
    severity: Literal["none", "minor", "moderate", "severe", "unknown"] = Field(
        description="none = no damage. unknown = image is not a vehicle or too unclear."
    )
    damaged_parts: list[str] = Field(description="Visible damaged parts, for example 'front bumper'. Empty list if none.")
    summary: str = Field(description="One short sentence describing what you see")


llm = ChatGoogleGenerativeAI(
    model=os.getenv("VISION_MODEL"),
    temperature=0,
    timeout=120,
    max_retries=1,
)
analyzer = llm.with_structured_output(DamageReport)


def analyze_damage(image_path: str) -> DamageReport:
    data = Path(image_path).read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")

    message = HumanMessage(content=[
        {
            "type": "text",
            "text": (
                "You are checking a photo for an insurance claim. "
                "Describe ONLY what you can actually see. "
                "If the image is not a vehicle, set is_car=false, damage_visible=false, "
                "severity=unknown. Never guess damage that you cannot see."
            ),
        },
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
    ])

    last_error = None
    for attempt in range(2):
        try:
            return analyzer.invoke([message])
        except Exception as e:
            last_error = e
    raise last_error