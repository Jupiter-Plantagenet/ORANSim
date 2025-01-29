import pytest  
from oransim.simulation.scheduler import ORANScheduler  
import pytest
import numpy as np
import simpy
from oransim.simulation.scheduler import ORANScheduler
from oransim.core.mobility import RandomWalkModel, UE

class TestScheduler:  
    def test_event_scheduling(self):  
        scheduler = ORANScheduler()  
        triggered = [False]  

        def set_triggered():  
            triggered[0] = True  

        scheduler.add_event(delay=5.0, callback=set_triggered)  
        scheduler.run(until=6.0)  
        assert triggered[0]  

    def test_multiple_events(self):  
        scheduler = ORANScheduler()  
        counter = [0]  

        def increment():  
            counter[0] += 1  

        scheduler.add_event(1.0, increment)  
        scheduler.add_event(3.0, increment)  
        scheduler.run(until=4.0)  
        assert counter[0] == 2  


    def test_ue_mobility_integration(self):
        scheduler = ORANScheduler()
        initial_position = np.array([0.0, 0.0])
        mobility_model = RandomWalkModel(step_size=1.0)
        ue = UE(initial_position, mobility_model)
    
        scheduler.add_ue(ue)
    
        scheduler.run(until=1.0)  # run for 1 second
    
        assert not np.array_equal(ue.position, initial_position) # Position should have changed