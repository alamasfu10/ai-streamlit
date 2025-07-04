"""Tab of the main ST app to generate a new image."""
import os
from PIL import Image
import streamlit as st
import uuid
from vertexai.vision_models import ImageGenerationModel


# Get the image generation model
generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")


# Function to delete existing images
def delete_previous_image(prefix="generated_image"):
  """Deletes all files starting with 'generated_image'."""
  for filename in os.listdir():
    if filename.startswith(prefix):
      os.remove(filename)

# Text-to-image generation function
def generate_image(prompt, aspect_ratio, counter=10):
  """Generates an image given a prompt'."""
  delete_previous_image()
  response = generation_model.generate_images(
      prompt=prompt,
      number_of_images=1,
      aspect_ratio=aspect_ratio,
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


# ------ STREAMLIT UX/UI ------
def main():
  """UI definition for the Image Genertion."""
  st.title("AI-Streamlit: Generate an image")

  # 2-columns layout
  col1, col2 = st.columns(2)

  # 1st column: generate image
  with col1:
    st.header("Bring your creativity!")
    prompt = st.text_area("Enter your prompt:", height=100)

    aspect_ratios = ("1:1", "16:9", "9:16") # The tuple of available aspect ratios
    aspect_ratio = st.selectbox(
        "Choose Aspect Ratio:",
        aspect_ratios,
        index=0,  # Default to "9:16" (first item in the tuple)
    )
    if st.button("Generate Image"):
      with st.spinner("Generating image..."):
        generated_image = generate_image(
            prompt,
            aspect_ratio
        )
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
