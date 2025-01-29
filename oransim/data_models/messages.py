from enum import Enum  
from pydantic import BaseModel  

class MetricType(str, Enum):  
    CELL_LOAD = "cell_load"  
    HANDOVER_SUCCESS = "handover_success"  

class E2SMKPMIndication(BaseModel):  
    cell_id: int  
    metric: MetricType  
    value: float  
    timestamp: float = 0.0  # Simulated time  