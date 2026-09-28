"""Run: python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000"""
import logging
from fastapi import FastAPI
from src.api.routes import router
logging.basicConfig(level=logging.INFO)
app=FastAPI(title='MedTrace AI',version='0.1.0',description='Medical-device investigation research prototype. Human regulatory decisions required.')
app.include_router(router)
