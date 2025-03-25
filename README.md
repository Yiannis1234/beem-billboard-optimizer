# Beem Billboard Route Optimizer

## How to Run the App

**Important**: Always use the `app_code.py` file to run the application, not `app.py`:

```bash
# Option 1: Run directly
streamlit run app_code.py

# Option 2: Use the provided script
./run_app.sh

# Option 3: If the app gets stuck, use the restart script
./restart_app.sh
```

If you encounter any issues with the app not showing the latest changes, make sure you're running the correct file and try using the restart script.

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