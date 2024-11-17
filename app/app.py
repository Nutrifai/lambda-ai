from flask import Flask, request
from lambda_function import lambda_handler
import json

app = Flask(__name__)

def make_api_gateway_event():
    STAGE = "api"

    event = {
        "httpMethod": request.method,
        "rawPath": f"{STAGE}/{request.path}",
        "path": request.path,
        "body": "{}",
        "headers": dict(request.headers),
        "queryStringParameters": request.args.to_dict(),
        "requestContext": {
            "http": {
                "method": request.method,
                "path": request.path,
            },
            "authorizer": {
                "lambda": {
                    "email": "generic_user@email.com",
                    "expireOn": 1234567890,
                    "sessionId": "session_hash",
                    "userId": "isa",
                }
            },
            "stage": STAGE,
        },
    }

    event["multiValueQueryStringParameters"] = {
        key: value.split(",") for key, value in event["queryStringParameters"].items()
    }

    try:
        event["body"] = request.get_json()
    except:
        pass

    return event



@app.route("/<string:endpoint>", methods=['GET', 'POST', 'OPTIONS'])
@app.route("/<string:endpoint>/<string:pk>", methods=['GET', 'PUT', 'DELETE', 'OPTIONS', 'POST'])
@app.route("/<string:endpoint>/<string:pk>/<string:sk>", methods=['GET', 'PUT', 'DELETE', 'OPTIONS', 'POST'])
@app.route("/<string:endpoint>/<string:pk>/<string:endpoint2>/<string:sk>", methods=['GET', 'PUT', 'DELETE', 'OPTIONS', 'POST'])
@app.route("/<string:endpoint>/<string:pk>/<string:endpoint2>/<string:sk>/<string:endpoint3>", methods=['GET', 'PUT', 'DELETE', 'OPTIONS', 'POST'])
def handle_request(*args, **kwargs):
    response = lambda_handler(make_api_gateway_event())

    body = response.pop("body", None)
    status_code = response.pop("statusCode", 200)
    headers = response.pop("headers", {})

    return body, status_code, headers


if __name__ == "__main__":
    app.run(debug=True, port=5002)