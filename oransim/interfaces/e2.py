import json
import logging
from typing import Callable, Any, Dict
from queue import Queue

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class E2Interface:
    """
    Simulates the E2 interface between the Near-RT RIC and E2 nodes (e.g., O-DUs, O-CUs) in the ORAN architecture.

    This implementation supports basic message passing and subscription mechanisms.
    """

    def __init__(self, near_rt_ric, scheduler):
        """
        Initializes the E2Interface.

        Args:
            near_rt_ric: The Near-RT RIC instance.
            scheduler: The simulation scheduler.
        """
        self.near_rt_ric = near_rt_ric
        self.scheduler = scheduler
        self.e2_subscribers: Dict[str, Callable[[Dict[str, Any], str], None]] = {}
        self.message_queue: Queue = Queue()
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_message(self, message: Dict[str, Any], node_id: str):
        """
        Sends a message from an E2 node to the Near-RT RIC.

        Args:
            message (Dict[str, Any]): The message to send.
            node_id (str): The ID of the E2 node sending the message.
        """
        self.message_queue.put((message, node_id))
        self.scheduler.add_event(0, self._process_message_queue)  # Schedule message processing

    def _process_message_queue(self):
        """Processes the message queue, routing messages to subscribers."""
        while not self.message_queue.empty():
            message, node_id = self.message_queue.get()
            self.logger.info(f"E2 Interface: Near-RT RIC received message from E2 node {node_id}: {message}")

            # In a real implementation, you might determine the message type and route it to specific handlers/subscribers
            for subscriber_id, callback in self.e2_subscribers.items():
                try:
                    callback(message, node_id)
                except Exception as e:
                    self.logger.error(f"Error in subscriber {subscriber_id} when processing message: {e}")

    def send_indication(self, message: Dict[str, Any], du_id: str):
        """
        Sends an indication message from the Near-RT RIC to subscribed xApps.
        This is a placeholder for a more sophisticated subscription/publication mechanism.

        Args:
            message (Dict[str, Any]): The indication message to send.
            du_id (str): The ID of the DU the message originated from.
        """
        # In a real implementation, you would have a more sophisticated subscription mechanism
        # based on message type, E2 Node ID, etc.
        for subscriber_id, callback in self.e2_subscribers.items():
            try:
                callback(message, du_id)
                self.logger.info(f"E2 Interface: Sent indication message to xApp {subscriber_id}")
            except Exception as e:
                self.logger.error(f"Error sending indication to xApp {subscriber_id}: {e}")

    def subscribe(self, subscriber_id: str, callback: Callable[[Dict[str, Any], str], None]):
        """
        Subscribes an xApp or other component to receive messages from the E2 interface.

        Args:
            subscriber_id (str): The ID of the subscriber (e.g., xApp ID).
            callback (Callable[[Dict[str, Any]], None]): The callback function to be called when a message is received.
                                                        The callback function should accept two arguments:
                                                        1. The message (Dict[str, Any]).
                                                        2. The ID of the E2 node that sent the message.
        """
        if not isinstance(subscriber_id, str):
            raise TypeError("subscriber_id must be a string")
        if not callable(callback):
            raise TypeError("callback must be a callable function")

        self.e2_subscribers[subscriber_id] = callback
        self.logger.info(f"E2 Interface: xApp {subscriber_id} subscribed to E2 messages")

    def unsubscribe(self, subscriber_id: str):
        """
        Unsubscribes an xApp or other component from receiving messages.

        Args:
            subscriber_id (str): The ID of the subscriber to unsubscribe.
        """
        if subscriber_id in self.e2_subscribers:
            del self.e2_subscribers[subscriber_id]
            self.logger.info(f"E2 Interface: xApp {subscriber_id} unsubscribed from E2 messages")
        else:
            self.logger.warning(f"E2 Interface: Attempted to unsubscribe unknown xApp: {subscriber_id}")