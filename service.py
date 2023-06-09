from fastapi import FastAPI
from pydantic import BaseModel

from predictor import predicate

app = FastAPI()


class PredictionParameters(BaseModel):
    series: str = None
    model: str = None
    year: str = None
    kilometer: str = None
    mtv: str = None
    power: str = None
    transmission: str = None
    guarantee: str = None


class PredictionResponse(BaseModel):
    price: int


@app.post("/predicate", response_model=PredictionResponse)
def create_item(item: PredictionParameters) -> PredictionResponse:
    isAutomaticTransmission = "1" if item.transmission == "automatic" else "0"
    isManuelTransmission = "1" if isAutomaticTransmission == "0" else "0"

    print(item)
    price = predicate("0", item.series, item.model, item.year, item.kilometer, item.mtv, item.power,
                      isManuelTransmission,
                      isAutomaticTransmission, item.guarantee)

    return PredictionResponse(price=price)