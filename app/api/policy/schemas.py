from pydantic import BaseModel


class PolicyResponse(BaseModel):
    """
    Schema for representing a policy response.

    :param id: Unique identifier for the policy.
    :type id: int
    :param name: Name of the policy.
    :type name: str
    :param coverage_amount: Coverage amount of the policy.
    :type coverage_amount: float
    :param premium: Premium cost of the policy.
    :type premium: float
    """

    id: int
    name: str
    coverage_amount: float
    premium: float

    class Config:
        """
        Configuration for Pydantic models.

        - `from_attributes` enables attribute access for model instances.
        """
        from_attributes = True
