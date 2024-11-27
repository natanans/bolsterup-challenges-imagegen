import os
import streamlit as st
from PIL import Image
import base64
import io
from src.text_to_image import LandmarkProcessor

# Initialize the LandmarkProcessor with API keys
processor = LandmarkProcessor(
    api_key=os.getenv('LLMAPIKEY'), 
    replicate_api_token=os.getenv('REPLICATEAPIKEY')
)

# Title and Instructions
st.title("Image Generation from Text")
st.info("""
#### NOTE: 
1. Use the form below to generate AI-created images of landmarks by entering the name of the landmark.
2. The generated images can be downloaded by right-clicking on them and selecting "Save image as."
3. A carousel will display the AI-generated images alongside their captions.
4. Landmark details, generated using an LLM, will be displayed below the carousel.
""")

# Form for user input
with st.form(key='form'):
    prompt = st.text_input('Enter a text prompt for image generation')
    num_images = st.number_input('Enter the number of images to generate', min_value=1, max_value=5, value=1)
    submit_button = st.form_submit_button('Generate Images')

# Generate and display images
if submit_button:
    if prompt:
        st.write(f"Generating {num_images} image(s) for the prompt: **{prompt}**")

        with st.spinner('Generating images...'):
            images, captions, json_data_list = [], [], []

            for i in range(num_images):
                try:
                    image_path, landmark_json = processor.process_landmark(prompt)
                    image = Image.open(image_path)
                    images.append(image)

                    captions.append(landmark_json.get('image_generation_prompt', f"Image {i + 1}"))
                    json_data_list.append(landmark_json)

                except Exception as e:
                    st.error(f"Error generating image {i + 1}: {e}")

        # Display images in a carousel if generated
        if images:
            # Swiper.js CSS and JS
            swiper_css = '''
            <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />
            <style>
                .swiper-container { width: 100%; height: 1100px; margin: 0; padding: 0; }
                .swiper-slide {
                    text-align: center; font-size: 18px; background: #fff;
                    display: flex; flex-direction: column; justify-content: center; align-items: center;
                }
                .swiper-slide img { width: 100%; height: 100%; object-fit: cover; }
                .carousel-caption {
                    background: rgba(0,0,0,0.7); color: #fff; padding: 10px;
                    text-align: center; font-size: 24px;
                }
            </style>
            '''
            swiper_js = '''
            <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
            <script>
                var swiper = new Swiper('.swiper-container', {
                    loop: true,
                    pagination: { el: '.swiper-pagination', clickable: true },
                    navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' }
                });
            </script>
            '''

            # Generate carousel HTML
            html_code = '<div class="swiper-container"><div class="swiper-wrapper">'
            for idx, (img, caption) in enumerate(zip(images, captions)):
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                html_code += f'''
                <div class="swiper-slide">
                    <img src="data:image/png;base64,{img_str}" alt="{caption}">
                    <div class="carousel-caption">{caption}</div>
                </div>
                '''
            html_code += '</div><div class="swiper-pagination"></div><div class="swiper-button-next"></div><div class="swiper-button-prev"></div></div>'

            # Combine HTML, CSS, and JS
            full_html = f"{swiper_css}{html_code}{swiper_js}"

            st.components.v1.html(full_html, height=1150)

            # Display landmark details
            if json_data_list:
                st.subheader("Landmark Details")
                formatted_text = "\n\n".join(
                    f"**{key.capitalize()}**: {value}" 
                    for key, value in json_data_list[0].items() if key != "error"
                )
                st.markdown(formatted_text)
        else:
            st.error("No images were generated.")
    else:
        st.warning("Please enter a prompt to generate images.")