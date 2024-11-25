def generate_diet_prompt(data):
    """
    Generates a diet prompt based on the provided patient data.

    Args:
        data (dict): A dictionary containing patient information with the following keys:
            - idade (int): Age of the patient in years.
            - peso (float): Weight of the patient in kilograms.
            - altura (float): Height of the patient in centimeters.
            - sexo (str): Gender of the patient.
            - nivel_atividade (str): Activity level of the patient.
            - condicao_saude (str, optional): Health conditions of the patient. Defaults to "Nenhuma".
            - alergia (str, optional): Allergies of the patient. Defaults to "Nenhuma".
            - refeicoes_diarias (int): Number of daily meals.
            - objetivo (str): Goal of the diet.
            
    Returns:
        str: A formatted string prompt for generating a personalized diet plan in JSON format.
    """

    prompt = f"""
    Você é um nutricionista especialista em gerar dietas personalizadas levando em consideração as necessidades e restrições de cada paciente.
    Neste momento você está atendendo que possui as seguintes informações:
    - Idade: {data["idade"]} anos
    - Peso: {data["peso"]} kg
    - Altura: {data["altura"]} cm
    - Sexo: {data["sexo"]}
    - Nível de atividade: {data["nivel_atividade"]}
    - Condições de saúde: {data.get("condicao_saude", "Nenhuma")}
    - Alergias: {data.get("alergia", "Nenhuma")}
    - Número de refeições diárias: {data["refeicoes_diarias"]}
    - Objetivo: {data["objetivo"]}
    
    
    Com base nessas informações, crie uma dieta personalizada para o paciente. Lembre-se que a dieta deve trazer as quantidades de calorias de cada refeição e o total diário, além de ser balanceada e saudável.

    Seu retorno deve ser um json com a seguinte estrutura (não adicione ```json``` no início do json):
    {{
        "refeicoes": [
        {{
            "refeicao": "Café da manhã",
            "alimentos": [
                {{
                    "alimento": "Alimento 1",
                    "quantidade": "Quantidade do alimento 1",
                    "calorias": "Calorias do alimento 1"
                }},
                {{
                    "alimento": "Alimento 2",
                    "quantidade": "Quantidade do alimento 2",
                    "calorias": "Calorias do alimento 2"
                }}
            ],
            "calorias": "Total de calorias da refeição"
        }},
        ...
        ],
        "calorias_diarias": "Total de calorias diárias",
        "observacoes_importante": "Observações importantes sobre a dieta gerada",
        "titulo": "Título da dieta gerada",
    }}
    """
    return prompt.strip()