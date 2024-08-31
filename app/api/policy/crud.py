import logging
from sqlalchemy.orm import Session
from .models import Policy

# Create a logger for this module
logger = logging.getLogger(__name__)


def get_policies(db: Session, skip: int = 0, limit: int = 10) -> list[Policy]:
    """
    Retrieve a list of policies from the database with optional pagination.

    :param db: The database session to use.
    :type db: Session
    :param skip: Number of records to skip, defaults to 0.
    :type skip: int, optional
    :param limit: Maximum number of records to return, defaults to 10.
    :type limit: int, optional
    :return: A list of policies.
    :rtype: list[Policy]
    """
    logger.debug(f"Fetching policies with skip={skip} and limit={limit}")
    policies = db.query(Policy).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(policies)} policies")
    return policies


def get_policy(db: Session, policy_id: int) -> Policy | None:
    """
    Retrieve a single policy from the database by its ID.

    :param db: The database session to use.
    :type db: Session
    :param policy_id: The ID of the policy to retrieve.
    :type policy_id: int
    :return: The policy if found, otherwise None.
    :rtype: Policy | None
    """
    logger.debug(f"Fetching policy with id={policy_id}")
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if policy:
        logger.debug(f"Found policy: {policy}")
    else:
        logger.debug(f"No policy found with id={policy_id}")
    return policy
