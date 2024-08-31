from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix="/api")


@router.get("/health", summary="Check the health status of the service")
async def health() -> Dict[str, str]:
    """
    Endpoint to check the health status of the service.

    :return: A dictionary with the status of the service.
    :rtype: dict[str, str]
    """
    return {"status": "ok"}
