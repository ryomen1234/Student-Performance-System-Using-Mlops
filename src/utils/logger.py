import logging
import os
import yaml
from datetime import datetime


def get_logger(file_name: str) -> logging.Logger:
        """
        logs the the data in logs dir.
        args:
        file_name: str = file name of the log file(ex. pipeline.log, model.log).

        return:
        logger: logging.logger = logger object.

        """

        header = f"\n{'-'*60}\n--- Logger session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n{'-'*60}"
        print(header)
        
        try:
            # load the logs dir path
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
            
            logs_path = config["paths"]["logs_dir"] 
            
            # create logs dir
            os.makedirs(logs_path, exist_ok=True)
        except FileNotFoundError:
            raise
        except Exception as e:
            Exception (f"Some unexpected error occured: {e}")
            raise

        # define log file path
        file_path = os.path.join(logs_path, file_name)
        # create logger object
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # prevent duplicate logs if imported multiple times
        if not logger.handlers:
             # file handler
             file_handler = logging.FileHandler(file_path)
             file_handler.setFormatter(
                  logging.Formatter(
                       "%(asctime)s - %(levelname)s - %(message)s",
                       "%Y-%m-%d %H-%M-%S"
                  )
             )

             # concole handler
             console_handler = logging.StreamHandler()
             console_handler.setFormatter(
                  logging.Formatter(
                       "%(levelname)s - %(message)s",
                    )
                )
             
             # Add handlers to logger object
             logger.addHandler(file_handler)
             logger.addHandler(console_handler)
        
        return logger




