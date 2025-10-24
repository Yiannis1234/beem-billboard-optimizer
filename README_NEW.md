# Ad Success Predictor - Organized Structure

A comprehensive billboard advertising success predictor for Manchester and London areas, featuring real-time weather and traffic data integration.

## 🎯 Features

- **Real-time Data Integration**: Live weather and traffic data from external APIs
- **Universal Dark/Light Mode**: Perfect visibility in both themes
- **Enhanced Traffic Analysis**: Detailed congestion levels, speed ratios, and density metrics
- **Comprehensive Weather Impact**: Visibility, temperature, precipitation, and wind effects
- **Organized Codebase**: Clean separation of backend and frontend logic
- **Responsive Design**: Mobile-friendly interface with modern styling

## 📁 Project Structure

```
beem-billboard-optimizer/
├── backend/                    # Backend logic and data
│   ├── __init__.py
│   ├── models.py              # Data models and area definitions
│   ├── api_services.py        # External API integrations
│   └── business_logic.py      # Core prediction algorithms
├── frontend/                   # Frontend components and styling
│   ├── __init__.py
│   ├── styles.py              # Universal CSS for light/dark mode
│   └── components.py           # Reusable UI components
├── app.py                     # Main Streamlit application
├── simple_ad_success.py      # Original monolithic file (backup)
├── test_app.py               # Comprehensive test suite
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yiannis1234/beem-billboard-optimizer.git
   cd beem-billboard-optimizer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Test the application:**
   ```bash
   python test_app.py
   ```

## 🏗️ Architecture Overview

### Backend (`backend/`)

#### `models.py`
- **Data Models**: Structured data classes for areas, weather, traffic, and results
- **AreaDatabase**: Comprehensive database of Manchester and London areas
- **Type Safety**: Full type hints and dataclass definitions

#### `api_services.py`
- **WeatherAPIService**: Integration with WeatherAPI.com
- **TrafficAPIService**: Integration with TomTom Traffic API
- **Robust Error Handling**: Fallback data when APIs are unavailable
- **Enhanced Metrics**: Speed ratios, congestion levels, traffic density

#### `business_logic.py`
- **AdSuccessCalculator**: Core prediction algorithms
- **Weather Adjustments**: Detailed weather impact calculations
- **Success Scoring**: 0-100 scoring system with multiple factors
- **Reason Generation**: Intelligent success reason explanations

### Frontend (`frontend/`)

#### `styles.py`
- **Universal CSS**: Works perfectly in both light and dark modes
- **CSS Variables**: Dynamic theme switching
- **Responsive Design**: Mobile-friendly layouts
- **Modern Styling**: Clean, professional appearance

#### `components.py`
- **UIComponents**: Reusable Streamlit components
- **Modular Design**: Separated UI logic for maintainability
- **Rich Visualizations**: Enhanced data presentation
- **Interactive Elements**: Dynamic content based on results

## 🔧 Key Improvements

### 1. Dark Mode Visibility ✅
- **Universal CSS Variables**: Automatic theme detection
- **Perfect Contrast**: All text and elements visible in both modes
- **Consistent Styling**: Unified appearance across all components

### 2. Enhanced Traffic API ✅
- **Detailed Metrics**: Speed ratios, congestion colors, traffic density
- **Better Error Handling**: Comprehensive fallback mechanisms
- **Real-time Status**: Live data indicators and timestamps
- **Visual Indicators**: Color-coded congestion levels (🟢🟡🟠🔴🛑)

### 3. Code Organization ✅
- **Separation of Concerns**: Clear backend/frontend division
- **Modular Design**: Reusable components and services
- **Type Safety**: Full type hints throughout
- **Maintainability**: Easy to extend and modify

### 4. Enhanced Data Presentation ✅
- **Rich Visualizations**: Better charts and metrics display
- **Interactive Elements**: Dynamic content based on results
- **Comprehensive Information**: Detailed weather and traffic impacts
- **Professional UI**: Modern, clean interface design

## 📊 Data Sources

### Weather Data
- **Provider**: WeatherAPI.com
- **Metrics**: Temperature, condition, visibility, wind, humidity, UV, precipitation
- **Update Frequency**: Real-time
- **Fallback**: Default values when API unavailable

### Traffic Data
- **Provider**: TomTom Traffic API
- **Metrics**: Current speed, free-flow speed, congestion level, traffic density
- **Update Frequency**: Real-time
- **Fallback**: Estimated values when API unavailable

## 🧪 Testing

The application includes a comprehensive test suite (`test_app.py`) that verifies:

- ✅ Backend module imports
- ✅ Frontend module imports
- ✅ Area database functionality
- ✅ API services integration
- ✅ Business logic calculations

Run tests with:
```bash
python test_app.py
```

## 🎨 UI Features

### Universal Theme Support
- **Automatic Detection**: Respects system theme preferences
- **CSS Variables**: Dynamic color switching
- **Perfect Visibility**: All elements visible in both modes

### Enhanced Components
- **Success Cards**: Color-coded based on performance level
- **Rich Metrics**: Detailed weather and traffic information
- **Interactive Tables**: Sortable area comparisons
- **Pro Tips**: Contextual advice based on results

### Mobile Responsive
- **Adaptive Layout**: Works on all screen sizes
- **Touch Friendly**: Optimized for mobile interaction
- **Fast Loading**: Optimized performance

## 🔄 Migration from Original

The original `simple_ad_success.py` file has been preserved as a backup. The new organized structure provides:

- **Better Maintainability**: Easier to modify and extend
- **Improved Performance**: Optimized imports and structure
- **Enhanced Features**: Better error handling and data presentation
- **Future-Proof**: Ready for additional features and integrations

## 🚀 Deployment

### Streamlit Cloud
The application is ready for deployment on Streamlit Cloud:

1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with `streamlit run app.py`

### Local Development
```bash
# Development mode with auto-reload
streamlit run app.py --server.runOnSave true
```

## 📈 Performance

- **Fast Loading**: Optimized imports and structure
- **Efficient APIs**: Smart caching and error handling
- **Responsive UI**: Smooth interactions and animations
- **Memory Efficient**: Clean data structures and lifecycle management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python test_app.py`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Weather Data**: Provided by [WeatherAPI.com](https://www.weatherapi.com/)
- **Traffic Data**: Provided by [TomTom](https://developer.tomtom.com/)
- **Framework**: Built with [Streamlit](https://streamlit.io/)

---

**🎯 Ready to predict ad success with confidence!** The application now features perfect dark mode visibility, enhanced traffic data presentation, and a beautifully organized codebase that's easy to maintain and extend.
