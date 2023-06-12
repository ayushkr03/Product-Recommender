#!/bin/bash
pip install -r requirements.txt

if [ $? -eq 0 ]
then
    uvicorn main:app --reload      #host=0.0.0.0 --port=8000 &
    #streamlit run myapp.py &
else
    echo "Failed to install dependencies"
fi
