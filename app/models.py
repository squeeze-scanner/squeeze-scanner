from pydantic import BaseModel
from typing import List


class StockScanResult(BaseModel):
    ticker: str
    rsi: float
    short_interest: float
    days_to_cover: float
    score: float


class ScanResponse(BaseModel):
    results: List[StockScanResult]
