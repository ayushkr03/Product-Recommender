#!/bin/bash
#pip install -r requirements.txt & uvicorn main:app --reload 
pip install -U pip & pip install -r requirements.txt --upgrade & gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0
