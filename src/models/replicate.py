import os
import replicate
import uuid  # For generating unique filenames


class ReplicateImageGenerator:
    def __init__(self, api_token: str):
        """
        Initialize the ReplicateImageGenerator with an API token.
        """
        self.api_token = api_token
        os.environ["REPLICATE_API_TOKEN"] = self.api_token
        self.client = replicate.Client(api_token=self.api_token)
        self.output_dir = "generated_images"
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_image(self, model: str, input_params: dict):
        """
        Generate an image using the specified model and input parameters.

        Args:
            model (str): The model ID to use for generation.
            input_params (dict): Input parameters for the model.

        Returns:
            str: Path of the saved image file.
        """
        try:
            # Run the model
            output = self.client.run(model, input=input_params)

            # Generate a unique filename
            filename = f"{uuid.uuid4().hex}.jpg"
            output_file = os.path.join(self.output_dir, filename)

            # Save the output image in the generated_images directory
            with open(output_file, "wb") as file:
                file.write(output.read())

            print(f"Image saved as {output_file}")
            return output_file
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

