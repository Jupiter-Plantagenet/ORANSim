import pytest  
from oransim.simulation.scheduler import ORANScheduler  

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