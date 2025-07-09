import logging
import os
from datetime import datetime

def setup_logger(name="wbru_playcounts"):
    """Set up logger with file and console handlers"""
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler - daily log files
    today = datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(f"{logs_dir}/wbru_playcounts_{today}.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_date_string():
    """Get current date in day.month.year format"""
    return datetime.now().strftime("%d.%m.%Y")

def get_playcount_column_name():
    """Get column name for current date's playcounts"""
    return f"Playcounts {get_date_string()}"