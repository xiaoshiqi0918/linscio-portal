from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str | None = None
    locked_until: str | None = None


class ProductOut(BaseModel):
    product_id: str
    name: str
    description: str | None = None
    sort_order: int = 0


class ProductListResponse(BaseModel):
    products: list[ProductOut]
