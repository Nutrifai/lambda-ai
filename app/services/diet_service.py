import google.generativeai as genai
from assets.prompts.diet_prompt import generate_diet_prompt
from repositories.base_table_repository import TableRepository
from Entities.Tables.diet_table import DietTable
import uuid
import datetime
import json

API_KEY = "to_be_replaced"
genai.configure(api_key=API_KEY)
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class DietService:
    """
    Service class for handling diet-related operations.
    
    This class provides methods to generate diets and interact with the diet repository.
    """
    def __init__(self):
        """
        Initialize the DietService instance.
        
        This constructor initializes the generative model with the specified configuration
        and sets up the diet repository.
        """
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 10,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
        )

        self.diet_repository = TableRepository(table=DietTable())

    def generate_diet(self, body, user_info):
        """
        Generate a diet based on the provided body and user information.
        
        This function calls the generative model to create a diet and prepares the data
        for saving in the diet repository.
        
        Args:
            body (dict): The request body containing diet generation parameters.
            user_info (UserRequestInfo): The user information.
        
        Returns:
            dict: A dictionary containing the generated diet details.
        """
        diet = json.loads(self.call_llm(generate_diet_prompt(body)))

        # Prepare diet data for saving
        diet_body = {
            'dietId': str(uuid.uuid4()),
            'userId': user_info.userId,
            'meals': diet.get('refeicoes'),
            'calories': diet.get('calorias_diarias'),
            'importantObservations': diet.get('observacoes_importante'),
            'creationDate': str(datetime.datetime.now()),
            'title': diet.get('titulo'),
            'goal': body['objetivo']
        }

        self.diet_repository.create_item(diet_body)
        return diet_body

    def call_llm(self, prompt: str):
        """
        Call the language model with the specified prompt.
        """
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        return response.text

    def get_diets(self, user_info):
        """
        Retrieve all diets for the specified user.
        """
        return self.diet_repository.get_by_pk(pk=user_info.userId)

    def get_diets_by_id(self, user_info, dietId):
        """
        Retrieve a specific diet by its ID.
        """
        return self.diet_repository.get_by_pk(pk=user_info.userId, sk=dietId)
        