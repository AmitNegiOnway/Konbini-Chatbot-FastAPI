from fastapi import APIRouter,Depends
from app.core.dependencies import require_manager

router=APIRouter()

@router.get("/manager/sales-pie")
def sales_pie(user:dict=Depends(require_manager)):
    # Replace with real data from your database or CSV
    return {"labels": ["Onigiri", "Bento", "Fried Chicken", "Coffee"], "values": [35000, 48000, 22000, 18000]}

