from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ProductBrandData(BaseModel):
    name: str


class ProductData(BaseModel):
    brand: Optional[ProductBrandData] = None
    size: Optional[str] = None
