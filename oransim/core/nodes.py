import numpy as np
import random
from dataclasses import dataclass
from typing import Optional, Union, List, Dict, Any
from enum import Enum
from oransim.core.interfaces.o1 import ConfigStatus

class RUConfig:
    """
    Configuration class for O-RU.
    """
    def __init__(self,
                 ru_id: str,
                 frequency: float = 3.5e9,  # 3.5 GHz
                 bandwidth: float = 100e6,  # 100 MHz
                 tx_power: float = 46.0,  # dBm
                 iq_samples_per_slot: int = 1024,  # For fronthaul IQ simulation
                 cells: List[Dict[str, Any]] = None,
                 supported_operations: List[str] = None):
        self.ru_id = ru_id
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.tx_power = tx_power
        self.iq_samples_per_slot = iq_samples_per_slot
        self.cells = cells if cells is not None else []
        self.supported_operations = supported_operations if supported_operations is not None else []

class DUConfig:
    """
    Configuration class for O-DU.
    """
    def __init__(self,
                 du_id: str,
                 max_ues: int = 100,
                 schedulers: List[str] = None,
                 cells: List[Dict[str, Any]] = None):
        self.du_id = du_id
        self.max_ues = max_ues
        self.schedulers = schedulers if schedulers is not None else []
        self.cells = cells if cells is not None else []

class CUCPConfig:
    """
    Configuration class for O-CU-CP.
    """
    def __init__(self,
                 cucp_id: str,
                 control_schedulers: List[str] = None,
                 cells: List[Dict[str, Any]] = None):
        self.cucp_id = cucp_id
        self.control_schedulers = control_schedulers if control_schedulers is not None else []
        self.cells = cells if cells is not None else []

class CUUPConfig:
    """
    Configuration class for O-CU-UP.
    """
    def __init__(self,
                 cuup_id: str,
                 max_ues: int = 100,
                 qos_schedulers: List[str] = None,
                 cells: List[Dict[str, Any]] = None):
        self.cuup_id = cuup_id
        self.max_ues = max_ues
        self.qos_schedulers = qos_schedulers if qos_schedulers is not None else []
        self.cells = cells if cells is not None else []

class O_RU:
    """
    Represents an O-RAN Radio Unit (O-RU).
    """

    def __init__(self, config: RUConfig, scheduler):
        self.config = config
        self.scheduler = scheduler
        self.connected_ues = set()
        self.iq_buffer = []

    def generate_iq_data(self) -> np.ndarray:
        """Simulate IQ samples (complex numbers) for fronthaul transmission."""
        iq = np.random.normal(0, 1, self.config.iq_samples_per_slot) + 1j * np.random.normal(0, 1,
                                                                                             self.config.iq_samples_per_slot)
        return iq

    def send_iq_data(self, target_du):
        """Transmit IQ data to O-DU via fronthaul with simulated latency/jitter."""
        iq_data = self.generate_iq_data()
        latency = max(0.001, random.normalvariate(0.1, 0.02))  # 100ms ±20ms
        self.scheduler.add_event(latency, target_du.receive_iq_data, iq_data)

    def apply_o1_config(self, config: Dict[str, Any]):
        """Applies O1 configurations to O_RU."""
        if "frequency" in config:
            self.config.frequency = config["frequency"]
        if "bandwidth" in config:
            self.config.bandwidth = config["bandwidth"]
        if "tx_power" in config:
            self.config.tx_power = config["tx_power"]
        if "cells" in config:
            self.config.cells = config["cells"]
        if "supported_operations" in config:
            self.config.supported_operations = config["supported_operations"]

        print(f"O-RU {self.config.ru_id} configured with O1: {config}")

