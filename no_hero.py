import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Beem Billboard Optimizer", 
    page_icon="📢", 
    layout="wide", 
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar on mobile
)

# Show all components except the hero container
st.write('## The orange hero container has been removed!')

# Run the normal app
exec(open('app_code.py').read())
