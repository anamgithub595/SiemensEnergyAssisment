from pydantic import BaseModel, Field, ConfigDict

class ModelInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "feature_0": -0.1, "feature_1": 1.2, "feature_2": -0.5,
                "feature_3": 0.8, "feature_4": -2.1, "feature_5": 0.3,
                "feature_6": 1.1, "feature_7": -0.0, "feature_8": 0.9,
                "feature_9": 4.4, "feature_10": -2.2, "feature_11": -2.1,
                "feature_12": -2.4, "feature_13": 2.4, "feature_14": 1.1
            }
        }
    )
    feature_0: float
    feature_1: float
    feature_2: float
    feature_3: float
    feature_4: float
    feature_5: float
    feature_6: float
    feature_7: float
    feature_8: float
    feature_9: float
    feature_10: float
    feature_11: float
    feature_12: float
    feature_13: float
    feature_14: float

class PredictionOut(BaseModel):
    prediction: int = Field(..., json_schema_extra={"example": 1}, description="The binary prediction from the model (0 or 1).")