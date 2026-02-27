# Wine Quality ML Training with Docker

## Overview

This project demonstrates how to train a Machine Learning model inside a Docker container. It uses a Random Forest Classifier from Scikit-Learn to train a model and save it as a `.pkl` file. The purpose of this lab is to show how Docker can be used to create a reproducible ML training environment.

The container installs dependencies, runs the training script, and saves the trained model.

---

## Project Structure

```
Lab1/
│
├── dockerfile              # Defines the Docker image
├── ReadMe.md               # Project documentation
│
└── src/
    ├── main.py             # Entry point script
    ├── train.py            # Model training logic
    ├── requirements.txt    # Python dependencies
    └── models/
        └── wine_model.pkl  # Saved trained model
```

---

## What the Project Does

The project performs the following steps:

1. Loads a dataset (Wine dataset from Scikit-Learn)
2. Splits the dataset into training and testing sets
3. Trains a Random Forest Classifier
4. Saves the trained model using joblib
5. Runs all of the above inside a Docker container

This ensures the training process is consistent across different systems.

---

## Technologies Used

* Python 3.10
* Scikit-Learn
* Joblib
* Docker

---

## Dockerfile Explanation

The Dockerfile performs the following actions:

```
FROM python:3.10
```

Uses official Python image.

```
WORKDIR /app
```

Sets working directory inside container.

```
COPY src/requirements.txt .
RUN pip install -r requirements.txt
```

Copies and installs dependencies.

```
COPY src/ ./src/
```

Copies source code.

```
CMD ["python", "src/main.py"]
```

Runs the training script when container starts.

---

## How to Build the Docker Image

Run this command from the project root directory:

```
docker build -t wine-ml-training .
```

This creates a Docker image named:

```
wine-ml-training
```

---

## How to Run the Container

Run:

```
docker run wine-ml-training
```

Expected output:

```
The model training was successful
```

---

## Output

After execution, the trained model is saved as:

```
src/models/wine_model.pkl
```

This file contains the trained Machine Learning model and can be used later for predictions.

---

## Why Use Docker for ML?

Docker provides:

* Reproducible environment
* Dependency isolation
* Easy deployment
* No local setup required
* Same behavior across all machines

This is especially useful in ML pipelines and production environments.
