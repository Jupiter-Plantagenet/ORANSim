from typing import Dict, Any, Union, List
import logging

class A1Interface:
    """
    Simulates the A1 interface between the Non-RT RIC and Near-RT RIC in the ORAN architecture.

    For this basic version, it is a simple interface that supports
    sending and receiving A1 policies, without simulating the underlying
    messaging protocols.
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

    def send_policy(self, policy: Dict[str, Any], near_rt_ric: 'NearRTRIC'):
        """
        Sends an A1 policy from the Non-RT RIC to the Near-RT RIC.

        Args:
            policy (Dict[str, Any]): The A1 policy to send (a dictionary).
        """
        if not isinstance(policy, dict):
            raise TypeError("Policy must be a dictionary")

        if "type" not in policy or "content" not in policy:
          raise ValueError("Policy must have 'type' and 'content' fields")

        if near_rt_ric != self.near_rt_ric:
          raise ValueError("Invalid Near-RT RIC passed to send_policy")

        logging.info(f"A1 Interface: Sending policy of type {policy['type']} from Non-RT RIC to Near-RT RIC")
        try:
            self.near_rt_ric.receive_a1_policy(policy)
        except Exception as e:
            logging.error(f"Failed to send policy: {e}")

    def receive_policy(self, policy: Dict[str, Any]):
        """
        Receives an A1 policy from the Non-RT RIC. This is a placeholder for more complex interactions.

        Args:
            policy (Dict[str, Any]): The A1 policy received (a dictionary).
        """
        if not isinstance(policy, dict):
            raise TypeError("Policy must be a dictionary")
        # In a more advanced implementation, you might perform some validation or processing on the received policy here.
        logging.info(f"A1 Interface: Received policy of type {policy['type']} in Near-RT RIC")