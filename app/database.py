from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# 1. Define the database URL
# For local development, we'll use SQLite, which is a simple file-based database.
# The database file 'predictions.db' will be created in the root of your project.
SQLALCHEMY_DATABASE_URL = "sqlite:///./predictions.db"

# 2. Create the SQLAlchemy engine
# The engine is the entry point to our database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class
# Each instance of SessionLocal will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class
# We will inherit from this class to create each of the ORM models (our database tables).
Base = declarative_base()

class PredictionLog(Base):
    """
    SQLAlchemy ORM model for the prediction_logs table.
    """
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Input Features
    feature_0 = Column(Float, index=True)
    feature_1 = Column(Float, index=True)
    feature_2 = Column(Float)
    feature_3 = Column(Float, index=True)
    feature_4 = Column(Float)
    feature_5 = Column(Float)
    feature_6 = Column(Float)
    feature_7 = Column(Float, index=True)
    feature_8 = Column(Float)
    feature_9 = Column(Float, index=True)
    feature_10 = Column(Float)
    feature_11 = Column(Float)
    feature_12 = Column(Float, index=True)
    feature_13 = Column(Float)
    feature_14 = Column(Float)
    
    # Prediction Result
    prediction = Column(Integer, index=True)