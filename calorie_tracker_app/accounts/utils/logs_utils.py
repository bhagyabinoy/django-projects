import logging

def set_log_file(file_name):
    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    # Create handlers
    c_handler = logging.FileHandler(file_name)
    c_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - : %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    return logger

#close log
def close_log(logger):
    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()