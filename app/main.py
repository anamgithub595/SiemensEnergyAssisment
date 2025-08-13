from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import sqlalchemy

from . import schemas, model, crud, database

# Create all database tables (this will check for existence first)
database.Base.metadata.create_all(bind=database.engine)

# Create an instance of the FastAPI application
app = FastAPI(title="ML API", version="0.1.0")

# --- Dependency for Database Session ---
def get_db():
    """
    Dependency to get a database session for each request.
    Ensures the session is closed after the request is finished.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Simple health check endpoint to confirm the server is running.
    """
    return {"status": "ok"}

@app.get("/db-check", tags=["Health Check"])
def db_check(db: Session = Depends(get_db)):
    """
    Checks the database connection by performing a simple query.
    """
    try:
        # Perform a simple, fast query to check the connection
        db.execute(sqlalchemy.text('SELECT 1'))
        return {"status": "ok", "message": "Database connection is healthy."}
    except Exception as e:
        # If the query fails, we raise an HTTP exception
        raise HTTPException(
            status_code=503,
            detail=f"Database connection error: {e}"
        )

@app.post("/predict", response_model=schemas.PredictionOut, tags=["Prediction"])
def predict(
    input_data: schemas.ModelInput,
    model_handler: model.ModelHandler = Depends(model.get_model_handler),
    db: Session = Depends(get_db)
):
    """
    Accepts input features, makes a prediction, logs the transaction,
    and returns the prediction.
    """
    prediction = model_handler.predict(input_data)

    # This is the crucial line that was missing from your endpoint
    crud.create_prediction_log(db=db, input_data=input_data, prediction=prediction)

    return schemas.PredictionOut(prediction=prediction)