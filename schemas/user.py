from pydantic import BaseModel

# === Pydantic schemas for response ===
class Token(BaseModel):
    accessToken: str
    tokenType: str

class User(BaseModel):
    userId: str
    email: str
    name: str
    surname: str