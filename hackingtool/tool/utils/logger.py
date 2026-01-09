import logging
import os
from tool.config import LOGS_DIR

def setup_logger(name="ai_sec_tool"):
    """Sets up a logger that writes to file and console."""
    
    # Ensure log directory exists
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create handlers
    file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "app.log"))
    console_handler = logging.StreamHandler()
    
    # Set levels
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO) # Console is cleaner
    
    # Create formatters and add it to handlers
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_format = logging.Formatter('[%(levelname)s] %(message)s')
    
    file_handler.setFormatter(file_format)
    console_handler.setFormatter(console_format)
    
    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Global logger instance
logger = setup_logger()
