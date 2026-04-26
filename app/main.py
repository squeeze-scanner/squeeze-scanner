from fastapi import FastAPI
from app.scanner import scan_market

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Short Squeeze Scanner running"}

@app.get("/scan")
def scan():
    return scan_market()
from apscheduler.schedulers.background import BackgroundScheduler
from app.scanner import scan_market

scheduler = BackgroundScheduler()

def scheduled_scan():
    results = scan_market()
    print("SCAN RESULTS:", results)

scheduler.add_job(scheduled_scan, "interval", minutes=15)
scheduler.start()
