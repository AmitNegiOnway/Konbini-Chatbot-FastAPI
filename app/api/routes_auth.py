from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import create_token, verify_password, get_current_user
from app.core.config import setting
from pydantic import BaseModel

# ------------------------------
# Fake user database (replace with real DB later)
# ------------------------------
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$ZDZYebZfRvo/3o7e.tTIwOKd0XG0GFNZyzgWhGGQ34HqPTWuPKPha",  # generate for "admin"
        "role": "manager"
    },
    "amit": {
        "username": "amit",
        "hashed_password": "$2b$12$j/Rb63RZajt9tYKtCoUEUOKdmgjUflyu2D8Gy4MMi3i19Ov5OJeju",  # run script above onway123(premium)
        "role": "premium"
    },
    "normal_cust": {
        "username": "normal_cust",
        "hashed_password": "$2b$12$cJEDhcTzSNH1Qc0BengBk.gb4mTDpfDOOiRO4m2m4l9Jzjr5P58Gi",# cust123
        "role": "normal"
    }
}

# To generate a bcrypt hash for a new user:
# from app.core.security import get_password_hash
# print(get_password_hash("your_plain_password"))

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token login."""
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_minutes=30
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Optional: simple login endpoint (if you still want JSON body)
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def simple_login(login_data: LoginRequest):
    user = fake_users_db.get(login_data.username)
    if not user or not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

# Protected test endpoint to get current user info
@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user




from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

