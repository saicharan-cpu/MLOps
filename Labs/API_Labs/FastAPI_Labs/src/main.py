from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from predict import predict_data, load_model
import numpy as np

app = FastAPI()

# Load model globally at startup
try:
    model = load_model()
except FileNotFoundError as e:
    print("ERROR: ", e)
    model = None

# Pydantic models
class WineData(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float

class WineResponse(BaseModel):
    predicted_class: int

class WineQualityResponse(BaseModel):
    predicted_class: int
    advice: str

# Health endpoint
@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

# Predict raw class
@app.post("/predict", response_model=WineResponse)
async def predict_wine(wine_features: WineData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    features = [[
        wine_features.alcohol,
        wine_features.malic_acid,
        wine_features.ash,
        wine_features.alcalinity_of_ash
    ]]
    y_pred = model.predict(np.array(features))
    return WineResponse(predicted_class=int(y_pred[0]))

# Predict class + advice
@app.post("/predict_quality", response_model=WineQualityResponse)
async def predict_wine_quality(wine_features: WineData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        features = [[
            wine_features.alcohol,
            wine_features.malic_acid,
            wine_features.ash,
            wine_features.alcalinity_of_ash
        ]]
        y_pred = model.predict(np.array(features))
        predicted_class = int(y_pred[0])

        advice_map = {
            0: "Low quality wine, not recommended",
            1: "Medium quality wine, acceptable",
            2: "High quality wine, recommended"
        }

        return WineQualityResponse(
            predicted_class=predicted_class,
            advice=advice_map.get(predicted_class, "Unknown")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
