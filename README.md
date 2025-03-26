# Beem Billboard Route Optimizer

This application helps optimize bicycle routes for Beem's mobile billboards in Manchester. Get real-time weather, traffic, and pedestrian data to maximize engagement and plan your routes efficiently.

## Setup and Installation

### Prerequisites
- Python 3.9 or higher
- pip or conda package manager

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/Yiannis1234/beem-billboard-optimizer.git
   cd beem-billboard-optimizer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the application

**Option 1: Using the run script (recommended)**
```
./run_app.sh
```

**Option 2: Running directly with Streamlit**
```
streamlit run app_code.py
```

## Troubleshooting

If you encounter issues running the app:

1. **Missing modules error**: Make sure you've installed all dependencies
   ```
   pip install -r requirements.txt
   ```

2. **Port already in use**: Kill any existing Streamlit processes
   ```
   pkill -f "streamlit run"
   ```

3. **Streamlit command not found**: Make sure Streamlit is properly installed and your environment is activated
   ```
   pip install streamlit
   ```

## Using the Application

1. **Open the sidebar**: Click the ">" button in the top-left corner
2. **Select area**: Choose an area from the dropdown in the sidebar
3. **Set time options**: Choose current time or custom time
4. **Analyze**: Click the "ANALYZE ROUTE" button to see results
5. **View data**: Navigate through tabs to see different analyses

## API Keys

The application uses the following APIs:
- Weather data from [WeatherAPI.com](https://www.weatherapi.com/)
- Traffic data from [TomTom](https://developer.tomtom.com/)

## Deployment

The app is deployed on Streamlit Cloud at: [beem-billboard-optimizer](https://beem-billboard-optimizer-lvvnqjcpqucrxzvnhg3vc6.streamlit.app/)

## About

Beem Billboard Route Optimizer helps businesses optimize mobile billboard routes for maximum engagement through eye-catching billboards carried by cyclists.

Our solution is:
- 🌿 Eco-friendly
- 💰 Cost-effective
- 🎯 Highly targeted
- 📱 Engaging
- 📊 Data-driven

A web application that helps optimize bike routes for Beem's mobile billboards in Manchester, UK. The application uses real-time weather and traffic data to provide recommendations for the most effective routes and times for billboard display.

![Beem Billboard Bike Route Optimizer Screenshot](https://raw.githubusercontent.com/your-username/beem-billboard-optimizer/main/static/screenshot.png)

## Features

- **Real-time Data**: Get up-to-date weather conditions and traffic data for different areas of Manchester
- **Pedestrian Density Estimation**: AI-powered predictions of pedestrian activity based on time, location, and conditions
- **Engagement Scoring**: Calculate an engagement score to determine the effectiveness of billboard displays
- **Best Times Analysis**: View recommended times with highest potential engagement for each area
- **Interactive Map**: Visualize routes on an interactive map
- **Historical Patterns**: View engagement trends over time

## Areas Covered

- Northern Quarter
- City Centre
- Ancoats
- Piccadilly

## Technology Stack

- Streamlit for the web application
- Python for data processing and analysis
- WeatherAPI.com for real-time weather data
- TomTom Traffic API for real-time traffic conditions
- Pandas for data manipulation
- NumPy for numerical operations

## Live Demo

The application is deployed and can be accessed at:
[https://beem-billboard-optimizer.streamlit.app/](https://beem-billboard-optimizer.streamlit.app/)

## Local Development

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Configuration

The application uses the following environment variables:
- `WEATHER_API_KEY`: API key for accessing weather data
- `TRAFFIC_API_KEY`: API key for accessing traffic data

These are configured in the application directly, but can be overridden using environment variables or a `.streamlit/secrets.toml` file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Weather data provided by [WeatherAPI.com](https://www.weatherapi.com/)
- Traffic data provided by [TomTom](https://developer.tomtom.com/)
- Streamlit for the amazing framework 