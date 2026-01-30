from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data


app = FastAPI()

class WineData(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float

class WineResponse(BaseModel):
    predicted_class: int


@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

@app.post("/predict", response_model=WineResponse)
async def predict_wine(wine_features: WineData):
    features = [[
        wine_features.alcohol,
        wine_features.malic_acid,
        wine_features.ash,
        wine_features.alcalinity_of_ash
    ]]
    prediction = predict_data(features)
    return WineResponse(predicted_class=int(prediction[0]))

    


    
