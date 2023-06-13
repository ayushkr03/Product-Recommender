#!/bin/bash
#pip install -r requirements.txt & uvicorn main:app --reload 
pip install -r requirements.txt & streamlit run myapp.py --server.port 80 --server.address 0.0.0.0
