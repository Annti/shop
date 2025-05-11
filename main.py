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
from pydantic import ValidationError

from config import settings
from schemas.products import Product, ProductListResponse
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
    response_p_list = {"products":{"total":0, "products_list":[]}}
    i = 0
    #przygotowanie do rozszerzenia o błedy
    status_code = status.HTTP_200_OK
    for d in data:
        i +=1
        try:
             product = Product(**d)  # row to np. dict z CSV
        except ValidationError as e:
            print("Niepoprawny produkt:", e)
            status_code = status.HTTP_400_BAD_REQUEST
            for error in e.errors():
                error = f"{error['msg']} {'.'.join(map(str, error['loc']))}"
        else:
            print("Produkt poprawny:", product)
            status_code = status.HTTP_200_OK
            error = ""

        d["status_code"]=status_code
        d["error"]=error
        response_p_list["products"]["products_list"].append(d)

    response_p_list["products"]["total"]=i

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
    
    with open(source) as file, open("response.csv", "w") as res:
        reader = csv.DictReader(file)
        data = mock_instert_data_to_db(reader)

        writer = csv.DictWriter(res, fieldnames=["sku", "name", "price_net", "price_gross", "description", "available", "status_code", "error"])
        writer.writeheader()
        writer.writerows(data["products"]["products_list"])

    return data