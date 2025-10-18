import pandas as pd
import numpy as np
from typing import Tuple

import os
from src.utils.logger import get_logger


"""
define logger for the logs.
"""
try:
    logger = get_logger("preprocessing.log")
    print(f"loger object created successfully.")
except ModuleNotFoundError:
    Exception(f"Module Not Found Error")
    raise
except Exception as e:
    Exception(f"Some unexpected error occured")
    raise


def preprocessing(data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    this method preprocess the data.
    1.remove Student id.
    2. standardize the data.

    args:
    data: dataframe object.

    return:
    Tuple of numpy array X and y.
    
    """
    try:
        data.drop(columns=['StudentID', 'GradeClass'], inplace=True)
        logger.info("unwanted features removed successfully.")

        X, y = data.drop(columns=['GPA']), data['GPA']
        logger.info("data split into X and y")

        X = X.values
        y = y.values
        logger.info(f"data convetred to numpy array: X dtype: {X.dtype}, y dtype: {y.dtype}")

        return X, y
    except Exception as e:
        logger.error(f"Some unexpected error occured: {e}")
        raise

    

def main():
    """
    this method first load the raw data.
    then preprocess it. save data in data preprocess dir.
    """

    try:

        data_path = r"E:\project\Student-Performance-System-Using-Mlops\data\raw\student.csv"
        df = pd.read_csv(data_path)
        logger.info(f"data loaded successfully from: {data_path}")

        X, y = preprocessing(df)
        logger.info(f"data pre-procssed successfully.")

        data_dir_path = r"data/preprocess"
        os.makedirs(data_dir_path, exist_ok=True)
        logger.info(f"data path for X, y created.")

        np.save(os.path.join(data_dir_path, 'features.npy'), X)
        np.save(os.path.join(data_dir_path, "labels.npy"), y)
        logger.info(f"X and y stored successfully.")

    except Exception as e:
        logger.info(f"Some unexpected error occured.")
    

if __name__ == "__main__":
    main()






      
      
      
    
 
  
  
  
      
    
  
  

  

