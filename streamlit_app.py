import streamlit as st
from PIL import Image
import base64
import io
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
            images = []
            captions = []
            json_data_list = []
            for i in range(num_images):
                try:
                    # Call the LandmarkProcessor to generate the image and get JSON data
                    image_path, landmark_json = processor.process_landmark(prompt)

                    # Open and store the generated image
                    image = Image.open(image_path)
                    images.append(image)

                    # Extract the image caption from landmark details
                    image_caption = landmark_json.get('image_generation_prompt', f"Image {i + 1}")
                    captions.append(image_caption)
                    json_data_list.append(landmark_json)

                except Exception as e:
                    st.error(f"Error generating image {i + 1}: {e}")

        # After generating all images, build the carousel
        if images:
            # Build the HTML for the carousel using Swiper.js
            # Include Swiper.js CSS and JS
            swiper_css = '''
            <link
              rel="stylesheet"
              href="https://unpkg.com/swiper/swiper-bundle.min.css"
            />
            <style>
            .swiper-container {
                width: 100%;
                height: 500px;
            }
            .swiper-slide {
                text-align: center;
                font-size: 18px;
                background: #fff;

                /* Center slide text vertically */
                display: -webkit-box;
                display: -ms-flexbox;
                display: -webkit-flex;
                display: flex;
                -webkit-box-pack: center;
                -ms-flex-pack: center;
                -webkit-justify-content: center;
                justify-content: center;
                -webkit-box-align: center;
                -ms-flex-align: center;
                -webkit-align-items: center;
                align-items: center;
                position: relative;
            }
            .swiper-slide img {
                width: 100%;
                height: auto;
            }
            .carousel-caption {
                position: absolute;
                bottom: 10px;
                left: 0;
                right: 0;
                text-align: center;
                color: #fff;
                background: rgba(0,0,0,0.5);
                padding: 10px;
            }
            </style>
            '''
            swiper_js = '''
            <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
            <script>
            var swiper = new Swiper('.swiper-container', {
              loop: true,
              pagination: {
                el: '.swiper-pagination',
                clickable: true,
              },
              navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
              },
            });
            </script>
            '''

            # Build the HTML code for the carousel
            html_code = '''
            <div class="swiper-container">
                <div class="swiper-wrapper">
            '''
            for idx, (img, caption) in enumerate(zip(images, captions)):
                # Convert image to base64
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                html_code += f'''
                <div class="swiper-slide">
                    <img src="data:image/png;base64,{img_str}" alt="{caption}">
                    <div class="carousel-caption">
                        <h3>{caption}</h3>
                    </div>
                </div>
                '''

            html_code += '''
                </div>
                <!-- Add Pagination -->
                <div class="swiper-pagination"></div>
                <!-- Add Navigation -->
                <div class="swiper-button-next"></div>
                <div class="swiper-button-prev"></div>
            </div>
            '''

            # Combine everything
            full_html = f'''
            {swiper_css}
            {html_code}
            {swiper_js}
            '''

            # Display the carousel and JSON data side by side
            col1, col2 = st.columns(2)
            with col1:
                st.components.v1.html(full_html, height=600)
            with col2:
                st.subheader("Landmark Details")
                # Display JSON data for each image
                for idx, landmark_json in enumerate(json_data_list):
                    st.markdown(f"**Details for Image {idx + 1}:**")
                    st.json(landmark_json)
        else:
            st.error("No images were generated.")

    else:
        st.warning("Please enter a prompt to generate images.")
        