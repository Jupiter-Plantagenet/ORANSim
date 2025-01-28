import simpy  

class ORANScheduler:  
    def __init__(self):  
        self.env = simpy.Environment()  
        self.events = []  

    def add_event(self, delay: float, callback, *args):  
        """Schedule an event after `delay` seconds."""  
        self.env.process(self._event_wrapper(delay, callback, args))  

    def _event_wrapper(self, delay, callback, args):  
        yield self.env.timeout(delay)  
        callback(*args)  

    def run(self, until: float = 1000):  
        """Run simulation for `until` virtual seconds."""  
        self.env.run(until=until)  