from pydantic import BaseModel


class UserRequestInfo(BaseModel):
    """
    Model representing user request information.
    
    Attributes:
        email (str): The email of the user.
        expireOn (int): The expiration time of the session.
        sessionId (str): The session ID.
        userId (str): The user ID.
    """
    email: str
    expireOn: int
    sessionId: str
    userId: str

def get_user_info(event: dict) -> UserRequestInfo:
    """
    Extract user information from the event dictionary.
    
    This function extracts user information from the 'requestContext' key in the event
    dictionary and returns it as a UserRequestInfo instance.
    
    Args:
        event (dict): The event dictionary containing request context.
    
    Returns:
        UserRequestInfo: An instance of UserRequestInfo containing the extracted user information.
    """
    return UserRequestInfo(
        **event.get("requestContext", {}).get("authorizer", {}).get("lambda", {})
    )