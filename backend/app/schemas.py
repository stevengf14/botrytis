from pydantic import BaseModel


class PredictResponse(BaseModel):
    label: str
    confidence: float
