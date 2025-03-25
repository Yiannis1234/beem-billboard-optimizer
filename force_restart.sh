#!/bin/bash
# Kill ALL Streamlit processes
killall -9 streamlit
killall -9 python3

# Start app_code.py with Streamlit
streamlit run app_code.py 