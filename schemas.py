"""
Pydantic models that describe the JSON our API sends back.

FastAPI uses these to check the data and to build the /docs page.
"""

from pydantic import BaseModel


class ReadingResponse(BaseModel):
    raw_value: int
    moisture_percent: float
    status: str           # "dry", "normal" or "wet"
    message: str
    timestamp: str
    simulated: bool       # True while we have no real sensor
