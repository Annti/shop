from pydantic import BaseModel, confloat, constr


class Product(BaseModel):
    sku: constr(min_length = 1)
    name: constr(min_length = 1)
    price_net: confloat(ge=0)
    price_gross: confloat(ge=0)
    description: str
    available: constr(min_length = 1)

class ProductListInner(BaseModel):
    total: int
    products_list: list[Product]

class ProductListResponse(BaseModel):
    products: ProductListInner