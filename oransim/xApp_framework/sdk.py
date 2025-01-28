from functools import wraps  

def on_e2_message(e2_term: E2Termination, xapp_id: str):  
    """Decorator to bind an xApp function to E2 messages."""  
    def decorator(func):  
        @wraps(func)  
        def wrapper(message: dict):  
            return func(message)  
        e2_term.subscribe(xapp_id, wrapper)  
        return wrapper  
    return decorator  