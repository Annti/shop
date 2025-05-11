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