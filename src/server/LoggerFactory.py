import logging
import os


class LoggerFactory:
    def __init__(self, log_directory):
        self.log_directory = log_directory
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        log_file = os.path.join(self.log_directory, 'server.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
