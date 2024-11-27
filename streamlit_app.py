import streamlit as st
from PIL import Image
import os

# Import your LandmarkProcessor class
from src.text_to_image import LandmarkProcessor  # Replace 'your_module' with the actual module name

# Initialize the LandmarkProcessor with your API keys
processor = LandmarkProcessor(api_key = os.getenv('LLMAPIKEY'), replicate_api_token = os.getenv('REPLICATEAPIKEY'))

# Title and Instructions
st.title("Image Generation from Text")
st.info("""
#### NOTE: 
1. You can download the generated image by right-clicking on it and selecting "Save image as."
2. Use the form below to generate images based on a text prompt.
3. JSON data will be displayed alongside the images.
""")

# Form for user input
with st.form(key='form'):
    prompt = st.text_input(label='Enter a text prompt for image generation')
    num_images = st.number_input('Enter the number of images to generate', min_value=1, max_value=5, value=1)
    submit_button = st.form_submit_button(label='Generate Images')

# Generate and display images
if submit_button:
    if prompt:
        st.write(f"Generating {num_images} image(s) for the prompt: **{prompt}**")

        # Add a loading spinner
        with st.spinner('Generating images...'):
            for i in range(num_images):
                try:
                    # Call the LandmarkProcessor to generate the image and get JSON data
                    image_path, landmark_details = processor.process_landmark(prompt)

                    # Open and display the generated image
                    image = Image.open(image_path)

                    # Extract the image caption from landmark details
                    image_caption = "image_caption"#landmark_details.get('image_generation_prompt', f"Image {i + 1}")

                    # Display image and JSON side by side
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(image, caption=image_caption, use_column_width=True)
                    with col2:
                        st.subheader("Landmark Details")
                        st.json(landmark_details)

                except Exception as e:
                    st.error(f"Error generating image {i + 1}: {e}")
    else:
        st.warning("Please enter a prompt to generate images.")