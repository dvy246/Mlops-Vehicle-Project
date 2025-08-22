# Mlops-Vehicle-Project
MLOps Project - Vehicle Insurance Data Pipeline
Welcome to this MLOps project, designed to demonstrate a robust pipeline for managing vehicle insurance data. This project aims to impress recruiters and visitors by showcasing the various tools, techniques, services, and features that go into building and deploying a machine learning pipeline for real-world data management. Follow along to learn about project setup, data processing, model deployment, and CI/CD automation!

📁 Project Setup and Structure
Step 1: Project Template
Start by executing the template.py file to create the initial project template, which includes the required folder structure and placeholder files.
Step 2: Package Management
Write the setup for importing local packages in setup.py and pyproject.toml files.
Tip: Learn more about these files from crashcourse.txt.
Step 3: Virtual Environment and Dependencies
Create a virtual environment and install required dependencies from requirements.txt:
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
Verify the local packages by running:
pip list
📊 MongoDB Setup and Data Management
Step 4: MongoDB Atlas Configuration
Sign up for MongoDB Atlas and create a new project.
Set up a free M0 cluster, configure the username and password, and allow access from any IP address (0.0.0.0/0).
Retrieve the MongoDB connection string for Python and save it (replace <password> with your password).
Step 5: Pushing Data to MongoDB
Create a folder named notebook, add the dataset, and create a notebook file mongoDB_demo.ipynb.
Use the notebook to push data to the MongoDB database.
Verify the data in MongoDB Atlas under Database > Browse Collections.
📝 Logging, Exception Handling, and EDA
Step 6: Set Up Logging and Exception Handling
Create logging and exception handling modules. Test them on a demo file demo.py.
Step 7: Exploratory Data Analysis (EDA) and Feature Engineering
Analyze and engineer features in the EDA and Feature Engg notebook for further processing in the pipeline.
📥 Data Ingestion
Step 8: Data Ingestion Pipeline
Define MongoDB connection functions in configuration.mongo_db_connections.py.
Develop data ingestion components in the data_access and components.data_ingestion.py files to fetch and transform data.
Update entity/config_entity.py and entity/artifact_entity.py with relevant ingestion configurations.
Run demo.py after setting up MongoDB connection as an environment variable.
Setting Environment Variables
Set MongoDB URL:
# For Bash
export MONGODB_URL="mongodb+srv://<username>:<password>...."
# For Powershell
$env:MONGODB_URL = "mongodb+srv://<username>:<password>...."
Note: On Windows, you can also set environment variables through the system settings.
🔍 Data Validation, Transformation & Model Training
Step 9: Data Validation
Define schema in config.schema.yaml and implement data validation functions in utils.main_utils.py.
Step 10: Data Transformation
Implement data transformation logic in components.data_transformation.py and create estimator.py in the entity folder.
Step 11: Model Training
Define and implement model training steps in components.model_trainer.py using code from estimator.py.

# Project Structure

```bash
app.py
├── config
│   ├── model.yaml
│   └── schema.yaml
├── demo.py
├── Dockerfile
├── LICENSE
├── Logs
│   └── 2025-08-06.log
├── notebook
│   ├── data.csv
│   └── mongoDB_demo.ipynb
├── projectflow.txt
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.py
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   └── __init__.cpython-310.pyc
│   ├── cloud_storage
│   │   ├── __init__.py
│   │   └── aws_storage.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── data_validation.py
│   │   ├── model_evaluation.py
│   │   ├── model_pusher.py
│   │   └── model_trainer.py
│   ├── configuration
│   │   ├── __init__.py
│   │   ├── aws_connection.py
│   │   └── mongo_db_connection.py
│   ├── constants
│   │   └── __init__.py
