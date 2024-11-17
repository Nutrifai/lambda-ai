from pydantic import BaseModel


class UserRequestInfo(BaseModel):
    email: str
    expireOn: int
    sessionId: str
    userId: str

def get_user_info(event: dict) -> UserRequestInfo:
    return UserRequestInfo(
        **event.get("requestContext", {}).get("authorizer", {}).get("lambda", {})
    )