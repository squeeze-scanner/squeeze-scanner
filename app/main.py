from fastapi import FastAPI
from app.scanner import scan_market

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Short Squeeze Scanner running"}

@app.get("/scan")
def scan():
    return scan_market()
