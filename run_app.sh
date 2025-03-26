#!/bin/bash

# Find and kill any existing Streamlit processes (but do it gracefully)
pkill -f "streamlit run"

# Wait a moment to make sure processes are terminated
sleep 2

# Run the Streamlit app in the background
streamlit run app_code.py
