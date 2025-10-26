# 📊 BritMetrics
## Billboard Intelligence Platform

**Go Beyond Generic Billboard Analytics** - Get campaign-specific recommendations tailored to YOUR brand, target audience, and real-time context.

Unlike JCDecaux and other generic location-based analytics, BritMetrics personalizes every insight based on your specific campaign type, target demographics, weather conditions, and area characteristics.

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

## Key Differentiators from JCDecaux

### What Makes Us Different:

1. **Campaign-Specific Targeting** - Not just location metrics, but personalized audience matching for YOUR brand
2. **Creative Recommendations** - Dynamic suggestions based on weather, demographics, and brand type
3. **Audience Match Scoring** - See exactly what % of viewers match your target demographic
4. **Tactical Campaign Tips** - Personalized strategies for maximizing ROI
5. **Context-Aware Insights** - Weather-responsive messaging and timing recommendations

## Using the Application

1. **Select Your Campaign Type**: Choose from 10+ campaign categories in the sidebar
2. **Choose Location**: Pick Manchester or London, then select an area
3. **Get Personalized Insights**:
   - Audience Match Score (how well the area matches YOUR target demographic)
   - Target Audience Size (YOUR demographic per hour, not just total footfall)
   - Creative Recommendations (weather & context-aware design tips)
   - Tactical Campaign Strategy (personalized ROI optimization tips)
4. **Compare Areas**: See rankings specific to YOUR campaign type

## API Keys

The application uses the following APIs:
- Weather data from [WeatherAPI.com](https://www.weatherapi.com/)
- Traffic data from [TomTom](https://developer.tomtom.com/)

## Deployment

The app is deployed on Streamlit Cloud at: [beem-billboard-optimizer](https://beem-billboard-optimizer-lvvnqjcpqucrxzvnhg3vc6.streamlit.app/)

## About BritMetrics

BritMetrics helps advertisers maximize campaign ROI through intelligent, brand-specific targeting and creative recommendations.

### Why We're Different from JCDecaux:

**JCDecaux and Traditional Providers:**
- ❌ Generic location-based metrics for everyone
- ❌ Same data regardless of your brand type
- ❌ No creative or messaging guidance
- ❌ One-size-fits-all recommendations

**Our Personalized Approach:**
- ✅ Campaign-specific audience matching
- ✅ Brand-tailored creative recommendations
- ✅ Weather-responsive messaging suggestions
- ✅ Target demographic isolation (not just total footfall)
- ✅ Tactical ROI optimization per campaign type
- 🌿 Eco-friendly bicycle-based billboards
- 💰 Cost-effective mobile advertising
- 🎯 Hyper-targeted based on YOUR audience

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