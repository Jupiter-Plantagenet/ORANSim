from typing import Dict, Any, List
import logging
from enum import Enum
from pydantic import BaseModel, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
    policy_type: A1PolicyType
    policy_id: str
    policy_content: Dict[str, Any]
    version: str = "1.0"
    target: str

class A1Interface:
    """
    Simulates the A1 interface between the Non-RT RIC and Near-RT RIC in the ORAN architecture.

    This implementation supports sending and receiving A1 policies, basic policy validation,
    and error handling.
    """

    def __init__(self, non_rt_ric, near_rt_ric):
        """
        Initializes the A1Interface.

        Args:
            non_rt_ric: The Non-RT RIC instance.
            near_rt_ric: The Near-RT RIC instance.
        """
        self.non_rt_ric = non_rt_ric
        self.near_rt_ric = near_rt_ric
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_policy(self, policy: A1Policy, near_rt_ric: 'NearRTRIC'):
        """
        Sends an A1 policy from the Non-RT RIC to the Near-RT RIC.

        Args:
            policy (A1Policy): The A1 policy to send.
            near_rt_ric ('NearRTRIC'): The Near-RT RIC to send the policy to.
        """
        if near_rt_ric != self.near_rt_ric:
          raise ValueError("Invalid Near-RT RIC passed to send_policy")

        try:
            policy_dict = policy.model_dump() # Convert Pydantic model to dict
            self.near_rt_ric.receive_a1_policy(policy_dict)
            self.logger.info(f"A1 Interface: Sent policy of type {policy.policy_type} (ID: {policy.policy_id}) to Near-RT RIC")
        except Exception as e:
            self.logger.error(f"A1 Interface: Failed to send policy: {e}")

    def receive_policy(self, policy_dict: Dict[str, Any]):
        """
        Receives an A1 policy from the Non-RT RIC. Performs basic validation and stores the policy in the Near-RT RIC.

        Args:
            policy_dict (Dict[str, Any]): The A1 policy received (a dictionary).

        Returns:
            bool: True if the policy is successfully received and validated, False otherwise.
        """
        try:
            # Validate the received policy using the Pydantic model
            policy = A1Policy(**policy_dict)
        except ValidationError as e:
            self.logger.error(f"A1 Interface: Invalid A1 policy received: {e}")
            return False
        try:
            self.near_rt_ric.store_a1_policy(policy)
            self.logger.info(f"A1 Interface: Received policy of type {policy.policy_type} (ID: {policy.policy_id}) in Near-RT RIC")
            return True
        except Exception as e:
            self.logger.error(f"A1 Interface: Failed to receive policy: {e}")
            return False