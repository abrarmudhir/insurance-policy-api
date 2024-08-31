from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from . import crud, schemas

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter(
    prefix="/api",
)


@router.get("/test", summary="Test route")
def test_route() -> dict:
    """
    Test endpoint to verify that the API is working.

    :return: A dictionary with a message confirming the route is operational.
    :rtype: dict
    """
    return {"message": "Test route works!"}


@router.get("/policies", response_model=list[schemas.PolicyResponse], summary="Retrieve policies")
def read_policies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[schemas.PolicyResponse]:
    """
    Retrieve a list of policies with optional pagination.

    :param skip: Number of policies to skip, defaults to 0.
    :type skip: int
    :param limit: Maximum number of policies to return, defaults to 10.
    :type limit: int
    :param db: Database session dependency.
    :type db: Session
    :return: A list of policies.
    :rtype: list[schemas.PolicyResponse]
    :raises HTTPException: If an error occurs during retrieval.
    """
    logger.info(f"Received request to get policies with skip={skip} and limit={limit}")

    try:
        policies = crud.get_policies(db, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(policies)} policies")
        return policies
    except Exception as e:
        logger.error(f"Error retrieving policies: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/policies/{policy_id}", response_model=schemas.PolicyResponse, summary="Retrieve a specific policy")
def read_policy(policy_id: int, db: Session = Depends(get_db)) -> schemas.PolicyResponse:
    """
    Retrieve a specific policy by its ID.

    :param policy_id: The ID of the policy to retrieve.
    :type policy_id: int
    :param db: Database session dependency.
    :type db: Session
    :return: The policy with the specified ID.
    :rtype: schemas.PolicyResponse
    :raises HTTPException: If the policy is not found or an error occurs.
    """
    logger.info(f"Received request to get policy with ID={policy_id}")

    try:
        policy = crud.get_policy(db, policy_id)
        if policy is None:
            logger.warning(f"Policy with ID={policy_id} not found")
            raise HTTPException(status_code=404, detail="Policy not found")

        logger.info(f"Retrieved policy with ID={policy_id}")
        return policy
    except Exception as e:
        logger.error(f"Error retrieving policy with ID={policy_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
