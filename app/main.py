from fastapi import FastAPI
from app.scanner import scan_market
from app.models import ScanResponse

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Short Squeeze Scanner running"}

@app.get("/scan", response_model=ScanResponse)
def scan():
    return ScanResponse(results=scan_market())
