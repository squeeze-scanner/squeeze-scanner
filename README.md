# Short Squeeze Scanner

A market scanner that identifies potential short squeeze candidates using:

- RSI (oversold conditions)
- Short interest %
- Days to cover

## Features

- REST API (`/scan`)
- Scoring engine
- Extensible data providers
- Scheduler support

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
