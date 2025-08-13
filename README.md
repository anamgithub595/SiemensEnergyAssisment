
# Machine Learning API Deployment Project

This project demonstrates the end-to-end process of developing a machine learning model, building a robust API with FastAPI, and deploying it to the cloud using AWS, Docker, and S3. It covers the full lifecycle from data cleaning and feature engineering to a live, containerized cloud deployment with persistent data logging.

## Project Architecture

The application is deployed on AWS following modern MLOps best practices for scalability and maintainability.

  * **AWS S3 (Simple Storage Service):** The trained `final_model.joblib` artifact is stored in a private S3 bucket. This decouples the model from the application code, allowing for independent updates.
  * **Docker Container:** The FastAPI application is containerized using Docker, ensuring a consistent and reproducible runtime environment. On startup, the container downloads the model artifact from S3.
  * **AWS EC2 (Elastic Compute Cloud):** A `t3.micro` virtual server hosts the running Docker container, making the API accessible to the public.
  * **Docker Volume:** A persistent Docker Volume is attached to the container on the EC2 host. This volume stores the `predictions.db` SQLite file, ensuring that all prediction logs are safely persisted even if the container restarts.

## Features

  * **Model:** A Random Forest Classifier trained for a binary classification task.
  * **API:** A robust API built with FastAPI, featuring asynchronous request handling and automatic data validation with Pydantic.
  * **Endpoints:**
      * `POST /predict`: Accepts feature data, serves a prediction, and logs the transaction.
      * `GET /health`: A simple health check to confirm the server is running.
      * `GET /db-check`: A health check to verify the database connection status.
  * **Database:** Every prediction request and its corresponding result are logged to a persistent SQLite database using the SQLAlchemy ORM.
  * **Deployment:** The entire application is containerized with Docker and deployed on an AWS EC2 instance.

-----

## Local Setup and Execution

To run this project on your local machine, follow these steps.

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/anamgithub595/SiemensEnergyAssisment.git
    cd SiemensEnergyAssisment
    ```

2.  **Create and Activate Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure AWS Credentials:**
    Create a `.env` file in the project root and add your AWS credentials.

    ```
    AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
    AWS_DEFAULT_REGION=your-aws-region
    ```

5.  **Run the Application:**
    The Uvicorn server will start the application. It will download the model from S3 on startup.

    ```bash
    uvicorn app.main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

-----

## Deployment to AWS

The application is designed to be deployed as a Docker container on an AWS EC2 instance.

1.  **Prerequisites:**

      * An AWS account with a configured IAM user and S3 bucket.
      * The `final_model.joblib` file uploaded to the S3 bucket.
      * Docker installed on your local machine.

2.  **Launch EC2 Instance:**

      * Launch a `t3.micro` EC2 instance using an Amazon Linux or Ubuntu AMI.
      * Create and assign a key pair for SSH access.
      * Configure the security group to allow inbound traffic on port `80` (HTTP) and `22` (SSH).

3.  **Install Docker on EC2:**

      * Connect to the EC2 instance via SSH.
      * Install Docker Engine using the appropriate commands for your chosen Linux distribution.
      * Add your user to the `docker` group (`sudo usermod -aG docker ${USER}`).

4.  **Deploy the Application:**

      * Clone your GitHub repository onto the EC2 instance.
      * Navigate to the project directory.
      * Create a `.env` file with your AWS credentials.
      * Build the Docker image: `docker build -t ml-api .`
      * Run the container with a persistent volume:
        ```bash
        docker volume create ml-api-db-data
        docker run -d -p 80:8000 --env-file .env -v ml-api-db-data:/app --name ml-api-container ml-api
        ```

5.  **Access the Live API:**
    The API will be publicly accessible at `http://52.87.209.187/docs`.

-----

## API Usage Example

Here is a sample request and response for the `/predict` endpoint.

### Sample Request

**Endpoint:** `POST /predict`

**Body:**

```json
{
  "feature_0": 0.9,
  "feature_1": -1.9,
  "feature_2": 0.0,
  "feature_3": 5.8,
  "feature_4": -2.1,
  "feature_5": 0.3,
  "feature_6": -4.9,
  "feature_7": 2.8,
  "feature_8": 0.3,
  "feature_9": -4.5,
  "feature_10": 0.1,
  "feature_11": -1.3,
  "feature_12": 2.0,
  "feature_13": 1.1,
  "feature_14": -1.3
}
```

### Sample Response

**Status Code:** `200 OK`

**Body:**

```json
{
  "prediction": 1
}
```
