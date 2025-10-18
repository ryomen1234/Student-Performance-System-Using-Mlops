import os
import time
import yaml
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from src.utils.logger import get_logger

CONFIG_PATH = "config.yaml"
MODEL_DIR = "models"
MODEL_FILENAME = "model.joblib"

logger = get_logger("train.log")

def load_config(path: str = CONFIG_PATH) -> dict:
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise

def train(features: np.ndarray, labels: np.ndarray, params: dict) -> GradientBoostingRegressor:
    model = GradientBoostingRegressor(**params)
    start = time.time()
    model.fit(features, labels)
    logger.info(f"Model trained in {time.time() - start:.2f} seconds")
     
    # save model.
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, MODEL_FILENAME))
    logger.info("Model saved successfully.")
    return model

def main():
    config = load_config()
    X = np.load(config["paths"]["feature"])
    y = np.load(config["paths"]["labels"])
    model_params = config["parameter"]
    train(X, y, model_params)

if __name__ == "__main__":
    main()
