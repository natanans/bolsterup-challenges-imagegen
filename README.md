# Landmark Description and Image Generation Script

## Overview

This project is a script that takes the name of a landmark or famous building as input, fetches detailed descriptions and interesting information about it, and generates an AI-created image representing the landmark. The script utilizes NLP models for data retrieval and image generation tools like Replicate's API.

## Demo

**Try the Streamlit web application here:**

👉 [Live Demo on Streamlit Cloud](https://bolsterup-challenges-imagegen-ibh6bmmhum77zebs6mt3tq.streamlit.app/) 👈

*Note: The app might not load immediately on the first try due to free hosting limitations. If this happens, please refresh the page after a few moments.*

## Features

- **Landmark Information Retrieval**: Fetches descriptions, historical significance, architects, construction details, and other key information about a landmark using an NLP model.
- **Image Generation**: Generates visual representations of the landmark using an AI image generation model.
- **Easter Egg**: Includes a hidden feature to cartoonify the generated images.
- **Output Structure**: Stores the retrieved information in a formatted JSON file and displays the generated images along with the details.
- **Streamlit Web App**: Provides a user-friendly interface for input and displays results with an image carousel.

## Project Structure

```
project/
├── LICENSE
├── requirements.txt
├── CHANGELOG.md
├── streamlit_app.py
├── README.md
├── generated_images/
│   ├── 06ee41dbb03c4b198250326eca48f09c.jpg
│   ├── 
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── grok.py
│   │   └── replicate.py
│   └── text_to_image.py
└── tests/
    └── model_test.ipynb
```

- `streamlit_app.py`: Main Streamlit application file for the web interface.
- `src/`: Contains all the source code modules.
  - `text_to_image.py`: Main script that processes the landmark input.
  - `models/`: Contains model classes for data retrieval and image generation.
    - `grok.py`: Handles landmark information retrieval using the Groq API.
    - `replicate.py`: Manages image generation using Replicate's API.
- `generated_images/`: Directory where generated images are stored.
- `tests/`: Contains test scripts and notebooks.

## Requirements

- Python 3.x
- Packages:
  - `pydantic`
  - `typing`
  - `groq`
  - `requests`
  - `replicate`
  - `streamlit`
  - `Pillow`

## Installation

1. **Clone the Repository**

   ```bash
   git clone <natananshiferaw@gmail.com>
   cd project
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, install packages manually:*

   ```bash
   pip install pydantic typing groq requests replicate streamlit Pillow
   ```

3. **Set Up API Keys**

   - Obtain API keys for the following services:
     - **Groq**: For landmark information retrieval (NLP model).
     - **Replicate**: For image generation.
   - Set the API keys as environment variables:

     ```bash
     export LLMAPIKEY='your_groq_api_key'
     export REPLICATEAPIKEY='your_replicate_api_key'
     ```

## Usage

1. **Navigate to Project Directory**

   ```bash
   cd project
   ```

2. **Run the Streamlit App**

   ```bash
   streamlit run streamlit_app.py
   ```

   This will open the web application in your default browser.

3. **Use the Application**

   - Enter the name of a landmark in the input field.
   - Specify the number of images to generate.
   - Click on "Generate Images".
   - View the generated images in the carousel and download them if desired.
   - The landmark details will be displayed below the images.
   - You can also download the landmark details as a JSON file.

## How It Works

### Models Used

- **NLP Model**: Used for retrieving detailed information about the landmark, such as descriptions, historical facts, architects, etc.
- **Image Generation Model**: Used for creating AI-generated images of the landmark based on the retrieved information.

### `LandmarkProcessor` Class

- **Initialization**

  ```python
  processor = LandmarkProcessor(
      api_key=os.getenv('LLMAPIKEY'), 
      replicate_api_token=os.getenv('REPLICATEAPIKEY')
  )
  ```

- **Methods**

  - `process_landmark(landmark_name: str)`: Fetches landmark details and generates an image.

- **Easter Egg**

  - An easter egg is included that, when activated, will cartoonify the generated images.
  - To activate it, uncomment the following line in the `process_landmark()` method:

    ```python
    # landmark_name = landmark_name + ' make it cartoon and animated'
    ```

### Workflow

1. **Fetch Landmark Details**

   - Uses `LLMRetriever` to interact with the Groq API (NLP model).
   - Retrieves information like description, architects, construction year, materials, etc.
   - Validates and parses the data into a `LandmarkResponse` object.

2. **Generate Image**

   - Constructs an image generation prompt using the retrieved details.
   - Uses `ReplicateImageGenerator` to generate an image via the Replicate API (image generation model).
   - Saves the generated image in the `generated_images/` directory.

3. **Display Results**

   - The Streamlit app displays the images in a carousel using Swiper.js.
   - Landmark details are formatted and displayed below the images.
   - Provides options to download images and JSON data.

## Dependencies

- **pydantic**: Data validation and settings management.

  ```bash
  pip install pydantic
  ```

- **groq**: For interacting with the Groq API.

  ```bash
  pip install groq
  ```

- **replicate**: Client library for Replicate's API.

  ```bash
  pip install replicate
  ```

- **streamlit**: Web application framework for the front end.

  ```bash
  pip install streamlit
  ```

- **Pillow**: Image processing library.

  ```bash
  pip install Pillow
  ```

## Files Generated

- **Generated Images**: Saved in the `generated_images/` directory with unique filenames.
- **JSON Data**: Landmark details can be downloaded as `landmark_details.json`.

## Customization

- **Change Image Generation Model**

  Modify the `model` parameter in the `generate_image()` method of `ReplicateImageGenerator`:

  ```python
  output_path = self.generator.generate_image(
      model="your_model_name",
      input_params={
          "width": 1024,
          "height": 1024,
          "prompt": full_prompt
      }
  )
  ```

- **Adjust Prompt**

  Modify the prompt construction in the `process_landmark()` method of `LandmarkProcessor` to customize the image generation prompt.

- **Activate Easter Egg**

  To cartoonify the generated images, uncomment the following line in `process_landmark()`:

  ```python
  # landmark_name = landmark_name + ' make it cartoon and animated'
  ```

## Error Handling

- Implements retry logic for API calls with exponential backoff.
- Validates API responses and provides meaningful error messages.
- Handles exceptions during image generation and data retrieval.

## Note on Free Hosting

- The Streamlit app is hosted on a free tier, which might cause delays or require a page refresh if it doesn't load immediately.
- If you experience loading issues, please wait a moment and refresh the page.

## Contact

For any questions or suggestions, please contact [natananshiferaw@gmail.com](mailto:natananshiferaw@gmail.com).

## License

This project is licensed under the MIT License.

---

*Note: Replace `<natananshiferaw@gmail.com>` and `natananshiferaw@gmail.com` with the actual repository URL and your email address.*