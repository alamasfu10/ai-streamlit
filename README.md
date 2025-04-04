# AI-powered Streamlit App

##### _This code is created with educational purposes._

## Overview

Deploy and use your first AI-powered Streamlit App.

## Requirements
* **Python 3.x** 
* **pip**

## Deployment guide
After you have cloned the repository, you just have to follow these steps

### 1). Virtual Environment
```bash
python3 -m venv env
```

### 2). Activate your Virtual Environment
```bash
source env/bin/activate
```

### 3). Install your python dependencies
```bash
pip install -r requirements.txt
```

### 4). Set Up your Google Cloud variables
```bash
export GOOGLE_CLOUD_PROJECT='<Your Google Cloud Project ID>'  # Change this
export GOOGLE_CLOUD_REGION='us-central1' # If you change this, make sure the region is supported.
```

### 4). Run the Streamlit App
```bash
streamlit run main.py
```