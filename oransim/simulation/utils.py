import logging
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

"""
Utility functions for the ORAN simulation environment.
"""

def calculate_distance(node1, node2):
    """
    Calculates the Euclidean distance between two nodes.

    Args:
        node1: The first node (must have a 'position' attribute, e.g., a UE or O-RU).
        node2: The second node (must have a 'position' attribute).

    Returns:
        float: The distance between the two nodes.
    """
    if not hasattr(node1, 'position') or not hasattr(node2, 'position'):
        raise ValueError("Both nodes must have a 'position' attribute")

    if not isinstance(node1.position, (list, tuple, np.ndarray)) or not isinstance(node2.position, (list, tuple, np.ndarray)):
        raise TypeError("Node positions must be list-like (list, tuple, or NumPy array)")

    if len(node1.position) != 2 or len(node2.position) != 2:
        raise ValueError("Node positions must be 2-dimensional (x, y)")

    x1, y1 = node1.position
    x2, y2 = node2.position
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

# Add more utility functions as needed for the simulation, e.g.,
# - Functions for converting between different units (e.g., dBm to mW).
# - Functions for calculating SINR, throughput, etc.
# - Functions for generating traffic.
# - Functions for creating and managing network topologies.