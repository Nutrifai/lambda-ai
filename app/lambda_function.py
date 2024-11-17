import json
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
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
    Initialize the NutritionistService instance if it hasn't been initialized yet.
    """
    global __diet_service

    if __diet_service:
        return

    __diet_service = DietService()


@router.get("/diets")
def get_diets():
    user_info = router.context.get("user")
    return __diet_service.get_diets(user_info=user_info)

@router.get("/diets/<dietId>")
def get_diet_by_id(dietId):
    user_info = router.context.get("user")
    return __diet_service.get_diets_by_id(user_info=user_info, dietId=dietId)

@router.post("/diets")
def post_diet():
    user_info = router.context.get("user")
    return __diet_service.generate_diet(body=resolver.current_event.body, user_info=user_info)


# Initialize APIGatewayRestResolver with CORS
resolver = APIGatewayRestResolver(cors=cors_config)
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
