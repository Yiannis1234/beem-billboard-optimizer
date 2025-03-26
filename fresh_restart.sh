#!/bin/bash

# Kill all running streamlit processes
pkill -f streamlit

# Wait a moment to ensure everything is properly shut down
sleep 2

# Start the Streamlit app with new API keys
streamlit run app_code.py 