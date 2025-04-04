"""Simple AI-powered Streamlit app.

Sample code of a basic Streamlit app that interacts with Vertex AI
Google Cloud Generative models to generate and edit images.
"""
import io
import os
import uuid

from PIL import Image

import streamlit as st
import vertexai
from vertexai.vision_models import Image as VertexImage
from vertexai.vision_models import ImageGenerationModel

# Get PROJECT_ID and LOCATION from os.environ variables
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us_central1")

# Init Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load generative AI models from Vertex AI
generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
edit_model = ImageGenerationModel.from_pretrained("imagegeneration@006")

# Set Page Config
st.set_page_config(
    layout="wide",
    page_title="AI-Streamlit",
    page_icon=":robot:"
)


# Function to delete existing images
def delete_previous_image(prefix="generated_image"):
  """Deletes all files starting with 'generated_image'."""
  for filename in os.listdir():
    if filename.startswith(prefix):
      os.remove(filename)


# Text-to-image generation function
def generate_image(prompt, counter):
  """Generates an image given a prompt'."""
  delete_previous_image()
  response = generation_model.generate_images(
      prompt=prompt,
      number_of_images=1,
      aspect_ratio="1:1",
      safety_filter_level="block_few",
      person_generation="allow_adult"
  )
  # print(response)
 
  if response.images:
    # Store the first image in the folder
    output_file = f"generated_image_{uuid.uuid4()}.png"
    response.images[0].save(
        location=output_file,
        include_generation_parameters=False
    )
    return Image.open(output_file)
  elif counter > 0:
    # If an error happens, retry the image generation request
    print("Retrying...")
    st.error("Retrying...")
    return generate_image(prompt, counter-1)
  else:
    return None


def edit_background_image(prompt, image, counter):
  """Edit an existing image given a prompt'."""
  delete_previous_image("edited_image")
  response = edit_model.edit_image(
      base_image=image,
      prompt=prompt,
      number_of_images=1,
      edit_mode="product-image",
  )

  # print(response)
  if response.images:
    # Store the first image in the folder
    output_file = f"edited_image_{uuid.uuid4()}.png"
    response.images[0].save(
        location=output_file,
        include_generation_parameters=False
    )
    return Image.open(output_file)
  elif counter > 0:
    # If an error happens, retry the image edition request
    print("Retrying...")
    st.error("Retrying...")
    return generate_image(prompt, counter-1)
  else:
    return None


def generate_image_tab():
  """UI definition for the Image Genertion."""
  st.title("AI-Streamlit: Generate an image")

  # 2-columns layout
  col1, col2 = st.columns(2)

  # 1st column: generate image
  with col1:
    st.header("Bring your creativity!")
    prompt = st.text_area("Enter your prompt:", height=100)
    if st.button("Generate Image"):
      with st.spinner("Generating image..."):
        generated_image = generate_image(prompt, 10)
        if generated_image:
          st.success("Image generated successfully!")
          
          # 2nd column: display the generated image
          with col2:
            st.image(
                generated_image,
                caption="Generated Image",
                use_container_width=True
            )
        else:
          st.error("Failed to generate image. Try again")


def edit_image_tab():
  """UI definition for the Image Edition."""
  st.title("Prompt Wars: Edit the background of the image")

  # 2-columns layout
  col1, col2 = st.columns(2)

  # 1st column: upload an image
  with col1:
    st.header("Upload the image to edit")
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
      # To read file as bytes:
      bytes_data = uploaded_file.getvalue()

      # To convert to a PIL Image object:
      image = Image.open(io.BytesIO(bytes_data))

      # Display the image:
      st.image(image, caption="Uploaded Image.", use_container_width=True)

      # Create a Vertex AI Image object
      base_img = VertexImage(image_bytes=bytes_data)

      # 2nd column: edit the image
      with col2:
        st.header("Enter the prompt to edit the background")
        prompt = st.text_area("Prompt:", height=75)
        if st.button("Edit Image"):
          with st.spinner("Editing image..."):
            edited_image = edit_background_image(prompt, base_img, 10)
            if edited_image:
              with col2:
                st.image(
                    edited_image,
                    caption="Edited Image",
                    use_container_width=True
                )
            else:
              st.error("Failed to generate image. Try again")


# Create tabs and navigation bar
tab1, tab2 = st.tabs(
    ["Generate images", "Background editing",]
)

with tab1:
  generate_image_tab()

with tab2:
  edit_image_tab()
