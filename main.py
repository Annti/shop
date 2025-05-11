import csv
import re
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

import jwt
import requests
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt

from config import settings
from schemas.products import ProductListResponse
from schemas.user import Token, User

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

def mock_instert_data_to_db(data: dict):
    response_p_list = {"products":[]}
    #przygotowanie do rozszerzenia o błedy
    status_code = "200"
    for d in data:
        d["status_code"]=status_code
        response_p_list["products"].append(d)
    return response_p_list

@app.post("/products/source_file")
def import_products_from_scource_file(source: str, response_model=ProductListResponse):

    file_path = Path(source)  # lub dowolna ścieżka
    extension = file_path.suffix      # → ".csv"

    if not extension.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be csv"
        )
    
    with open(source) as file:
        
        reader = csv.DictReader(file)
        data = mock_instert_data_to_db(reader)


    return data


# def extract_file_id(url: str) -> str:
#     match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
#     if not match:
#         raise ValueError("Niepoprawny link Google Drive")
#     return match.group(1)

# def convert_to_download_url(view_url: str) -> str:
#     file_id = extract_file_id(view_url)
#     return f"https://drive.google.com/uc?export=download&id={file_id}"

# @app.post("/products/source_file")
# def import_products_from_scource_file(source: str, response_model=Products):
#     download_url = convert_to_download_url(source)
#     print(download_url)
#     downloaded_file = requests.get(download_url)
#     downloaded_file.raise_for_status() # rzuc wyjatek jak nie udało się pobrac pliku

#     cd = downloaded_file.headers.get("Content-Disposition")
#     filename = "unknown.csv"
#     if cd and "filename=" in cd:
#         filename = cd.split("filename=")[-1].strip("\"'")
#         print("Nazwa pliku:", filename)

#     if not filename.lower().endswith(".csv"):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="File must be csv"
#         )
    
#     # with open(downloaded_file) as file:
#     #     reader = csv.DictReader(file)
#     #     print(reader)
#     #     # print("response", instert_data(data))

#     return {}



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
