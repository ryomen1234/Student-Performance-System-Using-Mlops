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


def evaluate(features: np.ndarray, labels: np.ndarray) -> None:
    # load model path.
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        model_path = config["paths"]["model_path"]
        logger.info(f"Model path loaded successfully.")
    except Exception as e:
        logger.error(f"Some Unexpected error occured: {e}")
        raise
    
    # load model
    try:
        model = joblib.load(model_path)
        cv = KFold(n_splits=3, shuffle=True, random_state=42)

        scores = cross_val_score(model, features, labels, cv=cv, scoring="neg_mean_absolute_error")

        logger.info(f"{'='*10}Model Evaluation{'='*10}")
        logger.info(f"Model: {model.__class__.__name__}")

        logger.info(f"Cross-validation MAE: {-scores.mean():.3f}")
    except Exception as e:
        logger.error(f"Some unexpected error occured: {e}")
        raise