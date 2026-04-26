import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
SCAN_INTERVAL_MINUTES = int(os.getenv("SCAN_INTERVAL_MINUTES", 15))
