from .base_table_model import TableModel

class DietModel(TableModel):
    dietId: str
    userId: str 
    meals: list[dict]
    calories: str 
    importantObservations: str
    creationDate: str 
    title: str
    goal: str
