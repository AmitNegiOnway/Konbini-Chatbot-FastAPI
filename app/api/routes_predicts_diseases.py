from fastapi import APIRouter ,Depends
from app.api.schema import DiseasesInput,DiseasesOutput
from app.core.dependencies import require_customer
from app.services.model_service import PremiumCustomer


router=APIRouter()

@router.post('/predict_diseases', response_model=DiseasesOutput)
def predict(user_input: DiseasesInput,user:dict=Depends(require_customer)):
    premium = PremiumCustomer(user_input)
    rec = premium.get_recommendations()
    return DiseasesOutput(

        predict_diseases=rec["disease"],
        predict_nutrition=rec["nutrition_advice"],
        predict_food=rec["food_advice"]
        
        )


