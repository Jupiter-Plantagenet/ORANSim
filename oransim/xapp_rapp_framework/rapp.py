import logging
from typing import Dict, Any
from oransim.core.interfaces.a1 import A1Interface, A1Policy, A1PolicyType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class RApp:
    """
    Base class for rApps in the ORAN Non-RT RIC.

    This class provides a basic structure for rApps, including methods for:
    - Registering with the Non-RT RIC.
    - Creating and managing A1 policies.
    - Interacting with the A1 interface.
    - (Optional) Interacting with an external ML runtime (e.g., ONNX, TensorFlow).
    """

    def __init__(self, rapp_id: str, a1_interface: A1Interface, non_rt_ric):
        """
        Initializes the rApp.

        Args:
            rapp_id (str): A unique identifier for the rApp.
            a1_interface (A1Interface): The A1 interface instance for communication with the Near-RT RIC.
            non_rt_ric (NonRTRIC): The Non-RT RIC instance this rApp is associated with.
        """
        self.rapp_id = rapp_id
        self.a1_interface = a1_interface
        self.non_rt_ric = non_rt_ric
        self.logger = logging.getLogger(self.__class__.__name__)
        self.policies: Dict[str, A1Policy] = {}  # Store created policies

    def register(self):
        """
        Registers the rApp with the Non-RT RIC.
        """
        self.non_rt_ric.add_rapp(self)
        self.logger.info(f"rApp {self.rapp_id} registered with Non-RT RIC")

    def unregister(self):
        """
        Unregisters the rApp from the Non-RT RIC.
        """
        self.non_rt_ric.remove_rapp(self.rapp_id)
        self.logger.info(f"rApp {self.rapp_id} unregistered from Non-RT RIC")

    def create_a1_policy(self, policy_type: A1PolicyType, policy_content: Dict[str, Any], target: str) -> A1Policy:
        """
        Creates an A1 policy.

        Args:
            policy_type (A1PolicyType): The type of the A1 policy (an Enum value).
            policy_content (Dict[str, Any]): The content of the policy (specific to the policy type).
            target (str): Target for the policy (e.g. "o_du", "o_ru")

        Returns:
            A1Policy: The created A1 policy object.
        """
        policy_id = f"policy-{len(self.policies) + 1}"  # Simple ID generation for this example
        policy = A1Policy(
            policy_type=policy_type,
            policy_id=policy_id,
            policy_content=policy_content,
            target=target
        )
        self.policies[policy_id] = policy
        self.logger.info(f"rApp {self.rapp_id} created A1 policy of type {policy_type} with ID {policy_id}")
        return policy

    def send_a1_policy(self, policy_id: str, near_rt_ric_id: str):
        """
        Sends an A1 policy to a specified Near-RT RIC.

        Args:
            policy_id (str): The ID of the policy to send.
            near_rt_ric_id (str): The ID of the Near-RT RIC to send the policy to.
        """
        if policy_id not in self.policies:
            raise KeyError(f"Policy with ID {policy_id} not found in rApp {self.rapp_id}")

        policy = self.policies[policy_id]
        
        # Find the Near-RT RIC instance based on the ID
        near_rt_ric = None
        for ric in self.non_rt_ric.managed_near_rt_rics:
            if ric.near_rt_ric_id == near_rt_ric_id:  # Assuming NearRTRIC has an ID attribute
                near_rt_ric = ric
                break

        if near_rt_ric is None:
            raise ValueError(f"Near-RT RIC with ID {near_rt_ric_id} not found.")
        
        self.a1_interface.send_policy(policy, near_rt_ric)
        self.logger.info(f"rApp {self.rapp_id} sent A1 policy {policy_id} to Near-RT RIC {near_rt_ric_id}")

    def update_a1_policy(self, policy_id: str, new_policy_content: Dict[str, Any]):
        """
        Updates an existing A1 policy.

        Args:
            policy_id (str): The ID of the policy to update.
            new_policy_content (Dict[str, Any]): The new content for the policy.
        """
        if policy_id not in self.policies:
            raise KeyError(f"Policy with ID {policy_id} not found in rApp {self.rapp_id}")

        self.policies[policy_id].policy_content = new_policy_content
        self.logger.info(f"rApp {self.rapp_id} updated A1 policy {policy_id}")

    def delete_a1_policy(self, policy_id: str):
        """
        Deletes an A1 policy.

        Args:
            policy_id (str): The ID of the policy to delete.
        """
        if policy_id not in self.policies:
            raise KeyError(f"Policy with ID {policy_id} not found in rApp {self.rapp_id}")

        del self.policies[policy_id]
        self.logger.info(f"rApp {self.rapp_id} deleted A1 policy {policy_id}")

    # Example of a method that might interact with an external ML runtime:
    # def load_ml_model(self, model_path: str):
    #     """Loads an ML model (e.g., ONNX, TensorFlow) for use by the rApp."""
    #     # Implement model loading logic here, potentially using a library like ONNX Runtime or TensorFlow.
    #     self.logger.info(f"rApp {self.rapp_id} loaded ML model from {model_path}")

    # Add more methods as needed for your specific rApp functionality.