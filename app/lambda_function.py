import json
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, CORSConfig
from aws_lambda_powertools.event_handler.api_gateway import Router
from services.diet_service import DietService
from services.diet_service import DietService
from utils.get_user_info import get_user_info

# CORS configuration settings for handling CORS securely
cors_config = CORSConfig(allow_credentials=True)

# Initialize the router for handling API Gateway events
router = Router()

# Global variable to hold the NutritionistService instance
__diet_service: DietService = None

def __setup_services():
    """
    Initialize the DietService instance if it hasn't been initialized yet.
    
    This function checks if the global __diet_service variable is None. If it is,
    it initializes the DietService instance and assigns it to the global variable.
    """
    global __diet_service

    if __diet_service:
        return

    __diet_service = DietService()


@router.get("/diets")
def get_diets():
    """
    Handle GET requests to retrieve all diets.
    
    This function retrieves the user information from the router context and
    calls the get_diets method of the DietService instance.
    
    Returns:
        dict: A dictionary containing the list of diets.
    """
    user_info = router.context.get("user")
    return __diet_service.get_diets(user_info=user_info)

@router.get("/diets/<dietId>")
def get_diet_by_id(dietId):
    """
    Handle GET requests to retrieve a specific diet by its ID.
    
    Args:
        dietId (str): The ID of the diet to retrieve.
    
    Returns:
        dict: A dictionary containing the details of the specified diet.
    """
    user_info = router.context.get("user")
    return __diet_service.get_diets_by_id(user_info=user_info, dietId=dietId)

@router.post("/diets")
def post_diet():
    """
    Handle POST requests to create a new diet.
    
    This function retrieves the user information from the router context and
    calls the create_diet method of the DietService instance with the request body.
    
    Returns:
        dict: A dictionary containing the details of the created diet.
    """
    user_info = router.context.get("user")
    return __diet_service.generate_diet(body=resolver.current_event.body, user_info=user_info)


# Initialize APIGatewayHttpResolver with CORS
resolver = APIGatewayHttpResolver(cors=cors_config)
resolver.include_router(router=router, prefix="")

def lambda_handler(event, context=None):
    """
    AWS Lambda handler function.

    Args:
        event (dict): The event dictionary containing request data.
        context (object, optional): The context object containing runtime information.
        
    Returns:
        dict: The response dictionary to be returned to API Gateway.
    """
    __setup_services()

    resolver.append_context(user=get_user_info(event))

    # Parse stringified JSON body if present
    if "body" in event and type(event["body"]) is str:
        event["body"] = json.loads(event["body"])

    return resolver.resolve(event, context)
