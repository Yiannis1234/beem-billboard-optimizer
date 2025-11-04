"""
CSS styling for the Ad Success Predictor application.
Provides universal light and dark mode compatibility.
"""

UNIVERSAL_CSS = """
<style>
    /* Root variables for theme switching */
    :root {
        --primary-color: #00d4aa;
        --primary-dark: #00b894;
        --secondary-color: #0066cc;
        --text-primary: #2d3436;
        --text-secondary: #636e72;
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --border-color: #e9ecef;
        --shadow: rgba(0,0,0,0.1);
    }

    /* Dark mode variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-primary: #ffffff;
            --text-secondary: #b2bec3;
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --border-color: #404040;
            --shadow: rgba(255,255,255,0.1);
        }
    }

    /* Force dark mode detection and apply styles */
    .stApp {
        background-color: var(--bg-secondary) !important;
    }

    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--secondary-color);
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Card styling with perfect visibility */
    .success-card {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px var(--shadow);
    }
    .success-card h2, .success-card h3, .success-card p { color: white !important; }
    .success-card .metric-highlight { color: white !important; }

    .warning-card {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px var(--shadow);
    }
    .warning-card h2, .warning-card h3, .warning-card p { color: white !important; }
    .warning-card .metric-highlight { color: white !important; }

    .danger-card {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px var(--shadow);
    }
    .danger-card h2, .danger-card h3, .danger-card p { color: white !important; }
    .danger-card .metric-highlight { color: white !important; }

    /* Reason box with theme-aware styling */
    .reason-box {
        background: var(--bg-primary);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid var(--primary-color);
        margin: 0.5rem 0;
        color: var(--text-primary) !important;
        box-shadow: 0 2px 4px var(--shadow);
        border: 1px solid var(--border-color);
    }
    .reason-box strong { color: var(--text-primary) !important; }

    /* Metric highlight styling */
    .metric-highlight {
        font-size: 2rem;
        font-weight: bold;
        color: white !important;
    }

    /* Universal text visibility fixes */
    .main .block-container { 
        color: var(--text-primary) !important; 
        background: transparent !important; 
    }
    .main .block-container p, 
    .main .block-container h1, h2, h3, h4, h5, h6,
    .main .block-container div, 
    .main .block-container span, 
    .main .block-container label { 
        color: var(--text-primary) !important; 
    }

    /* Selectbox styling */
    .stSelectbox label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        margin-bottom: 0.35rem !important;
    }
    .stSelectbox div {
        color: var(--text-primary) !important;
    }
    .stSelectbox > div > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] > div {
        background-color: var(--bg-primary) !important;
        border: 2px solid #0078FF !important;
        border-radius: 10px !important;
        min-height: 48px !important;
        padding: 6px 12px !important;
        box-shadow: 0 4px 10px rgba(0, 120, 255, 0.12) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-baseweb="select"]:hover > div {
        border-color: #00d4aa !important;
        box-shadow: 0 6px 14px rgba(0, 212, 170, 0.18) !important;
    }
    div[data-baseweb="select"]:focus-within > div {
        border-color: #00d4aa !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.25) !important;
    }
    div[data-baseweb="select"] span {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] svg {
        color: #0078FF !important;
        width: 22px !important;
        height: 22px !important;
    }
    div[role="listbox"] {
        background-color: var(--bg-primary) !important;
        border: 2px solid #0078FF !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 30px rgba(0, 120, 255, 0.2) !important;
        padding: 4px !important;
    }
    div[role="option"] {
        color: var(--text-primary) !important;
        border-radius: 6px !important;
        padding: 10px !important;
    }
    div[role="option"]:hover {
        background: rgba(0, 120, 255, 0.12) !important;
    }

    /* Button styling */
    .stButton button { 
        color: white !important; 
        background-color: var(--primary-color) !important; 
        border: none !important;
    }

    /* Metric containers */
    .stMetric, 
    .stMetric label, 
    .stMetric div { 
        color: var(--text-primary) !important; 
    }

    div[data-testid="metric-container"] {
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important; 
        padding: 1rem !important;
    }
    div[data-testid="metric-container"] div, 
    div[data-testid="metric-container"] label, 
    div[data-testid="metric-container"] span { 
        color: var(--text-primary) !important; 
    }

    /* Data table styling */
    .stDataFrame { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
        border: 2px solid var(--primary-color) !important; 
        border-radius: 10px !important; 
    }
    .stDataFrame table { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
    }
    .stDataFrame th { 
        background-color: var(--primary-color) !important; 
        color: white !important; 
        font-weight: bold !important; 
        padding: 12px !important; 
    }
    .stDataFrame td { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
        padding: 10px !important; 
        border-bottom: 1px solid var(--border-color) !important; 
    }
    .stDataFrame tr:nth-child(even) { 
        background-color: var(--bg-secondary) !important; 
    }
    .stDataFrame tr:hover { 
        background-color: rgba(0, 212, 170, 0.1) !important; 
    }

    /* Alert boxes */
    .stAlert {
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 25px var(--shadow) !important;
    }
    .stAlert > div { 
        color: var(--text-primary) !important; 
    }

    /* Success, info, warning, error alerts */
    .stSuccess {
        background-color: rgba(0, 212, 170, 0.1) !important;
        border-left: 4px solid var(--primary-color) !important;
        color: var(--text-primary) !important;
    }
    .stInfo {
        background-color: rgba(0, 102, 204, 0.1) !important;
        border-left: 4px solid var(--secondary-color) !important;
        color: var(--text-primary) !important;
    }
    .stWarning {
        background-color: rgba(253, 203, 110, 0.1) !important;
        border-left: 4px solid #fdcb6e !important;
        color: var(--text-primary) !important;
    }
    .stError {
        background-color: rgba(253, 121, 168, 0.1) !important;
        border-left: 4px solid #fd79a8 !important;
        color: var(--text-primary) !important;
    }

    /* Container backgrounds */
    .main { 
        background-color: var(--bg-secondary) !important; 
    }
    .element-container, 
    .stColumn { 
        background-color: transparent !important; 
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stDataFrame { 
            border-radius: 12px; 
            font-size: 0.9rem; 
        }
        .stDataFrame th, 
        .stDataFrame td { 
            padding: 0.6rem 0.8rem; 
        }
        .stAlert { 
            padding: 1.2rem; 
            border-radius: 12px; 
        }
        .main-header {
            font-size: 2rem;
        }
    }

    /* Force visibility for all text elements */
    * {
        color: inherit;
    }
    
    /* Override any Streamlit default colors */
    .stApp > div {
        color: var(--text-primary) !important;
    }
    
    /* Ensure all headings are visible */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    /* Ensure all paragraphs are visible */
    p {
        color: var(--text-primary) !important;
    }
    
    /* Ensure all labels are visible */
    label {
        color: var(--text-primary) !important;
    }
</style>
"""
