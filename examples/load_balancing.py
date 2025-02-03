import logging
import numpy as np
from oransim.core.nodes import O_RU, O_DU, UE, DUConfig, RUConfig
from oransim.core.interfaces.o1 import O1Interface
from oransim.core.interfaces.e2 import E2Interface
from oransim.core.interfaces.f1 import F1Interface
from oransim.core.interfaces.xn import XnInterface
from oransim.core.interfaces.x2 import X2Interface
from oransim.core.mobility import RandomWaypointModel
from oransim.simulation.scheduler import ORANScheduler
from oransim.xapp_rapp_framework.xapp import XApp
from oransim.analytics.collector import CSVDataCollector
from oransim.analytics.analyzer import DataAnalyzer
from oransim.analytics.visualizer import DataVisualizer
from oransim.core.ric import NearRTRIC, NonRTRIC
from oransim.xapp_rapp_framework.xapp import XApp
from oransim.xapp_rapp_framework.rapp import RApp
from oransim.interfaces.a1 import A1Interface, A1Policy, A1PolicyType
import oransim.config_schema as config_schema
import os
import yaml
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create an rApp for load balancing
class LoadBalancingRApp(RApp):
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

def main():
    # Create a scheduler
    scheduler = ORANScheduler()

    # Create config directory if it doesn't exist
    config_directory = "configs"
    os.makedirs(config_directory, exist_ok=True)

    # Create a dummy config_schema.yaml file
    config_schema_path = "config_schema.yaml"
    with open(config_schema_path, "w") as f:
        yaml.dump(config_schema.schema, f)

    # Create an O1 interface instance
    o1_interface = O1Interface(config_directory, config_schema_path)

    # Create an A1 interface instance
    a1_interface = A1Interface(None, None)

    # Create a Near-RT RIC instance
    e2_interface = E2Interface(None, scheduler)
    near_rt_ric = NearRTRIC("near_rt_ric_1", a1_interface, e2_interface, scheduler)
    a1_interface.near_rt_ric = near_rt_ric

    # Create a Non-RT RIC instance
    non_rt_ric = NonRTRIC(a1_interface, scheduler)
    a1_interface.non_rt_ric = non_rt_ric
    non_rt_ric.add_managed_near_rt_ric(near_rt_ric)

    # Create an rApp for load balancing
    load_balancing_rapp = LoadBalancingRApp("load_balancing_rapp_1", a1_interface, non_rt_ric)
    load_balancing_rapp.register()

    # Create an F1 interface instance
    f1_interface = F1Interface(scheduler)

    # Create an X2 interface instance
    x2_interface = X2Interface(scheduler)

    # Create an Xn interface instance
    xn_interface = XnInterface(scheduler)

    # Create O-RU configurations
    o_ru1_config = RUConfig(
        ru_id="o-ru-1",
        frequency=2.4e9,
        bandwidth=20e6,
        tx_power=30,
        supported_operations=["start", "stop", "reconfigure"],
        cells=[{"cell_id": "cell_1", "max_ues": 50}, {"cell_id": "cell_2", "max_ues": 75}],
    )

    # Create O-RU instances
    o_ru1 = O_RU(o_ru1_config, scheduler)

    # Set the interfaces for the nodes
    o_ru1.set_xn_interface(xn_interface)
    o_ru1.set_x2_interface(x2_interface)

    # Create O-DU configurations
    o_du1_config = DUConfig(
        du_id="o-du-1",
        max_ues=100,
        schedulers=["scheduler_1", "scheduler_2"],
        cells=[{"cell_id": "cell_3", "du_id": "du_1", "max_ues": 60}],
    )

    # Create O-DU instances
    o_du1 = O_DU(o_du1_config, scheduler)
    
    # Set the interfaces for the nodes
    o_du1.set_xn_interface(xn_interface)
    o_du1.set_x2_interface(x2_interface)
    o_du1.set_e2_interface(e2_interface)
    o_du1.set_e2_node(near_rt_ric)
    o_du1.set_f1_interface(f1_interface)
    near_rt_ric.register_e2_node("o_du_1", o_du1)

    # Apply the configurations using the O1 interface
    o1_interface.apply_configs({"o_ru_1": o_ru1, "o_du_1": o_du1})

    # Create UEs with different mobility models
    mobility_model1 = RandomWaypointModel(speed=5, area_size=(100, 100))
    ue1 = UE("ue_1", np.array([10, 10]), mobility_model1, scheduler)

    mobility_model2 = RandomWalkModel(step_size=2)
    ue2 = UE("ue_2", np.array([50, 50]), mobility_model2, scheduler)

    # Add UEs to the scheduler
    scheduler.add_ue(ue1)
    scheduler.add_ue(ue2)

    # Attach UEs to O-DUs
    ue1.attach_to_du(o_du1)
    ue2.attach_to_du(o_du1)

    # Create a data collector
    data_collector = CSVDataCollector("simulation_results.csv")

    # Run the simulation
    scheduler.run(until=10)

    # Collect and analyze data
    data_collector.collect_data({"time": scheduler.env.now, "ue_id": ue1.ue_id, "position": ue1.position})
    data_collector.collect_data({"time": scheduler.env.now, "ue_id": ue2.ue_id, "position": ue2.position})
    data_collector.write_data()

    # Analyze data
    analyzer = DataAnalyzer()
    try:
        df = analyzer.load_data_from_csv("simulation_results.csv")
        if df is not None:
            avg_x = analyzer.calculate_average(df, "position")
            print(f"Average X position: {avg_x}")
    except Exception as e:
        logging.error(f"Error during data analysis: {e}")

    # Visualize data
    visualizer = DataVisualizer()
    visualizer.plot_line(df, "time", "position", title="UE Position Over Time", xlabel="Time", ylabel="Position")

if __name__ == "__main__":
    main()