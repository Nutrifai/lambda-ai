from pydantic import BaseModel
from ..Models.base_table_model import TableModel

class Table(BaseModel):
    partition_key: str
    name: str
    model: TableModel
    sort_key: str = ''