import logging
from fastapi import FastAPI
from app.api.health import routes as health_routes
from app.api.policy import routes as policy_routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
api = FastAPI()


async def lifespan(app: FastAPI) -> None:
    """
    Lifespan event handler for the FastAPI application.

    Logs startup and shutdown events of the application.

    :param app: The FastAPI application instance.
    :type app: FastAPI
    :return: None
    """
    logger.info("Starting up the FastAPI application")
    try:
        yield
    finally:
        logger.info("Shutting down the FastAPI application")


# Set the lifespan handler for the FastAPI instance
api.lifespan = lifespan

# Include routers with appropriate prefixes
api.include_router(health_routes.router)
api.include_router(policy_routes.router)


@api.get("/", summary="Root endpoint")
async def read_root() -> dict:
    """
    Root endpoint for basic checks.

    Logs access to the root endpoint and returns a welcome message.

    :return: A dictionary with a welcome message.
    :rtype: dict
    """
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the API"}
