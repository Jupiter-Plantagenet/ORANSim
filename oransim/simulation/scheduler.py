import simpy
from typing import List
from oransim.core.mobility import UE

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

    def add_event(self, delay: float, callback, *args):
        """Schedule an event after `delay` seconds.

        Args:
            delay (float): The delay before the event is triggered, in seconds.
            callback (callable): The function to be called when the event is triggered.
            *args: Variable arguments to be passed to the callback.
        """
        self.env.process(self._event_wrapper(delay, callback, args))

    def _event_wrapper(self, delay, callback, args):
        """A wrapper for scheduling events"""
        yield self.env.timeout(delay)
        callback(*args)

    def run(self, until: float = 1000):
        """Run simulation for `until` virtual second.

        Args:
            until (float): The duration to run the simulation for, in seconds.
        """
        self.env.run(until=until)

    def add_ue(self, ue: UE):
        """Adds a UE to the simulation environment.
        
        Args:
            ue (UE): The UE object to add.
        """
        self.ues.append(ue)
        self.env.process(self._update_ue_position(ue))


    def _update_ue_position(self, ue: UE):
      """
        Updates the UE position at regular intervals using the mobility model.
      """
      while True:
          yield self.env.timeout(0.1) # Update every 0.1 second
          ue.update_position(0.1)