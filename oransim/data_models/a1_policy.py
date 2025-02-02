from typing import Dict, Any, Union, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class A1PolicyType(Enum):
    """
    Enumeration for supported A1 policy types.
    """
    TYPE_1 = "POLICY-TYPE-1"  # Example policy types
    TYPE_2 = "POLICY-TYPE-2"
    TYPE_3 = "POLICY-TYPE-3"

class A1Policy(BaseModel):
    """
    Represents an A1 policy.

    Attributes:
        policy_type (A1PolicyType): The type of the A1 policy.
        policy_id (str): Unique identifier for the policy.
        policy_content (Dict[str, Any]): The content of the policy (specific to the policy type).
        version: (str): Version of the policy.
        target: (str): Target for the policy (e.g. "o_du", "o_ru").
    """
    policy_type: A1PolicyType = Field(..., description="The type of the A1 policy.")
    policy_id: str = Field(..., description="Unique identifier for the policy.")
    policy_content: Dict[str, Any] = Field(..., description="The content of the policy (specific to the policy type).")
    version: str = Field("1.0", description="Version of the policy.")
    target: str = Field(..., description="Target for the policy (e.g. 'o_du', 'o_ru')")

    @validator("policy_id")
    def policy_id_must_be_non_empty(cls, v):
        if not v:
            raise ValueError("policy_id must be a non-empty string")
        return v

    @validator("target")
    def validate_target(cls, v):
        valid_targets = ["o_du", "o_ru"]
        if v not in valid_targets:
            raise ValueError(f"Invalid target: {v}. Must be one of: {valid_targets}")
        return v

    class Config:
        # Use enums by value for serialization/deserialization
        use_enum_values = True