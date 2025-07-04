"""Tab of the main ST app to edit an uploaded image."""
import io
import os
import uuid

from PIL import Image
import streamlit as st
from vertexai.preview.vision_models import Image as VertexImage
from vertexai.vision_models import ImageGenerationModel


# Get edit model from pretrained models
edit_model = ImageGenerationModel.from_pretrained("imagegeneration@006")


# Function to delete existing images
def delete_previous_image(prefix="generated_image"):
  """Deletes all files starting with 'generated_image'."""
  for filename in os.listdir():
    if filename.startswith(prefix):
      os.remove(filename)


def edit_background_image(prompt, image, product_position, counter=10):
  """Edit an existing image given a prompt'."""
  delete_previous_image("edited_image")
  response = edit_model.edit_image(
      base_image=image,
      prompt=prompt,
      number_of_images=1,
      edit_mode="product-image",
      product_position=product_position  # "reposition / fixed"
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
    return edit_background_image(prompt, image, product_position, counter-1)
  else:
    return None


# ------ STREAMLIT UI/UX CODE ---------
def main():
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

        # Create a radio button selector
        product_position = st.radio(
            "Defines whether the subject should stay fixed or be repositioned (modifying its size and positioning in the image):",
            ("reposition", "fixed"),
            index=0,  # Optional: Sets "fixed" as the default selected option\
        )

        if st.button("Edit Image"):
          with st.spinner("Editing image..."):
            edited_image = edit_background_image(prompt, base_img, product_position)
            if edited_image:
              with col2:
                st.image(
                    edited_image,
                    caption="Edited Image",
                    use_container_width=True
                )
            else:
              st.error("Failed to generate image. Try again")
