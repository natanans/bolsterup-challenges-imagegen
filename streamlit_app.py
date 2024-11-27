import streamlit as st
from PIL import Image
#from your_image_generator import generate_image_text  # Import your custom method

# Title and Instructions
st.title("Image Generation from Text")
st.info("""
#### NOTE: 
1. You can download the generated image by right-clicking on it and selecting "Save image as."
2. Use the form below to generate images based on a text prompt.
3. JSON links and captions will be displayed along with the images.
""")

# Form for user input
with st.form(key='form'):
    prompt = st.text_input(label='Enter a text prompt for image generation')
    num_images = st.number_input('Enter the number of images to generate', min_value=1, max_value=5, value=1)
    submit_button = st.form_submit_button(label='Generate Images')

def generate_image_text():
    return "Asd"
# Generate and display images
if submit_button:
    if prompt:
        st.write(f"Generating {num_images} images for the prompt: **{prompt}**")

        for i in range(num_images):
            try:
                # Call your custom image generation function
                image_path, image_caption, json_link = generate_image_text(prompt, image_index=i)
                
                # Open and display the generated image
                image = Image.open(image_path)
                st.image(image, caption=f"{image_caption}", use_column_width=True)

                # Display JSON link and caption
                st.markdown(f"**Caption:** {image_caption}")
                st.markdown(f"**JSON Data Link:** [View JSON](file://{json_link})")

            except Exception as e:
                st.error(f"Error generating image {i + 1}: {e}")
    else:
        st.warning("Please enter a prompt to generate images.")