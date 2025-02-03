import pytest
from oransim.simulation.scheduler import ORANScheduler
from oransim.core.mobility import UE, RandomWalkModel
import numpy as np

class MockNearRTRIC:
    def __init__(self):
      self.near_rt_ric_id = "near_rt_ric_1"

# Test Cases for ORANScheduler
def test_oranscheduler_initialization():
    scheduler = ORANScheduler()
    assert scheduler.env is not None
    assert scheduler.events == []
    assert scheduler.ues == []

def test_oranscheduler_add_event():
    scheduler = ORANScheduler()
    callback_executed = False

    def test_callback():
        nonlocal callback_executed
        callback_executed = True

    scheduler.add_event(1.0, test_callback)
    scheduler.run(until=2.0)
    assert callback_executed

def test_oranscheduler_add_event_negative_delay():
  scheduler = ORANScheduler()
  with pytest.raises(ValueError):
    scheduler.add_event(-1.0, lambda: None)

def test_oranscheduler_run_negative_time():
    scheduler = ORANScheduler()
    with pytest.raises(ValueError):
        scheduler.run(until=-1.0)

def test_oranscheduler_add_ue():
    scheduler = ORANScheduler()
    mobility_model = RandomWalkModel()
    ue = UE("ue_1", np.array([0, 0]), mobility_model, scheduler)
    scheduler.add_ue(ue)
    assert ue in scheduler.ues

def test_oranscheduler_run_until():
    scheduler = ORANScheduler()
    mobility_model = RandomWalkModel()
    ue = UE("ue_1", np.array([0, 0]), mobility_model, scheduler)
    scheduler.add_ue(ue)
    assert scheduler.env.now == 0.0
    scheduler.run(until=5.0)
    assert scheduler.env.now == 5.0

def test_oranscheduler_get_near_rt_ric():
    scheduler = ORANScheduler()
    scheduler.near_rt_ric = MockNearRTRIC()
    assert isinstance(scheduler.get_near_rt_ric(), MockNearRTRIC)