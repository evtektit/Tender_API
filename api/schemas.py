from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

Source = Literal["rts", "sber", "zakazrf", "agregatoreat"]

class ParseRequest(BaseModel):
    query: str = Field(..., min_length=1)
    sources: List[Source] = ["rts", "sber", "zakazrf", "agregatoreat"]
    limit: int = 20

class ParseResponse(BaseModel):
    count: int
    results: List[Dict[str, Any]]
    errors: Dict[str, str] = {}
