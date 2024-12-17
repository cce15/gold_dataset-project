import os
import requests
import shutil
import coloredlogs, logging

# # Configure logging to a file
logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the log level

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set the log level for the console handler
# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)



# # Create a logger object.
# logger = logging.getLogger(__name__)
#
# # By default the install() function installs a handler on the root logger,
# # this means that log messages from your code and log messages from the
# # libraries that you use will all show up on the terminal.
# coloredlogs.install(level='DEBUG')
#
# # If you don't want to see log messages from libraries, you can pass a
# # specific logger object to the install() function. In this case only log
# # messages originating from that logger will show up on the terminal.
# coloredlogs.install(level='DEBUG', logger=logger)

# Some examples.
# logger.debug("this is a debugging message")
# logger.info("this is an informational message")
# logger.warning("this is a warning message")
# logger.error("this is an error message")
# logger.critical("this is a critical message")

def delete_files_and_folders(directory):
    """
    Delete all files and folders within the specified directory.

    :param directory: The path to the directory from which to delete files and folders.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        logger.warning(f"The directory {directory} does not exist.")
        return

    # Iterate over all the files and folders in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        try:
            # Check if it is a file
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file
                logger.warning(f"File {file_path} has been deleted.")
            # Check if it is a directory
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory
                logger.warning(f"Directory {file_path} has been deleted.")
        except Exception as e:
            logger.error(f"Failed to delete {file_path}. Reason: {e}")

def internet_check():
    # URL to check
    url = "https://www.google.com"
    try:
        # Make a GET request using requests library
        response = requests.get(url)

        # If the status code is 200, proceed with Selenium
        if response.status_code == 200:
            logger.info("Internet is connected")
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Failed to check internet. Reason: {e}")
        return False

internet_check()