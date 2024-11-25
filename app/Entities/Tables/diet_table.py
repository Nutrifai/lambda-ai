from .base_table import Table
from ..Models.diet_model import DietModel, TableModel

class DietTable(Table):
    """
    Represents the Diet table in the database.
    
    Attributes:
        partition_key (str): The partition key for the table, default is "userId".
        sort_key (str): The sort key for the table, default is "dietId".
        name (str): The name of the table, default is "Diet".
        model (TableModel): The model associated with the table, default is DietModel.
    """

    partition_key: str = "userId"
    sort_key: str = "dietId"
    name: str = "Diet"
    model: TableModel = DietModel