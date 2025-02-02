import pytest
import numpy as np
from oransim.core.mobility import (
    RandomWalkModel,
    RandomWaypointModel,
    ManhattanModel,
    UE,
)

# Test Cases for RandomWalkModel
def test_random_walk_model_initialization():
    model = RandomWalkModel(step_size=2.0)
    assert model.step_size == 2.0

def test_random_walk_model_update_position():
    model = RandomWalkModel(step_size=1.0)
    initial_position = np.array([0.0, 0.0])
    time_elapsed = 0.5
    new_position = model.update_position(initial_position, time_elapsed)
    assert isinstance(new_position, np.ndarray)
    assert new_position.shape == (2,)
    distance = np.linalg.norm(new_position - initial_position)
    assert np.isclose(distance, model.step_size * time_elapsed)

# Test Cases for RandomWaypointModel
def test_random_waypoint_model_initialization():
    model = RandomWaypointModel(speed=2.0, area_size=(10, 20), pause_time_mean=1.0, pause_time_std=0.5)
    assert model.speed == 2.0
    assert model.area_size == (10, 20)
    assert model.pause_time_mean == 1.0
    assert model.pause_time_std == 0.5

def test_random_waypoint_model_update_position():
    model = RandomWaypointModel(speed=1.0, area_size=(100, 100), pause_time_mean=0.1, pause_time_std=0.0)
    initial_position = np.array([0.0, 0.0])
    time_elapsed = 0.5  # Shorter than pause time

    # Test movement towards the first waypoint
    new_position = model.update_position(initial_position, time_elapsed)
    assert isinstance(new_position, np.ndarray)
    assert new_position.shape == (2,)
    assert not np.array_equal(new_position, initial_position)  # Position should have changed

    # Test pause at waypoint
    model.is_paused = True
    model.pause_timer = 0
    paused_position = model.update_position(new_position, time_elapsed)
    assert np.allclose(paused_position, new_position)  # Position should not change during pause

    # Test movement towards a new waypoint after pause
    model.is_paused = False
    model.target = None  # Reset target to choose a new one
    moved_position = model.update_position(paused_position, time_elapsed)
    assert not np.array_equal(moved_position, paused_position)  # Position should change again

# Test Cases for ManhattanModel
def test_manhattan_model_initialization():
    model = ManhattanModel(speed=1.0, grid_size=(5, 5), block_size=10.0)
    assert model.speed == 1.0
    assert model.grid_size == (5, 5)
    assert model.block_size == 10.0

def test_manhattan_model_update_position():
    model = ManhattanModel(speed=5.0, grid_size=(5, 5), block_size=10.0)
    initial_position = np.array([5.0, 5.0])  # Center of a block
    time_elapsed = 1.0

    # Test movement to a new block
    model.target = np.array([15.0, 5.0])  # Move to the right
    new_position = model.update_position(initial_position, time_elapsed)
    assert isinstance(new_position, np.ndarray)
    assert new_position.shape == (2,)
    assert np.allclose(new_position, np.array([10.0, 5.0]))  # Moved to the edge of the block

    # Test reaching a target block
    model.target = np.array([15.0, 5.0])
    reached_position = model.update_position(new_position, time_elapsed)
    assert np.allclose(reached_position, model.target)  # Reached the target

    # Test choosing a new target after reaching the target
    model.target = None
    new_target_position = model.update_position(reached_position, time_elapsed)
    assert not np.array_equal(new_target_position, reached_position)  # Position should have changed