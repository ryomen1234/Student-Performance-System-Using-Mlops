import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_absolute_error

import os
import time
import yaml
import joblib
from src.utils.logger import get_logger


# define the logger
try:
    logger = get_logger("train.log")
    print(f"Logger defined successfully.")
except ModuleNotFoundError:
    Exception (f"Module Not Found Error.")
    raise
except Exception as e:
    Exception (f"Some unexcpected error occured.")
    raise

def train(features: np.ndarray, labels: np.ndarray) -> None:

    """
    this method train the model and evaluate using KFold method.

    args:
    features: numpy array of features.
      labels: numpy array of output.

    return:
    return the sklearn model.
    
    """
    
    # load parameter.
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        params = config["parameter"]
        logger.info("params loaded successfully.")
    except FileNotFoundError:
        logger.error("File Not Found Error.")
        raise
    except Exception as e:
        logger.info(f"Some unexpected error occured.")
        raise

    # train model.
    try:
        model = GradientBoostingRegressor(**params)
        
        start = time.time()  # start time 
        model.fit(features, labels)
        logger.info(f"Model training done in {time.time() - start}")


    except Exception as e:
        logger.error(f"Some Unexpected error occured: {e}")
        raise
    
    # save model.
    try:
        # model_path = "models"  # path where the models is saved.
        # os.makedirs(model_path, exist_ok=True) # ensure path exist.
        path_to_save_model = os.path.join("models", 'model.joblib')

        joblib.dump(model, path_to_save_model)
        logger.info(f"Model loaded successfully.")

    except Exception as e:
        logger.error(f"Some unexpected error occured.")
        raise



def main():
    pass

if __name__ == "__main__":
    main()