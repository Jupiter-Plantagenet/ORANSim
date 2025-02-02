import logging
from typing import Dict, Any
from oransim.interfaces.a1 import A1Interface, A1Policy, A1PolicyType
from oransim.xapp_rapp_framework.rapp import RApp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class LoadBalancingRApp(RApp):
    """
    An example rApp that demonstrates a simple load balancing algorithm.

    This rApp monitors the load of O-DUs (via xApps and Near-RT RIC) and creates A1 policies
    to influence UE association and handover decisions, aiming to distribute load more evenly.

    For demonstration purposes, this rApp uses a simple threshold-based algorithm.
    In a real implementation, you would use more sophisticated techniques.
    """

    def __init__(self, rapp_id: str, a1_interface: A1Interface, non_rt_ric, load_threshold: float = 0.8):
        super().__init__(rapp_id, a1_interface, non_rt_ric)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.load_threshold = load_threshold  # Load threshold above which to trigger balancing actions

    def register(self):
        """
        Registers the rApp with the Non-RT RIC.
        """
        super().register()
        # Start monitoring O-DU load periodically (e.g., every 5 seconds)
        self.non_rt_ric.scheduler.add_event(5, self.monitor_o_du_load)

    def monitor_o_du_load(self):
        """
        Monitors the load of O-DUs and triggers load balancing actions if necessary.
        """
        self.logger.info(f"rApp {self.rapp_id} monitoring O-DU load...")
        # In a real implementation, you would query the Non-RT RIC or a monitoring system for O-DU load information.
        # Here, we'll simulate some O-DU load data for demonstration purposes.

        o_du_loads = {
            "o_du_1": random.uniform(0.6, 0.9),
            "o_du_2": random.uniform(0.3, 0.7),
            "o_du_3": random.uniform(0.7, 0.95),
        }

        overloaded_odus = [du_id for du_id, load in o_du_loads.items() if load > self.load_threshold]

        if overloaded_odus:
            self.logger.info(f"rApp {self.rapp_id} detected overloaded O-DUs: {overloaded_odus}")
            self.initiate_load_balancing(overloaded_odus, o_du_loads)
        else:
            self.logger.info("No O-DU load above threshold detected")

        # Re-schedule the monitoring event after 5 seconds
        self.non_rt_ric.scheduler.add_event(5, self.monitor_o_du_load)

    def initiate_load_balancing(self, overloaded_odus: List[str], o_du_loads: Dict[str, float]):
        """
        Initiates load balancing actions by creating and sending A1 policies.

        Args:
            overloaded_odus (List[str]): List of overloaded O-DU IDs.
            o_du_loads (Dict[str, float]): Dictionary mapping O-DU IDs to their load.
        """
        for du_id in overloaded_odus:
            # Find a suitable target O-DU for load balancing (e.g., the least loaded one)
            target_du_id = min(o_du_loads, key=o_du_loads.get)  # Simple example: choose the least loaded

            # Create an A1 policy to steer traffic from the overloaded O-DU to the target O-DU
            policy_content = {
                "action": "steer_traffic",
                "source_du": du_id,
                "target_du": target_du_id,
                "ue_group": "high_load_ues",  # You can define criteria for selecting UEs for load balancing
                "intensity": "high"
            }
            policy = self.create_a1_policy(A1PolicyType.TYPE_2, policy_content, target="o_du")
            # Find the Near-RT RIC associated with the O-DU
            for near_rt_ric in self.non_rt_ric.managed_near_rt_rics:
                if du_id in near_rt_ric.e2_nodes:  # Assuming NearRTRIC has a way to track managed O-DUs
                    # Send the policy to the responsible Near-RT RIC
                    self.send_a1_policy(policy.policy_id, near_rt_ric.near_rt_ric_id)
                    break
                else:
                    self.logger.info(f"Near-RT RIC not found for O-DU {du_id}")
            else:
                self.logger.warning(f"No suitable Near-RT RIC found for O-DU {du_id}")