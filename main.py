import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
from routers import prime, picture, time

load_dotenv()

app = FastAPI()
app.include_router(prime.router)
app.include_router(picture.router)
app.include_router(time.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["paths"]["/time"] = {
        "get": {
            "requestBody": {"content": {"application/json": {}}, "required": True}, "tags": ["default"],
            "description": f"Authorization: Bearer {os.getenv('API_TOKEN')}",
            "responses": {
                "200": {
                    "description": "Successfully response",
                },
                "401": {
                    "description": "Unauthorized"
                }
            }
        },

    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
