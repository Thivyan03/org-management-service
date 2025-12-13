from fastapi import FastAPI
from .routes.org_routes import router as org_router
from .routes.auth_routes import router as auth_router
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Organization Management Service")

app.include_router(org_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Backend running successfully!"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Organization Management Service",
        version="1.0.0",
        description="Org Management API with JWT Auth",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
