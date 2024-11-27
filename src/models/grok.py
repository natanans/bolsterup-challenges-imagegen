from pydantic import BaseModel, ValidationError
from typing import Optional, Union, List
from groq import Groq
import json


class LandmarkResponse(BaseModel):
    """
    Data model for representing information about a landmark.
    """
    description: Optional[str] = None  # Brief description of the landmark and its historical significance
    architects: Optional[Union[str, List[str]]] = None  # Architects or designers responsible for its construction
    construction_year: Optional[str] = None  # Year the landmark was built
    materials: Optional[Union[str, List[str]]] = None  # Materials used in its construction
    interesting_facts: Optional[Union[str, List[str]]] = None  # Interesting facts or historical anecdotes
    dimensions: Optional[Union[str, List[str]]] = None  # Dimensions or unique features of the landmark
    construction_cost: Optional[Union[str, List[str]]] = None  # Cost of construction
    cultural_significance: Optional[Union[str, List[str]]] = None  # Cultural or historical significance
    geographical_location: Optional[Union[str, List[str]]] = None  # Geographical location or significance of the landmark
    image_generation_prompt: Optional[Union[str, List[str]]] = None  # Image generation prompt based on user input
    error: Optional[str] = None  # Error field for any processing issues

    @classmethod
    def model_validate_json(cls, json_data: dict):
        """
        Validate and preprocess JSON data into the LandmarkResponse model.

        Args:
            json_data (dict): Input JSON data to be validated and processed.

        Returns:
            LandmarkResponse: The validated data as a LandmarkResponse object.
        """
        for key, value in json_data.items():
            if isinstance(value, list):
                json_data[key] = ", ".join(value)  # Convert lists to comma-separated strings
            elif isinstance(value, int):
                json_data[key] = str(value)  # Convert integers to strings
            elif isinstance(value, dict):
                json_data[key] = "; ".join([f"{k}: {v}" for k, v in value.items()])  # Convert dictionaries to strings
        return cls(**json_data)


class LLMRetriever:
    """
    A class to retrieve detailed information about landmarks using the Groq API.
    """
    def __init__(self, api_key):
        """
        Initialize the LLMRetriever.

        Args:
            groq_instance (Groq): Instance of the Groq API client.
        """
        self.groq = Groq(api_key=api_key)

    def fetch_landmark_details(self, landmark_name: str) -> Optional[LandmarkResponse]:
        """
        Retrieve detailed information about a landmark.

        Args:
            landmark_name (str): The name of the landmark to retrieve information for.

        Returns:
            Optional[LandmarkResponse]: The retrieved landmark details as a LandmarkResponse object,
            or an error message if retrieval fails.
        """
        landmark_name = landmark_name + " json" # for grok json reterival
        try:
            chat_completion = self.groq.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an assistant specialized in retrieving and analyzing landmark information. "
                            "Provide a JSON response with the following keys and values:\n"
                            "'description': A brief description of the landmark and its historical significance.\n"
                            "'architects': Architects or designers responsible for its construction.\n"
                            "'construction_year': Year it was built.\n"
                            "'materials': Materials used in its construction.\n"
                            "'interesting_facts': Interesting facts or historical anecdotes related to the landmark.\n"
                            "'dimensions': Dimensions or unique features of the landmark.\n"
                            "'construction_cost': Cost of construction.\n"
                            "'cultural_significance': Cultural or historical significance.\n"
                            "'geographical_location': Geographical location or significance of the landmark.\n"
                            "'image_generation_prompt': Prompt for generating an image based on the user input. "
                            "Use the above values to ensure accuracy and include the landmark name.\n"
                            "If any information is missing, state it explicitly as 'no_value'."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Landmark: {landmark_name}"
                    }
                ],
                model="llama3-70b-8192",
                temperature=0.7,
                stream=False,
                response_format={"type": "json_object"}
            )
            
            # Validate and parse the response into a LandmarkResponse object
            return LandmarkResponse.model_validate_json(json.loads(chat_completion.choices[0].message.content))
        except ValidationError as e:
            raise ValueError(f"Validation failed for the response: {e}") from e
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while fetching landmark details: {e}") from e