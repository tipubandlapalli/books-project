from pydantic import BaseModel, field_validator


class Book(BaseModel):
    id: int
    title: str
    description: str
    price: int = 0

    @field_validator("price")
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("price can't be negative")
        return price
    