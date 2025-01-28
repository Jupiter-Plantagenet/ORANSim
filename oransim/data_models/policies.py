from pydantic import BaseModel  

class A1Policy(BaseModel):  
    policy_id: int  
    policy: str          # Simplified for now; later use ENUMs  
    validity_window: tuple = (0, 0)  # Start/end timestamps  