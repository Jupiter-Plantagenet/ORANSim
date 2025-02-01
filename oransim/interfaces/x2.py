import logging
from typing import Callable, Any, Dict
from queue import Queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class X2Interface:
    """
    Simulates the X2 interface in the ORAN architecture.

    The X2 interface is used for communication between eNBs in LTE and gNBs in 5G for handover and 
    inter-cell interference coordination.

    This implementation supports basic message passing and routing functionalities.
    """

    def __init__(self, scheduler):
        """
        Initializes the X2Interface.

        Args:
            scheduler: The simulation scheduler.
        """
        self.scheduler = scheduler
        self.message_queue: Queue = Queue()
        self.nodes: Dict[str, Any] = {}  # Registered nodes (e.g., eNBs, gNBs)
        self.logger = logging.getLogger(self.__class__.__name__)

    def register_node(self, node_id: str, node):
        """
        Registers a node (e.g., eNB, gNB) with the X2 interface.

        Args:
            node_id (str): The ID of the node to register.
            node: The node instance.
        """
        if node_id in self.nodes:
            self.logger.warning(f"Node {node_id} already registered on X2 interface.")
            return

        self.nodes[node_id] = node
        self.logger.info(f"Node {node_id} registered on X2 interface.")

    def unregister_node(self, node_id: str):
        """
        Unregisters a node from the X2 interface.

        Args:
            node_id (str): The ID of the node to unregister.
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.logger.info(f"Node {node_id} unregistered from X2 interface.")
        else:
            self.logger.warning(f"Node {node_id} not found on X2 interface.")

    def send_message(self, message: Dict[str, Any], source_node_id: str, dest_node_id: str):
        """
        Sends a message over the X2 interface.

        Args:
            message (Dict[str, Any]): The message to send.
            source_node_id (str): The ID of the source node.
            dest_node_id (str): The ID of the destination node.
        """
        if source_node_id not in self.nodes:
            raise ValueError(f"Source node {source_node_id} not registered on X2 interface.")
        if dest_node_id not in self.nodes:
            raise ValueError(f"Destination node {dest_node_id} not registered on X2 interface.")

        self.message_queue.put((message, source_node_id, dest_node_id))
        self.scheduler.add_event(0, self._process_message_queue)  # Schedule message processing

    def _process_message_queue(self):
        """Processes the message queue and routes messages to the appropriate destination."""
        while not self.message_queue.empty():
            message, source_node_id, dest_node_id = self.message_queue.get()
            self.logger.info(f"X2 Interface: Sending message from {source_node_id} to {dest_node_id}: {message}")

            try:
                dest_node = self.nodes[dest_node_id]
                dest_node.receive_x2_message(message, source_node_id)
            except KeyError:
                self.logger.error(f"X2 Interface: Destination node not found: {dest_node_id}")
            except Exception as e:
                self.logger.error(f"X2 Interface: Error processing message from {source_node_id} to {dest_node_id}: {e}")