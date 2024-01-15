from pydantic import BaseModel


class ProductBrandData(BaseModel):
    name: str


class ProductData(BaseModel):
    brand: ProductBrandData | None = None
    size: str | None = None
