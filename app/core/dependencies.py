from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user

def require_customer(current_user: dict = Depends(get_current_user)):
    """Allow normal, premium, and manager roles."""
    if current_user["role"] not in ["normal", "premium", "manager"]:
        raise HTTPException(status_code=403, detail="Customer access required")
    return current_user

def require_premium(current_user: dict = Depends(get_current_user)):
    """Allow only premium customers or managers."""
    if current_user["role"] not in ["premium", "manager"]:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    return current_user

def require_manager(current_user: dict = Depends(get_current_user)):
    """Allow only managers."""
    if current_user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")
    return current_user
