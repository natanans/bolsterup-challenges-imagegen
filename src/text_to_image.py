import json

from .models import LLMRetriever, ReplicateImageGenerator



class LandmarkProcessor:
    """
    A class to handle both landmark information retrieval and image generation.
    """
    def __init__(self, api_key:  str, replicate_api_token: str):
        """
        Initialize the LandmarkProcessor with API keys for LLMRetriever and ReplicateImageGenerator.
        """
    
        self.retriever = LLMRetriever(api_key)
        self.generator = ReplicateImageGenerator(api_token=replicate_api_token)

    def process_landmark(self, landmark_name: str) -> str:
        """
        Fetch landmark details and generate an image based on the retrieved details.

        Args:
            landmark_name (str): The name of the landmark.

        Returns:
            str: Path to the generated image.
        
        Raises:
            ValueError: If an error exists in the landmark retrieval response.
        """
        # Fetch landmark details
        landmark_details = self.retriever.fetch_landmark_details(landmark_name)

        # Convert landmark details to JSON
        landmark_json = json.loads(landmark_details.model_dump_json(indent=4))

       # Check for errors in the response
        if "error" in landmark_json:
            error_message = landmark_json.get("error")
            if error_message:
                raise ValueError(f"Error fetching landmark details: {error_message}")

        # Check for 'no_value' in more than one key to check for available model data on landmark
        no_value_count = sum(1 for key, value in landmark_json.items() if value == 'no_value')
        if no_value_count > 1:
            raise ValueError(
                "Error fetching landmark details: Multiple essential details are missing, possibly because the LLM model "
                "is not trained on sufficient data for this landmark or the information is unavailable. "
                "Please revise your input prompt to provide more specific or widely recognized details about the landmark "
                "to improve the response and support image generation."
            )

        # Build the image generation prompt using all relevant keys
        prompt_parts = [
            f"Description: {landmark_json.get('description', 'No description available.')}",
            f"Architects: {landmark_json.get('architects', 'No architects available.')}",
            f"Construction Year: {landmark_json.get('construction_year', 'No year available.')}",
            f"Materials: {landmark_json.get('materials', 'No materials available.')}",
            f"Interesting Facts: {landmark_json.get('interesting_facts', 'No facts available.')}",
            f"Dimensions: {landmark_json.get('dimensions', 'No dimensions available.')}",
            f"Construction Cost: {landmark_json.get('construction_cost', 'No cost available.')}",
            f"Cultural Significance: {landmark_json.get('cultural_significance', 'No significance available.')}",
            f"Geographical Location: {landmark_json.get('geographical_location', 'No location available.')}",
        ]

        # Add the main image generation prompt
        prompt_parts.append(
            f"Image Prompt: {landmark_json.get('image_generation_prompt', 'No prompt available.')}"
        )

        # Combine all parts into a single prompt
        full_prompt = "\n".join(prompt_parts)

        # Generate and save the image
        output_path = self.generator.generate_image(
            model="black-forest-labs/flux-pro",
            input_params={
                "width": 1024,
                "height": 1024,
                "prompt": full_prompt
            }
        )
        return output_path, landmark_json