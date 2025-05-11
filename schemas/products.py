from pydantic import BaseModel


class Product(BaseModel):
    sku: str
    name: str
    price_net: float
    price_gross: float
    description: str
    available: int

class ProductListResponse(BaseModel):
    products: list[Product]