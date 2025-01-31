from typing import Dict, Any, List
from oransim.core.interfaces.a1 import A1Interface
from oransim.core.interfaces.e2 import E2Interface

class NearRTRIC:
    """
    Represents a Near-Real-Time RAN Intelligent Controller (Near-RT RIC) in the ORAN architecture.
    """

    def __init__(self, a1_interface: A1Interface, e2_interface: E2Interface, scheduler):
        self.a1_interface = a1_interface
        self.e2_interface = e2_interface
        self.scheduler = scheduler
        self.xapps: Dict[str, Any] = {}  # xApp instances managed by this Near-RT RIC
        self.a1_policies: Dict[str, Any] = {}  # A1 policies received from Non-RT RIC
        self.e2_nodes: Dict[str, Any] = {}  # E2 nodes connected to this Near-RT RIC
        self.supported_e2sm = {} # supported E2 service models

    def add_xapp(self, xapp):
        """Registers an xApp with the Near-RT RIC."""
        self.xapps[xapp.xapp_id] = xapp
        print(f"xApp {xapp.xapp_id} registered with Near-RT RIC")

    def remove_xapp(self, xapp_id: str):
        """Unregisters an xApp from the Near-RT RIC."""
        if xapp_id in self.xapps:
            del self.xapps[xapp_id]
            print(f"xApp {xapp_id} unregistered from Near-RT RIC")
        else:
            print(f"xApp {xapp_id} not found in Near-RT RIC")

    def receive_a1_policy(self, policy: Dict[str, Any]):
        """Receives an A1 policy from the Non-RT RIC."""
        policy_type = policy["type"]
        self.a1_policies[policy_type] = policy
        print(f"Near-RT RIC received A1 policy of type {policy_type}")

    def enforce_a1_policies(self):
      """Applies the A1 policies to the relevant O-CU/O-DU nodes."""
      for type, policy in self.a1_policies.items():
          if policy["target"] == "o_du":
            for node_id, node in self.e2_nodes.items():
              if node.__class__.__name__ == "O_DU":
                print(f"Applying policy of type {policy['type']} to O-DU {node_id}")

          if policy["target"] == "o_ru":
            for node_id, node in self.e2_nodes.items():
              if node.__class__.__name__ == "O_RU":
                print(f"Applying policy of type {policy['type']} to O-RU {node_id}")

    def receive_e2_message(self, message: Dict[str, Any], du_id: str):
        """Receives an E2 message from an O-DU."""
        # Process the E2 message (e.g., E2SM-KPM report)
        print(f"Near-RT RIC received E2 message from O-DU {du_id}: {message}")
        # Forward the message to the relevant xApp based on message type or other criteria
        self.e2_interface.send_indication(message, du_id)

    def register_e2_node(self, node_id: str, node):
      """Registers an E2 node (e.g., O-DU) with the Near-RT RIC."""
      self.e2_nodes[node_id] = node
      print(f"E2 node {node_id} registered with Near-RT RIC")

    def get_e2_node(self, node_id: str):
      """Gets the E2 node object based on node_id."""
      return self.e2_nodes[node_id]

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
        self.rapps: Dict[str, Any] = {}  # rApp instances managed by this Non-RT RIC
        self.managed_near_rt_rics: List[NearRTRIC] = []  # List of Near-RT RICs managed by this Non-RT RIC

    def add_rapp(self, rapp):
        """Registers an rApp with the Non-RT RIC."""
        self.rapps[rapp.rapp_id] = rapp
        print(f"rApp {rapp.rapp_id} registered with Non-RT RIC")

    def remove_rapp(self, rapp_id: str):
        """Unregisters an rApp from the Non-RT RIC."""
        if rapp_id in self.rapps:
            del self.rapps[rapp_id]
            print(f"rApp {rapp_id} unregistered from Non-RT RIC")
        else:
            print(f"rApp {rapp_id} not found in Non-RT RIC")

    def create_a1_policy(self, policy_type: str, policy_content: Dict[str, Any], target: str):
        """Creates an A1 policy."""
        policy = {
            "type": policy_type,
            "content": policy_content,
            "target": target
        }
        print(f"Non-RT RIC created A1 policy of type {policy_type}")
        return policy

    def send_a1_policy(self, policy: Dict[str, Any], near_rt_ric: NearRTRIC):
        """Sends an A1 policy to a Near-RT RIC."""
        self.a1_interface.send_policy(policy, near_rt_ric)
        print(f"Non-RT RIC sent A1 policy of type {policy['type']} to Near-RT RIC")

    def add_managed_near_rt_ric(self, near_rt_ric: NearRTRIC):
        """Adds a Near-RT RIC to the list of managed Near-RT RICs."""
        self.managed_near_rt_rics.append(near_rt_ric)
        print(f"Added Near-RT RIC to managed list")