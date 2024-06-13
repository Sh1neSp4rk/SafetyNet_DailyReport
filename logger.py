import logging

# Create a logger
logger = logging.getLogger('SafetyNet_DailyReport')

# Set the logging level
logger.setLevel(logging.INFO)

# Create a file handler to log to a file
file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.INFO)

# Create a console handler to log to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and attach it to the handlers
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger