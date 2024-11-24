from .base_table_model import TableModel

class DietModel(TableModel):
    """
    DietModel represents a dietary plan for a user.
    
    Attributes:
        dietId (str): Unique identifier for the diet.
        userId (str): Unique identifier for the user.
        meals (list[dict]): List of meals included in the diet.
        calories (str): Total calories for the diet.
        importantObservations (str): Important observations regarding the diet.
        creationDate (str): Date when the diet was created.
        title (str): Title of the diet plan.
        goal (str): Goal of the diet (e.g., weight loss, muscle gain).
    """

    dietId: str
    userId: str 
    meals: list[dict]
    calories: str 
    importantObservations: str
    creationDate: str 
    title: str
    goal: str
