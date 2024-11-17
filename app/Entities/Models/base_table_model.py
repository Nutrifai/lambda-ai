from pydantic import BaseModel, ConfigDict

class TableModel(BaseModel):
    """
    Base DynamoDB Table Interface.
    Use it to set all required fields and their validations
    """

    model_config = ConfigDict(
        extra='allow',
        coerce_numbers_to_str=True,
    )