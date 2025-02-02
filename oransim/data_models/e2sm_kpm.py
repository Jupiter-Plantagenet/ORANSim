from typing import Dict, Any, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class MeasurementType(Enum):
    """
    Enumerates the possible types of measurements for E2SM-KPM.
    """
    RSRP = "RSRP"
    RSRQ = "RSRQ"
    SNR = "SNR"
    # Add more measurement types as needed

class MeasurementRecord(BaseModel):
    """
    Represents a single measurement record for a specific UE.
    """
    ue_id: str = Field(..., description="The ID of the UE")
    meas_type: MeasurementType = Field(..., description="The type of measurement (e.g., RSRP, RSRQ)")
    value: float = Field(..., description="The measured value")

class E2SM_KPM_IndicationHeader(BaseModel):
    """
    Represents the header of an E2SM-KPM Indication message.
    """
    du_id: str = Field(..., description="ID of the O-DU sending the message")
    timestamp: float = Field(..., description="Timestamp of the measurement")

class E2SM_KPM_IndicationMessage(BaseModel):
    """
    Represents an E2SM-KPM Indication message.

    This is a simplified representation of an E2SM-KPM Indication message.
    In a real implementation, you would need to follow the ASN.1 definition
    of the E2SM-KPM service model.
    """
    header: E2SM_KPM_IndicationHeader = Field(..., description="The header of the message")
    measurements: List[MeasurementRecord] = Field(..., description="A list of measurement records")

    @validator("measurements")
    def check_measurements_not_empty(cls, v):
        if not v:
            raise ValueError("measurements list cannot be empty")
        return v