"""Simple AI-powered Streamlit app.

Sample code of a basic Streamlit app that interacts with Vertex AI
Google Cloud Generative models to generate and edit images.
"""
import os

import streamlit as st
import vertexai

# Import tabs
from sample_tabs.generate_images import main as generate_image_tab
from sample_tabs.edit_images import main as edit_image_tab

# Get PROJECT_ID and LOCATION from os.environ variables
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us_central1")

# Init Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Set Page Config
st.set_page_config(
    layout="wide",
    page_title="AI-Streamlit",
    page_icon=":robot:"
)

# Create tabs and navigation bar
tab1, tab2 = st.tabs(
    ["Generate images", "Background editing",]
)

with tab1:
  generate_image_tab()

with tab2:
  edit_image_tab()
