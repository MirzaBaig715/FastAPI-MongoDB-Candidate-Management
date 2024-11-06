import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

from src.api.middleware import LoggingMiddleware
from src.api.routes import auth, candidates, health
from src.config.settings import get_settings
from src.infrastructure.database import db

settings = get_settings()

# Initialize Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )

# FastAPI app initialization
app = FastAPI(title=settings.APP_NAME, version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await db.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()


# Register routers
app.include_router(
    health.router,
    prefix=settings.API_V1_PREFIX,
    tags=["health"]
)
app.include_router(
    auth.router,
    prefix=settings.API_V1_PREFIX,
    tags=["auth"]
)
app.include_router(
    candidates.router,
    prefix=settings.API_V1_PREFIX,
    tags=["candidates"]
)

app.add_middleware(LoggingMiddleware)

# Security configuration for Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Candidate Management System API",
        version="1.0.0",
        description="A modern API for managing candidate "
        "profiles and recruitment process",
        routes=app.routes,
    )

    # Define security scheme for Bearer tokens
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply Bearer token security globally
    openapi_schema["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
