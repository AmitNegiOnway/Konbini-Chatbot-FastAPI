from fastapi import APIRouter,HTTPException,Depends
from app.api.schema import InputSchema,OutputSchema
import pandas as pd 
from training.train_utils import FOOD_NUTRITION_DATA_FILE_PATH
from app.core.dependencies import require_customer
import os
router=APIRouter()

@router.post('/premium_product', response_model=OutputSchema)
def premium(user_input: InputSchema,user:dict=Depends(require_customer)):
    df = pd.read_csv(FOOD_NUTRITION_DATA_FILE_PATH)
    df['name']=df['name'].str.strip()
    match = df[df['name'].str.lower() == user_input.product_name.lower()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Product '{user_input.product_name}' not found")
    row = match.iloc[0]
    result=OutputSchema(
        price=int(row['price']),
        calories_kcal=int(row['calories_kcal']),
        protein_g=float(row['protein_g']),
        fat_g=float(row['fat_g']),
        carbohydrates_g=float(row['carbohydrates_g']),
        salt_equivalent_g=float(row['salt_equivalent_g']),
        saturated_fat_g=float(row['saturated_fat_g']),
        sugar_g=float(row['sugar_g']),
        dietary_fiber_g=float(row['dietary_fiber_g']),
        cholesterol_mg=float(row['cholesterol_mg']),
        sodium_mg=float(row['sodium_mg']),
        vitamin_c_mg=float(row['vitamin_c_mg']),
        calcium_mg=float(row['calcium_mg']),
        iron_mg=float(row['iron_mg']),
        category=str(row['Category']),
        meal_type=str(row['Meal_Type'])
    )
    
    os.makedirs("audits", exist_ok=True)
    with open("audits/prediction.txt", "a") as file:
        file.write(
            f"{user_input.product_name} -> "
            f"price={int(row['price'])}, calories={int(row['calories_kcal'])}\n"
        )
    return result
