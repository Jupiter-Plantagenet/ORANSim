import logging
import numpy as np
from oransim.core.nodes import O_RU, O_DU, UE, DUConfig, RUConfig
from oransim.interfaces.o1 import O1Interface
from oransim.interfaces.e2 import E2Interface
from oransim.interfaces.f1 import F1Interface
from oransim.interfaces.xn import XnInterface
from oransim.interfaces.x2 import X2Interface
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create an xApp for handover optimization
class HandoverOptimizationXApp(XApp):
    def __init__(self, xapp_id: str, e2_interface: E2Interface, near_rt_ric):
        super().__init__(xapp_id, e2_interface, near_rt_ric)
        self.logger = logging.getLogger(self.__class__.__name__)

    def receive_indication(self, message: Dict[str, Any], du_id: str):
        super().receive_indication(message, du_id)
        self.logger.info(f"xApp {self.xapp_id} received indication message from O-DU {du_id}: {message}")

        # Implement your logic to process the message and send control messages
        # For example, check if handover is needed and send a control message to adjust handover parameters

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

    # Create an xApp for handover optimization
    handover_xapp = HandoverOptimizationXApp("handover_xapp_1", e2_interface, near_rt_ric)
    handover_xapp.register()

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