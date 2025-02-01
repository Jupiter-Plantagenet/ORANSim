# oransim/core/ric.py
from typing import Dict, Any, List
from oransim.interfaces.a1 import A1Interface, A1Policy
from oransim.interfaces.e2 import E2Interface
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class NearRTRIC:
    """
    Represents a Near-Real-Time RAN Intelligent Controller (Near-RT RIC) in the ORAN architecture.
    """

    def __init__(self, near_rt_ric_id: str,  a1_interface: A1Interface, e2_interface: E2Interface, scheduler):
        self.near_rt_ric_id = near_rt_ric_id
        self.a1_interface = a1_interface
        self.e2_interface = e2_interface
        self.scheduler = scheduler
        self.xapps: Dict[str, Any] = {}  # xApp instances managed by this Near-RT RIC
        self.a1_policies: Dict[str, A1Policy] = {}  # A1 policies received from Non-RT RIC
        self.e2_nodes: Dict[str, Any] = {}  # E2 nodes connected to this Near-RT RIC
        self.supported_e2sm = {} # supported E2 service models
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_xapp(self, xapp):
        """Registers an xApp with the Near-RT RIC."""
        self.xapps[xapp.xapp_id] = xapp
        self.e2_interface.subscribe(xapp.xapp_id, xapp.receive_indication)
        self.logger.info(f"xApp {xapp.xapp_id} registered with Near-RT RIC")

    def remove_xapp(self, xapp_id: str):
        """Unregisters an xApp from the Near-RT RIC."""
        if xapp_id in self.xapps:
            del self.xapps[xapp_id]
            self.e2_interface.unsubscribe(xapp_id)
            self.logger.info(f"xApp {xapp_id} unregistered from Near-RT RIC")
        else:
            self.logger.warning(f"xApp {xapp_id} not found in Near-RT RIC")

    def receive_a1_policy(self, policy_dict: Dict[str, Any]):
        """Receives an A1 policy from the Non-RT RIC."""
        try:
            policy = A1Policy(**policy_dict) # Validate the policy
        except Exception as e:
            self.logger.error(f"Invalid A1 policy received: {e}")
            return

        self.store_a1_policy(policy)

    def store_a1_policy(self, policy: A1Policy):
        """Stores an A1 policy in the Near-RT RIC."""
        self.a1_policies[policy.policy_id] = policy
        self.logger.info(f"Near-RT RIC received A1 policy of type {policy.policy_type} with ID {policy.policy_id}")

    def enforce_a1_policies(self):
        """Applies the A1 policies to the relevant O-CU/O-DU nodes."""
        for policy in self.a1_policies.values():
            if policy.target == "o_du":
                for node_id, node in self.e2_nodes.items():
                    if node.__class__.__name__ == "O_DU":
                        self.logger.info(f"Applying policy of type {policy.policy_type} to O-DU {node_id}")
                        # Implement logic to apply policy to O-DU

            if policy.target == "o_ru":
                for node_id, node in self.e2_nodes.items():
                    if node.__class__.__name__ == "O_RU":
                        self.logger.info(f"Applying policy of type {policy.policy_type} to O-RU {node_id}")
                        # Implement logic to apply policy to O-RU

    def receive_e2_message(self, message: Dict[str, Any], node_id: str):
        """Receives an E2 message from an E2 Node."""
        self.logger.info(f"Near-RT RIC received E2 message from E2 node {node_id}: {message}")
        self.e2_interface.send_indication(message, node_id)

    def register_e2_node(self, node_id: str, node):
        """Registers an E2 node (e.g., O-DU) with the Near-RT RIC."""
        self.e2_nodes[node_id] = node
        self.logger.info(f"E2 node {node_id} registered with Near-RT RIC")

    def get_e2_node(self, node_id: str):
        """Gets the E2 node object based on node_id."""
        return self.e2_nodes.get(node_id)

    def add_supported_e2sm(self, e2sm_id: str, e2sm):
        """Adds a supported E2SM to the dictionary of supported E2SMs"""
        self.supported_e2sm[e2sm_id] = e2sm

class NonRTRIC:
    """
    Represents a Non-Real-Time RAN Intelligent Controller (Non-RT RIC) in the ORAN architecture.
    """

    def __init__(self, a1_interface: A1Interface, scheduler):
        self.a1_interface = a1_interface
        self.scheduler = scheduler
        self.rapps: Dict[str, RApp] = {}  # rApp instances managed by this Non-RT RIC
        self.managed_near_rt_rics: List[NearRTRIC] = []  # List of Near-RT RICs managed by this Non-RT RIC
        self.logger = logging.getLogger(self.__class__.__name__)

    def add_rapp(self, rapp: RApp):
        """Registers an rApp with the Non-RT RIC."""
        self.rapps[rapp.rapp_id] = rapp
        self.logger.info(f"rApp {rapp.rapp_id} registered with Non-RT RIC")

    def remove_rapp(self, rapp_id: str):
        """Unregisters an rApp from the Non-RT RIC."""
        if rapp_id in self.rapps:
            del self.rapps[rapp_id]
            self.logger.info(f"rApp {rapp_id} unregistered from Non-RT RIC")
        else:
            self.logger.warning(f"rApp {rapp_id} not found in Non-RT RIC")

    def create_a1_policy(self, policy_type: A1PolicyType, policy_content: Dict[str, Any], target: str) -> A1Policy:
        """Creates an A1 policy."""
        policy_id = f"policy-{len(self.a1_interface.near_rt_ric.a1_policies) + 1}" # Simple ID generation
        policy = A1Policy(
            policy_type=policy_type,
            policy_id=policy_id,
            policy_content=policy_content,
            target=target
        )
        self.logger.info(f"Non-RT RIC created A1 policy of type {policy_type} with ID {policy_id}")
        return policy

    def send_a1_policy(self, policy: A1Policy, near_rt_ric: NearRTRIC):
        """Sends an A1 policy to a Near-RT RIC."""
        self.a1_interface.send_policy(policy, near_rt_ric)
        self.logger.info(f"Non-RT RIC sent A1 policy of type {policy.policy_type} with ID {policy.policy_id}  to Near-RT RIC")

    def add_managed_near_rt_ric(self, near_rt_ric: NearRTRIC):
        """Adds a Near-RT RIC to the list of managed Near-RT RICs."""
        self.managed_near_rt_rics.append(near_rt_ric)
        print(f"Added Near-RT RIC to managed list")