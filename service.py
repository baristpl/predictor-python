from fastapi import FastAPI
from pydantic import BaseModel

from predictor import predicate

app = FastAPI()


class PredictionParameters(BaseModel):
    brand: str = None
    series: str = None
    model: str = None
    year: str = None
    kilometer: str = None
    mtv: str = None
    power: str = None
    transmission: str = None
    guarantee: str = None


@app.post("/predicate")
def create_item(item: PredictionParameters) -> int:
    isAutomaticTransmission = "1" if item.transmission == "automatic" else "0"
    isManuelTransmission = "1" if isAutomaticTransmission == "0" else "0"
    hasGuarantee = "1" if item.guarantee == True else "0"

    return predicate("0", item.series, item.model, item.year, item.kilometer, item.mtv, item.power,
                     isManuelTransmission,
                     isAutomaticTransmission, hasGuarantee)
