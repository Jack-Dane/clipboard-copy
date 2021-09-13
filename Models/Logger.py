
import logging


class Logger:

    def setupLogging(self, filepath):
        """
        Setup the logging file
        :param filepath: filepath of log file
        """
        logging.basicConfig(filename=filepath, level=logging.INFO)

    def loggingChange(self, change):
        """
        Log changes in file
        :param change: item that needs to be logged
        """
        logging.info(f"Clipboard Change {change}")
