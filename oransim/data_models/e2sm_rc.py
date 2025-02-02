from typing import Dict, Any, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class ControlType(Enum):
    """
    Enumerates the possible types of control actions for E2SM-RC.
    """
    HO_REQUEST = "HO_REQUEST"
    BEAMFORMING_UPDATE = "BEAMFORMING_UPDATE"
    # Add more control types as needed

class ControlAction(BaseModel):
    """
    Represents a control action within an E2SM-RC Control message.
    """
    control_type: ControlType = Field(..., description="The type of control action (e.g. HO_REQUEST)")
    parameters: Dict[str, Any] = Field(..., description="Parameters specific to the control action")

class E2SM_RC_ControlHeader(BaseModel):
    """
    Represents the header of an E2SM-RC Control message.
    """
    ric_id: str = Field(..., description="ID of the Near-RT RIC sending the message")
    du_id: str = Field(..., description="ID of the O-DU targeted by the message")
    timestamp: float = Field(..., description="Timestamp of when the message is generated")

class E2SM_RC_ControlMessage(BaseModel):
    """
    Represents an E2SM-RC Control message.

    This is a simplified representation of an E2SM-RC Control message.
    In a real implementation, you would need to follow the ASN.1 definition
    of the E2SM-RC service model.
    """
    header: E2SM_RC_ControlHeader = Field(..., description="The header of the message")
    actions: List[ControlAction] = Field(..., description="A list of control actions")

    @validator("actions")
    def check_actions_not_empty(cls, v):
        if not v:
            raise ValueError("actions list cannot be empty")
        return v