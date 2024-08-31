from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Policy(Base):
    """
    Represents a policy in the database.

    This class is used to define the structure of the `policies` table,
    which includes information about insurance policies.

    Attributes:
        id (int): The unique identifier for the policy.
        name (str): The name of the policy.
        coverage_amount (float): The amount covered by the policy.
        premium (float): The premium cost of the policy.
    """
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    """
    The unique identifier for the policy.

    :type: int
    """

    name = Column(String, index=True)
    """
    The name of the policy.

    :type: str
    """

    coverage_amount = Column(Float)
    """
    The amount covered by the policy.

    :type: float
    """

    premium = Column(Float)
    """
    The premium cost of the policy.

    :type: float
    """
