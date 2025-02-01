import logging
from typing import Any
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class OpenFronthaulInterface:
    """
    Simulates the Open Fronthaul interface between the O-RU and O-DU in the ORAN architecture.

    This implementation supports basic IQ data transfer with simulated latency and jitter.
    """

    def __init__(self, scheduler, latency_mean: float = 0.1, latency_std: float = 0.02, jitter_std: float = 0.005):
        """
        Initializes the OpenFronthaulInterface.

        Args:
            scheduler: The simulation scheduler.
            latency_mean (float): Mean latency introduced by the fronthaul in seconds. Defaults to 0.1.
            latency_std (float): Standard deviation of latency introduced by the fronthaul in seconds. Defaults to 0.02.
            jitter_std (float): Standard deviation of jitter (latency variation) in seconds. Defaults to 0.005.
        """
        self.scheduler = scheduler
        self.latency_mean = latency_mean
        self.latency_std = latency_std
        self.jitter_std = jitter_std
        self.o_ru = None
        self.o_du = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_o_ru(self, o_ru):
        """
        Sets the O-RU for this interface.

        Args:
            o_ru: The O-RU instance.
        """
        self.o_ru = o_ru

    def set_o_du(self, o_du):
        """
        Sets the O-DU for this interface.

        Args:
            o_du: The O-DU instance.
        """
        self.o_du = o_du

    def transmit_iq_data(self, iq_data: np.ndarray, o_ru, o_du):
        """
        Transmits IQ data from the O-RU to the O-DU over the Open Fronthaul interface.

        Args:
            iq_data (np.ndarray): The IQ data to transmit.
            o_ru: The source O-RU instance.
            o_du: The destination O-DU instance.
        """
        if o_ru != self.o_ru:
            raise ValueError("Invalid O-RU instance passed to transmit_iq_data")
        if o_du != self.o_du:
            raise ValueError("Invalid O-DU instance passed to transmit_iq_data")

        latency = self._calculate_latency()
        self.scheduler.add_event(latency, self.o_du.receive_iq_data, iq_data)
        self.logger.info(f"Open Fronthaul Interface: Transmitting IQ data from O-RU {o_ru.config.ru_id} to O-DU {o_du.config.du_id} with latency {latency:.4f} seconds")

    def _calculate_latency(self) -> float:
        """
        Calculates the latency for transmitting IQ data, including jitter.

        Returns:
            float: The total latency in seconds.
        """
        latency = np.random.normal(self.latency_mean, self.latency_std)
        jitter = np.random.normal(0, self.jitter_std)
        total_latency = max(0, latency + jitter)  # Ensure latency is not negative
        return total_latency