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
    def __init__(self):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
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
        diet = json.loads(self.call_llm(generate_diet_prompt(body)))

        # Prepara os dados para salvar
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
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        return response.text

    def get_diets(self, user_info):
        return self.diet_repository.get_by_pk(pk=user_info.userId)

    def get_diets_by_id(self, user_info, dietId):
        return self.diet_repository.get_by_pk(pk=user_info.userId, sk=dietId)
        