class O_DU:
    """
    Represents an O-RAN Distributed Unit (O-DU).
    """

    def __init__(self, config: DUConfig, scheduler: Any):
        self.config = config
        self.scheduler = scheduler
        self.received_iq = []
        self.connected_ues = []
        self.e2_node = None

    def set_e2_node(self, e2_node):
        """
        Sets the E2 node for this O-DU.

        Args:
            e2_node: The E2 node to set.
        """
        self.e2_node = e2_node

    def receive_iq_data(self, iq_data: np.ndarray):
        """Callback for fronthaul IQ data from O-RU"""
        self.received_iq.append(iq_data)
        print(f"O-DU {self.config.du_id} received IQ data of shape {iq_data.shape}")

    def report_load(self):
        """Send E2SM-KPM message to Near-RT RIC when load exceeds threshold."""
        load = len(self.connected_ues) / self.config.max_ues
        if load > 0.7:
            message = {
                "cell_id": self.config.du_id,
                "metric": "cell_load",
                "value": load
            }
            if self.e2_node:
                self.e2_node.send_message(message, self.config.du_id)

    def apply_o1_config(self, config: Dict[str, Any]):
        """Applies O1 configurations to O_DU."""
        if "max_ues" in config:
            self.config.max_ues = config["max_ues"]
        if "schedulers" in config:
            self.config.schedulers = config["schedulers"]
        if "cells" in config:
            self.config.cells = config["cells"]

        print(f"O-DU {self.config.du_id} configured with O1: {config}")

class O_CU_CP:
    """
    Represents an O-RAN Central Unit - Control Plane (O-CU-CP).
    """
    def __init__(self, config: CUCPConfig, scheduler):
        self.config = config
        self.scheduler = scheduler
        self.e2_node = None

    def set_e2_node(self, e2_node):
        """
        Sets the E2 node for this O-CU-CP.

        Args:
            e2_node: The E2 node to set.
        """
        self.e2_node = e2_node

    def apply_o1_config(self, config: Dict[str, Any]):
        """Applies O1 configurations to O_CU_CP."""
        if "control_schedulers" in config:
            self.config.control_schedulers = config["control_schedulers"]
        if "cells" in config:
            self.config.cells = config["cells"]
        print(f"O-CU-CP {self.config.cucp_id} configured with O1: {config}")

    # Add methods for handling control plane messages and interactions with O-DUs

class O_CU_UP:
    """
    Represents an O-RAN Central Unit - User Plane (O-CU-UP).
    """
    def __init__(self, config: CUUPConfig, scheduler):
        self.config = config
        self.scheduler = scheduler
        self.e2_node = None

    def set_e2_node(self, e2_node):
        """
        Sets the E2 node for this O-CU-UP.

        Args:
            e2_node: The E2 node to set.
        """
        self.e2_node = e2_node

    def apply_o1_config(self, config: Dict[str, Any]):
        """Applies O1 configurations to O_CU_UP."""
        if "qos_schedulers" in config:
            self.config.qos_schedulers = config["qos_schedulers"]
        if "cells" in config:
            self.config.cells = config["cells"]
        print(f"O-CU-UP {self.config.cuup_id} configured with O1: {config}")

    # Add methods for handling user plane data and interactions with O-DUs

class UE:
    """
    Represents a User Equipment (UE).
    """

    def __init__(self, ue_id: str, initial_position: np.ndarray, mobility_model, scheduler):
        self.ue_id = ue_id
        self.position = initial_position
        self.mobility_model = mobility_model
        self.scheduler = scheduler
        self.o_du = None  # The O-DU the UE is currently connected to

    def update_position(self, time_elapsed: float):
        """Updates the UE's position based on its mobility model."""
        self.position = self.mobility_model.update_position(self.position, time_elapsed)

    def attach_to_du(self, o_du):
        """Attaches the UE to a given O-DU."""
        self.o_du = o_du
        o_du.connected_ues.append(self)
        print(f"UE {self.ue_id} attached to O-DU {o_du.config.du_id}")

    def detach_from_du(self):
        """Detaches the UE from its current O-DU."""
        if self.o_du is not None:
            self.o_du.connected_ues.remove(self)
            print(f"UE {self.ue_id} detached from O-DU {self.o_du.config.du_id}")
            self.o_du = None