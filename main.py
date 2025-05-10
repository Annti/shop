from config import settings
from passlib.hash import bcrypt  
from schemas.user import Token, User
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from copy import deepcopy
import jwt  

# === Mock user db response ===
fake_user_db = {
        "userId": "tonyabc22123123",
        "email": "tony@gmail.com",
        "hashedPassword": bcrypt.hash("password123"),
        "name": "Tony",
        "surname": "Mazurek"
}

# === Inicjalizacja FastAPI ===
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def authenticate_user(email: str, password: str):
    user = fake_user_db
    if not user or not bcrypt.verify(password, user["hashedPassword"]):
        return None
    return user

def create_access_token(data: dict, expires: int):
    to_encode = deepcopy(data)
    expire = datetime.utcnow() + timedelta(minutes=expires)
    to_encode.update({"exp": expire, "sub": data["userId"]}) 
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token_data = {"userId": user["userId"], "email": user["email"]}
    access_token = create_access_token(token_data, settings.JWT_EXPIRE_MINUTES)
    return Token(accessToken=access_token, tokenType="bearer")

# === Endpoint chroniony tokenem ===
# @app.get("/user", response_model=User)
# def read_users_me(token: str = Depends(oauth2_scheme)):
#     payload = decode_token(token)
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     user_id = payload.get("sub")
#     for user in fake_users_db.values():
#         if user["user_id"] == user_id:
#             return User(**user)
#     raise HTTPException(status_code=404, detail="User not found")
