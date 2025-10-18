import os
import yaml
import time
import joblib
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_absolute_error
from src.utils.logger import get_logger

# Initialize logger once
logger = get_logger("evaluate.log")

CONFIG_PATH = "config.yaml"


def load_config(path: str = CONFIG_PATH) -> dict:
    """Load YAML configuration."""
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully.")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error while loading configuration: {e}")
        raise


def evaluate(features: np.ndarray, labels: np.ndarray) -> None:
    """Evaluate the trained model using cross-validation."""
    config = load_config()
    model_path = config["paths"].get("model_path", "models/model.joblib")

    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        raise FileNotFoundError(f"Model not found: {model_path}")

    try:
        logger.info("Loading trained model...")
        model = joblib.load(model_path)
        logger.info(f"Model loaded successfully: {model.__class__.__name__}")
    except Exception as e:
        logger.exception(f"Error loading model: {e}")
        raise

    try:
        logger.info("Starting model evaluation...")
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        scores = cross_val_score(model, features, labels, cv=cv, scoring="neg_mean_absolute_error")
        mean_mae = -scores.mean()

        logger.info("=" * 10 + " Model Evaluation " + "=" * 10)
        logger.info(f"Cross-validation MAE: {mean_mae:.4f}")

        # Optionally store metrics for DVC tracking
        # metrics = {"cross_val_MAE": round(mean_mae, 4)}
        # with open("metrics.json", "w") as f:
        #     yaml.safe_dump(metrics, f)
        # logger.info("Evaluation metrics saved to metrics.json.")

    except Exception as e:
        logger.exception(f"Unexpected error during evaluation: {e}")
        raise


def main():
    try:
        config = load_config()
        feature_path = config["paths"]["feature"]
        label_path = config["paths"]["labels"]

        X = np.load(feature_path)
        y = np.load(label_path)

        logger.info("Feature and label data loaded successfully.")
        evaluate(X, y)
    except Exception as e:
        logger.exception(f"Evaluation pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
