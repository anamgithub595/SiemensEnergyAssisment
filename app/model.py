import joblib
import pandas as pd
from pathlib import Path
import boto3
from io import BytesIO
import os

from . import schemas

# --- Configuration ---
BUCKET_NAME = "anam-siemens-assesment"  # <-- IMPORTANT: REPLACE WITH YOUR BUCKET NAME
MODEL_KEY = "final_model.joblib"

class ModelHandler:
    def __init__(self, bucket_name: str, model_key: str):
        self.model = self.load_model_from_s3(bucket_name, model_key)

    def load_model_from_s3(self, bucket_name: str, model_key: str):
        """Loads a model from an S3 bucket."""
        try:
            print(f"Loading model from S3 bucket: {bucket_name}, Key: {model_key}")
            s3_client = boto3.client("s3")
            # Use BytesIO to handle the downloaded object in memory
            with BytesIO() as f:
                s3_client.download_fileobj(Bucket=bucket_name, Key=model_key, Fileobj=f)
                f.seek(0) # Go to the beginning of the in-memory file
                loaded_model = joblib.load(f)
            print("Model loaded successfully from S3.")
            return loaded_model
        except Exception as e:
            print(f"Error loading model from S3: {e}")
            # Depending on the use case, you might want to raise the exception
            # or handle it gracefully (e.g., return None or a default model)
            raise

    def predict(self, input_data: schemas.ModelInput) -> int:
        """Makes a prediction using the loaded model."""
        data_dict = input_data.model_dump()
        data_dict["positive_predictors_sum"] = (
            data_dict["feature_3"] + data_dict["feature_7"] + data_dict["feature_12"]
        )
        data_dict["main_interaction"] = data_dict["feature_3"] * data_dict["feature_9"]
        df = pd.DataFrame([data_dict])
        prediction = self.model.predict(df)[0]
        return int(prediction)

# --- Singleton Pattern ---
model_handler = ModelHandler(bucket_name=BUCKET_NAME, model_key=MODEL_KEY)

def get_model_handler() -> ModelHandler:
    """Returns the singleton model handler instance."""
    return model_handler