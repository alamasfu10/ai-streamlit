# Import required dependencies
from google.cloud import storage
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import Part


# TODO: Get PROJECT_ID and LOCATION from os.environ variables

# TODO: Set up Google Cloud Configuration configuration
GCS_BUCKET_NAME = "<your_gcs_bucket>"
GCS_BUCKET_PATH = "streamlit_app/exercise_audio_files"

# TODO: Initialize vertexai

# TODO: Initialize GenerativeModel "gemini-2.0-flash-lite"


# Auxuliar function to store a file in GCS
def store_in_gcs(audio_file):
  storage_client = storage.Client()
  gcs_path = f"{GCS_BUCKET_PATH}/{audio_file.name}"
  blob = storage_client.bucket(GCS_BUCKET_NAME).blob(gcs_path)
  blob.upload_from_file(audio_file)


# TODO: Define function to send Gemini a prompt and an audio file
def ask_gemini(audio_file, prompt):
  # Hint: check the Part.from_uri and the generate_content(contents) functions
  return ""


# Streamlit UI part

# TODO: Create a title for your App

# TODO: Create a file uploader to uploade your audio file

# TODO: Display your audio file
# Hint: Check Streamlit st.audio

# TODO: Upload your audio file to GCS
# Hint: just call store_in_gcs(uploaded_file)

# TODO: Add a prompt text area

# TODO: Add a button to send the prompt and the audio to Gemini
# Hint: you should call the ask_gemini function

# TODO: Write the Gemini Response
