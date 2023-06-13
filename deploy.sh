#!/bin/bash
#pip install -r requirements.txt & uvicorn main:app --reload 
pip install -r requirements.txt & python -m streamlit run myapp.py --server.port 8000 --server.address 0.0.0.0
