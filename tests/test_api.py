import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base, PredictionLog

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ====================================================================
# Pytest Fixtures
# ====================================================================

@pytest.fixture()
def session():
    # Drop and recreate tables for a clean state
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # Dependency override
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

# ====================================================================
# Tests
# ====================================================================

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_db_check(client):
    response = client.get("/db-check")
    assert response.status_code == 200
    assert response.json()["message"] == "Database connection is healthy."

def test_predict_positive_case_1(client):
    payload = { "feature_0": 0.9, "feature_1": -1.9, "feature_2": 0.0, "feature_3": 5.8, "feature_4": -2.1, "feature_5": 0.3, "feature_6": -4.9, "feature_7": 2.8, "feature_8": 0.3, "feature_9": -4.5, "feature_10": 0.1, "feature_11": -1.3, "feature_12": 2.0, "feature_13": 1.1, "feature_14": -1.3 }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json() == {"prediction": 1}

def test_predict_positive_case_0(client):
    payload = { "feature_0": -0.1, "feature_1": 1.2, "feature_2": -0.5, "feature_3": 0.8, "feature_4": -2.1, "feature_5": 0.3, "feature_6": 1.1, "feature_7": -0.0, "feature_8": 0.9, "feature_9": 4.4, "feature_10": -2.2, "feature_11": -2.1, "feature_12": -2.4, "feature_13": 2.4, "feature_14": 1.1 }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json() == {"prediction": 0}

def test_predict_negative_missing_feature(client):
    payload = { "feature_0": 0.9, "feature_1": -1.9, "feature_2": 0.0, "feature_4": -2.1, "feature_5": 0.3, "feature_6": -4.9, "feature_7": 2.8, "feature_8": 0.3, "feature_9": -4.5, "feature_10": 0.1, "feature_11": -1.3, "feature_12": 2.0, "feature_13": 1.1, "feature_14": -1.3 }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_negative_wrong_data_type(client):
    payload = { "feature_0": 0.9, "feature_1": -1.9, "feature_2": 0.0, "feature_3": "not_a_float", "feature_4": -2.1, "feature_5": 0.3, "feature_6": -4.9, "feature_7": 2.8, "feature_8": 0.3, "feature_9": -4.5, "feature_10": 0.1, "feature_11": -1.3, "feature_12": 2.0, "feature_13": 1.1, "feature_14": 1.4 }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_prediction_logging(client, session):
    """
    This test now uses the 'session' fixture directly.
    """
    # 1. Check initial state
    initial_log_count = session.query(PredictionLog).count()
    assert initial_log_count == 0
    
    # 2. Make the API call
    payload = { "feature_0": 0.1, "feature_1": 0.2, "feature_2": 0.3, "feature_3": 0.4, "feature_4": 0.5, "feature_5": 0.6, "feature_6": 0.7, "feature_7": 0.8, "feature_8": 0.9, "feature_9": 1.0, "feature_10": 1.1, "feature_11": 1.2, "feature_12": 1.3, "feature_13": 1.4, "feature_14": 1.5 }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    # 3. Check final state within the SAME session
    final_log_count = session.query(PredictionLog).count()
    assert final_log_count == 1