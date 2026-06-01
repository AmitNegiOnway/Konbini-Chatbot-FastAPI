from pydantic import BaseModel, Field
from typing import Annotated, List

class InputSchema(BaseModel):
    product_name: str = Field(..., description="Name of the konbini product")

class OutputSchema(BaseModel):
    price: int
    calories_kcal: int
    protein_g: float
    fat_g: float
    carbohydrates_g: float
    salt_equivalent_g: float
    saturated_fat_g: float
    sugar_g: float
    dietary_fiber_g: float
    cholesterol_mg: float
    sodium_mg: float
    vitamin_c_mg: float
    calcium_mg: float
    iron_mg: float

class DiseasesInput(BaseModel):
    symptoms: List[str] = Field(..., description="List of symptoms")

class DiseasesOutput(BaseModel):
    predict_diseases: str
    predict_nutrition: str
    predict_food: str