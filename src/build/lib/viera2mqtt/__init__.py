import logging
import os

def callback_loglevel(value):
    value = value.lower()

    if value == "info":
        return logging.INFO
    elif value == "debug":
        return logging.DEBUG
    elif value == "error":
        return logging.ERROR
    elif value == "warning":
        return logging.WARNING
    elif value == "critical":
        return logging.CRITICAL
    
    return logging.INFO

logging.basicConfig(
    level=callback_loglevel(os.environ.get("V2M_LOGLEVEL", "info")),
    format="%(asctime)s - %(levelname)-8s  - %(name)s - %(message)s",
)
