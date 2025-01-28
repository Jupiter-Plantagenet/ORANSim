from typing import Dict, Callable  

class E2Termination:  
    def __init__(self):  
        self.subscribers: Dict[str, Callable] = {}  # xApp ID → callback  

    def subscribe(self, xapp_id: str, callback: Callable):  
        """Register an xApp to receive E2 messages."""  
        self.subscribers[xapp_id] = callback  

    def publish(self, message: dict):  
        """Send E2 message to all subscribed xApps."""  
        for xapp_id, callback in self.subscribers.items():  
            callback(message)  