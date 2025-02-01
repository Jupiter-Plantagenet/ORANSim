import simpy
from typing import List, Callable, Any
from oransim.core.mobility import UE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ORANScheduler:
    """
    A discrete-event simulation scheduler using SimPy.

    This class manages the simulation environment, schedules events,
    and handles UE mobility. It uses SimPy to simulate the timing of events.
    """

    def __init__(self):
        """
        Initializes the ORANScheduler.

        Creates a SimPy environment and initializes the event and UE lists.
        """
        self.env = simpy.Environment()
        self.events = []
        self.ues: List[UE] = []  # List to store UEs
        self.logger = logging.getLogger(self.__class__.__name__)
        self.e2_interface = None

    def set_e2_interface(self, e2_interface):
        """
        Sets the E2 interface for this scheduler.

        Args:
            e2_interface: The E2 interface to set.
        """
        self.e2_interface = e2_interface

    def add_event(self, delay: float, callback: Callable, *args):
        """
        Schedules an event to be executed after a given delay.

        Args:
            delay (float): The delay before the event is triggered, in seconds.
            callback (callable): The function to be called when the event is triggered.
            *args: Variable arguments to be passed to the callback function.
        """

        if delay < 0:
            raise ValueError("Delay time cannot be negative")

        def event_wrapper():
            yield self.env.timeout(delay)
            try:
                callback(*args)
            except Exception as e:
                self.logger.error(f"Error in callback {callback.__name__}: {e}")

        self.env.process(event_wrapper())

    def add_ue(self, ue: UE):
        """
        Adds a UE to the simulation environment and starts its mobility process.

        Args:
            ue (UE): The UE object to add.
        """
        self.ues.append(ue)
        self.env.process(self._ue_mobility_process(ue))
        self.logger.info(f"Added UE {ue.ue_id} to simulation environment at position {ue.position}")

    def _ue_mobility_process(self, ue: UE):
        """
        Updates the UE position at regular intervals based on its mobility model.
        This method runs as a SimPy process.

        Args:
            ue (UE): The UE instance.
        """
        while True:
            yield self.env.timeout(0.1)  # Update every 0.1 seconds (configurable)
            ue.update_position(0.1)  # Update position based on mobility model
            self.logger.debug(f"UE {ue.ue_id} updated position to: {ue.position}")

    def run(self, until: float = 1000):
        """
        Runs the simulation until the specified time.

        Args:
            until (float): The simulation time to run until, in seconds.
        """
        if until <= self.env.now:
            raise ValueError("'until' value must be greater than current simulation time")

        self.logger.info(f"Starting simulation until time {until}...")
        self.env.run(until=until)
        self.logger.info("Simulation finished.")

    def get_near_rt_ric(self):
        """
        Returns the Near-RT RIC instance.

        This is a placeholder for a more sophisticated mechanism to access 
        network components.
        """
        # In a more complex implementation, you might need a more sophisticated
        # way to access different components, like a registry or a lookup table.
        return self.near_rt_ric