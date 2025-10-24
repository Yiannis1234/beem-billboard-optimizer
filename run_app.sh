#!/bin/bash

# Ad Success Predictor - Run Script
# This script runs the organized application

echo "🎯 Starting Ad Success Predictor..."
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📦 Installing required dependencies..."
    pip install -r requirements.txt
fi

# Run tests first
echo "🧪 Running tests..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed! Starting application..."
    echo "🌐 The app will open in your browser at http://localhost:8501"
    echo ""
    
    # Run the application
    streamlit run app.py
else
    echo "❌ Tests failed. Please check the errors above."
    exit 1
fi
