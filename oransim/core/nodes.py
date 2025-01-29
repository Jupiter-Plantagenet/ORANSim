from dataclasses import dataclass  
from oransim.core.interfaces.e2 import E2Termination  
import numpy as np  
import random  
from typing import Optional  


@dataclass  
class BaseStationConfig:  
    cell_id: int  
    max_ues: int = 100  
    transmit_power: float = 46.0  # dBm  

#class O_DU:  
#    def __init__(self, config: BaseStationConfig, e2_term: E2Termination):  
#        self.config = config  
#        self.e2_term = e2_term  
#        self.connected_ues = []  
#3
#   def report_load(self):  
#        """Send E2SM-KPM message to Near-RT RIC when load exceeds threshold."""  
#        load = len(self.connected_ues) / self.config.max_ues  
#        if load > 0.7:  
#            message = {  
#                "cell_id": self.config.cell_id,  
#                "metric": "cell_load",  
#                "value": load  
#            }  
#            self.e2_term.publish(message)  

class O_DU:  
    def __init__(self, config: BaseStationConfig, scheduler):  
        self.config = config  
        self.scheduler = scheduler  
        self.received_iq = []  

    def receive_iq_data(self, iq_data: np.ndarray):  
        """Callback for fronthaul IQ data from O-RU"""  
        self.received_iq.append(iq_data)  
        print(f"O-DU {self.config.cell_id} received IQ data of shape {iq_data.shape}")  
    
    def apply_o1_config(self, config: dict):
      """Applies O1 configurations to O_DU."""
      if "max_ues" in config:
          self.config.max_ues = config["max_ues"]
      if "transmit_power" in config:
          self.config.transmit_power = config["transmit_power"]

      print(f"O-DU {self.config.cell_id} configured with O1: {config}")


@dataclass  
class RUConfig:  
    ru_id: int  
    frequency: float = 3.5e9  # 3.5 GHz  
    bandwidth: float = 100e6  # 100 MHz  
    tx_power: float = 46.0    # dBm  
    iq_samples_per_slot: int = 1024  # For fronthaul IQ simulation  

class O_RU:  
    def __init__(self, config: RUConfig, scheduler):  
        self.config = config  
        self.scheduler = scheduler  # ORANScheduler instance  
        self.connected_ues = set()  
        self.iq_buffer = []  

    def generate_iq_data(self) -> np.ndarray:  
        """Simulate IQ samples (complex numbers) for fronthaul transmission."""  
        iq = np.random.normal(0, 1, self.config.iq_samples_per_slot) + 1j * np.random.normal(0, 1, self.config.iq_samples_per_slot)  
        return iq  

    def send_iq_data(self, target_du):  
        """Transmit IQ data to O-DU via fronthaul with simulated latency/jitter."""  
        iq_data = self.generate_iq_data()  
        latency = max(0.001, random.normalvariate(0.1, 0.02))  # 100ms ±20ms  
        self.scheduler.add_event(latency, target_du.receive_iq_data, iq_data)
    
    def apply_o1_config(self, config: dict):
        """Applies O1 configurations to O_RU."""
        if "frequency" in config:
            self.config.frequency = config["frequency"]
        if "bandwidth" in config:
            self.config.bandwidth = config["bandwidth"]
        if "tx_power" in config:
          self.config.tx_power = config["tx_power"]
        print(f"O-RU {self.config.ru_id} configured with O1: {config}")