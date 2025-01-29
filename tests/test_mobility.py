import pytest
import numpy as np
from oransim.core.mobility import RandomWalkModel, RandomWaypointModel, ManhattanModel, UE

def test_random_walk_model():
    model = RandomWalkModel(step_size=1.0)
    initial_position = np.array([0.0, 0.0])
    time_elapsed = 1.0
    new_position = model.update_position(initial_position, time_elapsed)
    assert isinstance(new_position, np.ndarray)
    assert new_position.shape == (2,)
    assert not np.array_equal(new_position, initial_position)  # position should have changed

def test_random_waypoint_model():
    model = RandomWaypointModel(speed=1.0, area_size=(10.0, 10.0), pause_time_mean=0.1, pause_time_std=0.0)
    initial_position = np.array([0.0, 0.0])
    time_elapsed = 0.1
    ue = UE(initial_position, model)

    # Move towards a new target
    new_position = model.update_position(ue.position, time_elapsed)

    # Ensure we are in the paused state before proceeding
    while not model.is_paused:
        new_position = model.update_position(ue.position, time_elapsed)
    
    assert model.is_paused is True # Check if it is paused

    # check that the position doesn't change during the pause
    initial_pause_position = ue.position.copy()
    for _ in range(10):
      new_position = model.update_position(ue.position, 0.01)
      assert np.all(np.abs(new_position - initial_pause_position) < 1e-6) #UE should not move in pause
      initial_pause_position = new_position.copy()


    # check if we can set a new target and it will move towards it
    model.pause_timer = 100.0 # force the timer to finish
    for _ in range(10):
      new_position = model.update_position(ue.position, time_elapsed)
      if not np.array_equal(new_position, ue.position):
        break
    assert not np.array_equal(new_position, ue.position)

def test_manhattan_model():
    model = ManhattanModel(speed=1.0, grid_size=(3, 3), block_size=1.0)
    initial_position = np.array([1.0, 1.0])
    time_elapsed = 1.0
    ue = UE(initial_position, model)
    for _ in range(10):
      new_position = model.update_position(ue.position, time_elapsed)
      if not np.array_equal(new_position, initial_position):
        break

    assert isinstance(new_position, np.ndarray)
    assert new_position.shape == (2,)

    # ensure the UE moved to a different row or column
    assert not np.array_equal(new_position, initial_position)
    assert (int(new_position[0] // model.block_size) != int(initial_position[0] // model.block_size)) or (int(new_position[1] // model.block_size) != int(initial_position[1] // model.block_size))