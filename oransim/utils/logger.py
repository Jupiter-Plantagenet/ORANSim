import logging
import os

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a logger with the given name, log file, and level.

    Args:
        name (str): The name of the logger.
        log_file (str, optional): The path to the log file. If None, logs to console only. Defaults to None.
        level (int, optional): The logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: The configured logger instance.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if log_file:
        # Create directory for log file if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()  # Log to console

    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False  # Prevent logs from being propagated to the root logger

    return logger

# Example usage:
# logger = setup_logger(__name__, "logs/simulation.log", logging.DEBUG)
# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")