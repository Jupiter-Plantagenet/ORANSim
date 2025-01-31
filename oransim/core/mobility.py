from abc import ABC, abstractmethod
from typing import Tuple, List
import numpy as np
import random

class MobilityModel(ABC):
    """
    Abstract base class for UE mobility models.
    """
    @abstractmethod
    def update_position(self, current_position: np.ndarray, time_elapsed: float) -> np.ndarray:
        """
        Updates the UE position based on the mobility model.

        Args:
            current_position (np.ndarray): The current position of the UE as a 2D array (x, y).
            time_elapsed (float): The time elapsed since the last update, in seconds.

        Returns:
            np.ndarray: The updated position of the UE as a 2D numpy array (x, y).
        """
        pass

class UE:
    """
    Represents a User Equipment (UE) with a mobility model.
    """
    def __init__(self, ue_id: str, initial_position: np.ndarray, mobility_model: MobilityModel, scheduler):
        """
        Initializes a UE with a mobility model.

        Args:
            ue_id (str): Unique identifier for the UE.
            initial_position (np.ndarray): The initial position of the UE as a 2D numpy array (x, y).
            mobility_model (MobilityModel): The mobility model for the UE.
            scheduler: The simulation scheduler.
        """
        self.ue_id = ue_id
        self.position = initial_position
        self.mobility_model = mobility_model
        self.scheduler = scheduler
        self.o_du = None  # The O-DU the UE is currently connected to

    def update_position(self, time_elapsed: float) -> None:
        """
        Updates the UE's position using its mobility model.

        Args:
            time_elapsed (float): The time elapsed since the last update, in seconds.
        """
        self.position = self.mobility_model.update_position(self.position, time_elapsed)

    def attach_to_du(self, o_du):
        """Attaches the UE to a given O-DU."""
        if self.o_du is not None:
            self.detach_from_du()  # Detach from the current O-DU if connected
        self.o_du = o_du
        o_du.connected_ues.append(self)
        print(f"UE {self.ue_id} attached to O-DU {o_du.config.du_id}")

    def detach_from_du(self):
        """Detaches the UE from its current O-DU."""
        if self.o_du is not None:
            self.o_du.connected_ues.remove(self)
            print(f"UE {self.ue_id} detached from O-DU {self.o_du.config.du_id}")
            self.o_du = None

class RandomWalkModel(MobilityModel):
    """
    A simple random walk mobility model. The UE moves in a random direction at each step.
    """

    def __init__(self, step_size: float = 1.0):
        """
        Initializes the RandomWalkModel.

        Args:
            step_size (float): The distance the UE moves in each step, in meters.
        """
        self.step_size = step_size

    def update_position(self, current_position: np.ndarray, time_elapsed: float) -> np.ndarray:
        """
        Updates the UE position using the random walk model.

        Args:
            current_position (np.ndarray): The current position of the UE as a 2D array (x, y).
            time_elapsed (float): The time elapsed since the last update, in seconds.

        Returns:
            np.ndarray: The updated position of the UE.
        """
        angle = random.uniform(0, 2 * np.pi)
        dx = self.step_size * np.cos(angle) * time_elapsed
        dy = self.step_size * np.sin(angle) * time_elapsed
        return current_position + np.array([dx, dy])

class RandomWaypointModel(MobilityModel):
    """
    A random waypoint mobility model. The UE moves towards a randomly chosen waypoint,
    pauses for a random duration, and then chooses a new waypoint.
    """

    def __init__(self, speed: float = 1.0, area_size: Tuple[float, float] = (100.0, 100.0),
                 pause_time_mean: float = 5.0, pause_time_std: float = 2.0, tolerance: float = 1e-6):
        """
        Initializes the RandomWaypointModel.

        Args:
            speed (float): The speed at which the UE moves, in meters per second.
            area_size (Tuple[float, float]): The size of the simulation area (width, height), in meters.
            pause_time_mean (float): The average pause time at a waypoint, in seconds.
            pause_time_std (float): The standard deviation of the pause time at a waypoint, in seconds.
            tolerance (float): The tolerance for checking equality to a target location, in meters.
        """
        self.speed = speed
        self.area_size = area_size
        self.pause_time_mean = pause_time_mean
        self.pause_time_std = pause_time_std
        self.target = None
        self.pause_timer = 0.0
        self.is_paused = False
        self.tolerance = tolerance

    def update_position(self, current_position: np.ndarray, time_elapsed: float) -> np.ndarray:
        """
        Updates the UE position based on the random waypoint model.

        Args:
            current_position (np.ndarray): The current position of the UE as a 2D array (x, y).
            time_elapsed (float): The time elapsed since the last update, in seconds.

        Returns:
            np.ndarray: The updated position of the UE.
        """
        if self.is_paused:
            self.pause_timer += time_elapsed
            if self.pause_timer >= max(0.0, random.normalvariate(self.pause_time_mean, self.pause_time_std)):
                self.is_paused = False
                self.pause_timer = 0.0
            return current_position

        if self.target is None or np.all(np.abs(current_position - self.target) < self.tolerance):
            self.target = np.array([random.uniform(0, self.area_size[0]), random.uniform(0, self.area_size[1])])
            self.is_paused = True  # Set the is_paused flag to true when a new target is reached
            return current_position

        direction = self.target - current_position
        distance = np.linalg.norm(direction)
        if distance < self.speed * time_elapsed:
            return self.target
        else:
            unit_direction = direction / distance
            return current_position + unit_direction * self.speed * time_elapsed

class ManhattanModel(MobilityModel):
    """
    A Manhattan mobility model where UEs move on a grid, like in a city.
    """

    def __init__(self, speed: float = 1.0, grid_size: Tuple[int, int] = (10, 10), block_size: float = 10.0):
        """
        Initializes the ManhattanModel.

        Args:
            speed (float): The speed at which the UE moves, in meters per second.
            grid_size (Tuple[int, int]): The size of the grid (rows, columns).
            block_size (float): The size of each block in the grid, in meters.
        """
        self.speed = speed
        self.grid_size = grid_size
        self.block_size = block_size
        self.current_direction = None
        self.target = None

    def update_position(self, current_position: np.ndarray, time_elapsed: float) -> np.ndarray:
        """
        Updates the UE position based on a Manhattan grid.

        Args:
            current_position (np.ndarray): The current position of the UE as a 2D array (x, y).
            time_elapsed (float): The time elapsed since the last update, in seconds.

        Returns:
            np.ndarray: The updated position of the UE.
        """
        if self.target is None or np.all(current_position == self.target):
            current_row = int(current_position[1] // self.block_size)
            current_col = int(current_position[0] // self.block_size)

            possible_moves = []
            if current_row > 0:
                possible_moves.append(np.array([current_col, current_row - 1]))
            if current_row < self.grid_size[0] - 1:
                possible_moves.append(np.array([current_col, current_row + 1]))
            if current_col > 0:
                possible_moves.append(np.array([current_col - 1, current_row]))
            if current_col < self.grid_size[1] - 1:
                possible_moves.append(np.array([current_col + 1, current_row]))

            self.target = random.choice(possible_moves) * self.block_size
            return current_position

        direction = self.target - current_position
        distance = np.linalg.norm(direction)
        if distance < self.speed * time_elapsed:
            return self.target
        else:
            unit_direction = direction / distance
            return current_position + unit_direction * self.speed * time_elapsed