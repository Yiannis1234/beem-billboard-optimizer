#!/bin/bash

# Kill any existing Streamlit processes
pkill -f "streamlit run"

# Function to restart the app
restart_app() {
  echo "🔄 Changes detected! Restarting app..."
  
  # Kill existing Streamlit processes
  pkill -f "streamlit run" 2>/dev/null
  
  # Wait a moment for process to terminate
  sleep 1
  
  # Start Streamlit in the background
  streamlit run app_code.py &
  
  # Store the PID
  APP_PID=$!
  
  echo "✅ App restarted! PID: $APP_PID"
  echo "📱 View at: http://130.88.226.18:8501"
  echo "📝 Watching for changes in app_code.py..."
}

# Initial start
restart_app

# Watch for changes to app_code.py
echo "👀 Watching for changes to app_code.py..."
echo "✏️ Edit app_code.py in any text editor, and I'll auto-restart the app"
echo "🔍 To exit, press Ctrl+C"

# Keep checking for changes
LAST_MODIFIED=$(stat -f "%m" app_code.py)

while true; do
  CURRENT_MODIFIED=$(stat -f "%m" app_code.py)
  
  # If modification time changed, restart the app
  if [ "$CURRENT_MODIFIED" != "$LAST_MODIFIED" ]; then
    LAST_MODIFIED=$CURRENT_MODIFIED
    restart_app
  fi
  
  # Check every second
  sleep 1
done 