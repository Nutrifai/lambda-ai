from .base_table import Table
from ..Models.diet_model import DietModel, TableModel

class DietTable(Table):
    partition_key: str = "userId"
    sort_key: str = "dietId"
    name: str = "Diet"
    model: TableModel = DietModel