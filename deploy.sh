#!/bin/bash
#pip install -r requirements.txt & uvicorn main:app --reload 
pip install -r requirements.txt & gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0
