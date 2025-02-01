import logging
from typing import Callable, Any, Dict
from queue import Queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class XnInterface:
    """
    Simulates the Xn interface in the 5G ORAN architecture.

    The Xn interface is used for communication between peer gNBs (or ng-eNBs in non-standalone mode) 
    for supporting mobility and control procedures between nodes.

    This implementation supports basic message passing and routing functionalities.
    """

    def __init__(self, scheduler):
        """
        Initializes the XnInterface.

        Args:
            scheduler: The simulation scheduler.
        """
        self.scheduler = scheduler
        self.message_queue: Queue = Queue()
        self.nodes: Dict[str, Any] = {}  # Registered nodes (e.g., gNBs)
        self.logger = logging.getLogger(self.__class__.__name__)

    def register_node(self, node_id: str, node):
        """
        Registers a node (e.g., gNB) with the Xn interface.

        Args:
            node_id (str): The ID of the node to register.
            node: The node instance.
        """
        if node_id in self.nodes:
            self.logger.warning(f"Node {node_id} already registered on Xn interface.")
            return

        self.nodes[node_id] = node
        self.logger.info(f"Node {node_id} registered on Xn interface.")

    def unregister_node(self, node_id: str):
        """
        Unregisters a node from the Xn interface.

        Args:
            node_id (str): The ID of the node to unregister.
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.logger.info(f"Node {node_id} unregistered from Xn interface.")
        else:
            self.logger.warning(f"Node {node_id} not found on Xn interface.")

    def send_message(self, message: Dict[str, Any], source_node_id: str, dest_node_id: str):
        """
        Sends a message over the Xn interface.

        Args:
            message (Dict[str, Any]): The message to send.
            source_node_id (str): The ID of the source node.
            dest_node_id (str): The ID of the destination node.
        """
        
        if source_node_id not in self.nodes:
            raise ValueError(f"Source node {source_node_id} not registered on Xn interface.")
        if dest_node_id not in self.nodes:
            raise ValueError(f"Destination node {dest_node_id} not registered on Xn interface.")

        self.message_queue.put((message, source_node_id, dest_node_id))
        self.scheduler.add_event(0, self._process_message_queue)  # Schedule message processing

    def _process_message_queue(self):
        """Processes the message queue and routes messages to the appropriate destination."""
        while not self.message_queue.empty():
            message, source_node_id, dest_node_id = self.message_queue.get()
            self.logger.info(f"Xn Interface: Sending message from {source_node_id} to {dest_node_id}: {message}")

            try:
                dest_node = self.nodes[dest_node_id]
                dest_node.receive_xn_message(message, source_node_id)
            except KeyError:
                self.logger.error(f"Xn Interface: Destination node not found: {dest_node_id}")
            except Exception as e:
                self.logger.error(f"Xn Interface: Error processing message from {source_node_id} to {dest_node_id}: {e}")