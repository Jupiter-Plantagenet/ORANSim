import logging
from typing import Callable, Any, Dict
from queue import Queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class F1Interface:
    """
    Simulates the F1 interface between the O-CU (O-CU-CP and O-CU-UP) and O-DU in the ORAN architecture.

    This implementation supports basic message passing and routing functionalities.
    """

    def __init__(self, scheduler):
        """
        Initializes the F1Interface.

        Args:
            scheduler: The simulation scheduler.
        """
        self.scheduler = scheduler
        self.message_queue: Queue = Queue()
        self.cu_up = None
        self.cu_cp = None
        self.du = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_cu_up(self, cu_up):
        """
        Sets the O-CU-UP for this F1 interface.

        Args:
            cu_up: The O-CU-UP instance.
        """
        self.cu_up = cu_up

    def set_cu_cp(self, cu_cp):
        """
        Sets the O-CU-CP for this F1 interface.

        Args:
            cu_cp: The O-CU-CP instance.
        """
        self.cu_cp = cu_cp

    def set_du(self, du):
        """
        Sets the O-DU for this F1 interface.

        Args:
            du: The O-DU instance.
        """
        self.du = du

    def send_message(self, message: Dict[str, Any], source_node: str, dest_node: str):
        """
        Sends a message over the F1 interface.

        Args:
            message (Dict[str, Any]): The message to send.
            source_node (str): The ID of the source node (e.g., "o-cu-cp", "o-cu-up", "o-du").
            dest_node (str): The ID of the destination node (e.g., "o-cu-cp", "o-cu-up", "o-du").
        """
        if source_node not in ["o_cu_cp", "o_cu_up", "o_du"]:
          raise ValueError(f"Invalid source node for F1 interface: {source_node}")
        if dest_node not in ["o_cu_cp", "o_cu_up", "o_du"]:
          raise ValueError(f"Invalid destination node for F1 interface: {dest_node}")

        self.message_queue.put((message, source_node, dest_node))
        self.scheduler.add_event(0, self._process_message_queue)  # Schedule message processing

    def _process_message_queue(self):
        """Processes the message queue and routes messages to the appropriate destination."""
        while not self.message_queue.empty():
            message, source_node, dest_node = self.message_queue.get()
            self.logger.info(f"F1 Interface: Sending message from {source_node} to {dest_node}: {message}")

            try:
                if dest_node == "o_cu_cp" and self.cu_cp:
                    self.cu_cp.receive_f1_message(message, source_node)
                elif dest_node == "o_cu_up" and self.cu_up:
                    self.cu_up.receive_f1_message(message, source_node)
                elif dest_node == "o_du" and self.du:
                    self.du.receive_f1_message(message, source_node)
                else:
                    self.logger.error(f"F1 Interface: Invalid destination node or node not set: {dest_node}")
            except Exception as e:
                self.logger.error(f"F1 Interface: Error processing message from {source_node} to {dest_node}: {e}")