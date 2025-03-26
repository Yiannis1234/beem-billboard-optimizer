#!/bin/bash

# Check if a new text is provided
if [ -z "$1" ]; then
  echo "Please provide the new banner text."
  echo "Usage: ./direct_edit.sh \"YOUR NEW TEXT HERE\""
  exit 1
fi

NEW_TEXT="$1"
echo "Updating banner text to: $NEW_TEXT"

# Kill any running Streamlit processes
pkill -9 -f "streamlit"
sleep 1

# Find and replace the banner text in app_code.py
sed -i '' "s/PRESS TOP LEFT TO ANALYZE YOUR.*👈/PRESS TOP LEFT TO ANALYZE YOUR $NEW_TEXT 👈/g" app_code.py

echo "✅ Banner text updated to: $NEW_TEXT"

# Start Streamlit with the new changes
echo "🚀 Starting app with new text..."
streamlit run app_code.py 