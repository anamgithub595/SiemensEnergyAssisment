from sqlalchemy.orm import Session
from . import database, schemas

def create_prediction_log(db: Session, input_data: schemas.ModelInput, prediction: int):
    """
    Creates and saves a new prediction log entry in the database.
    """
    # Create a new SQLAlchemy model instance from the input data
    db_log_entry = database.PredictionLog(
        **input_data.model_dump(),
        prediction=prediction
    )
    
    # Add the instance to the session
    db.add(db_log_entry)
    
    # Commit the changes to the database
    db.commit()
    
    # Refresh the instance to get the new data from the DB (like the auto-generated id)
    db.refresh(db_log_entry)
    
    return db_log_entry