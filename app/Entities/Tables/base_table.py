from pydantic import BaseModel
from ..Models.base_table_model import TableModel

class Table(BaseModel):
    """
    Represents a table entity with partition key, name, model, and optional sort key.
    Attributes:
    
        partition_key (str): The partition key for the table.
        name (str): The name of the table.
        model (TableModel): The model associated with the table.
        sort_key (str, optional): The sort key for the table. Defaults to an empty string.
    """

    partition_key: str
    name: str
    model: TableModel
    sort_key: str = ''