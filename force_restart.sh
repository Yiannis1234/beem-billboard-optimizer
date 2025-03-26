#!/bin/bash

echo "Killing ALL Streamlit processes..."
pkill -9 -f "streamlit"
pkill -9 -f "app_code.py"

# Wait for processes to terminate
sleep 2

echo "Starting Streamlit app..."
echo "If changes are not showing, refresh your browser at http://130.88.226.18:8501"
streamlit run app_code.py 