from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from app.models import StallType
from typing import Optional


class StallSimpleResponse(BaseModel):
    id: int
    name: str
    location: str
    stall_type: StallType
    is_open: bool
    operating_hours: Optional[str] = None
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MenuItemBase(BaseModel):
    name: str
    food_category: str
    is_halal: bool
    is_available: bool
    is_best_seller: bool
    price: float
    image_url: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    stall_id: int


class MenuItemResponse(MenuItemCreate):
    id: int
    stall: StallSimpleResponse

    model_config = ConfigDict(from_attributes=True)


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    food_category: Optional[str] = None
    is_halal: Optional[bool] = None
    is_available: Optional[bool] = None
    is_best_seller: Optional[bool] = None
    price: Optional[float] = None
    image_url: Optional[str] = None


class StallBase(BaseModel):
    name: str
    location: str
    is_open: bool
    stall_type: StallType
    operating_hours: Optional[str] = None
    image_url: Optional[str] = None


class StallCreate(StallBase):
    pass


class StallUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    is_open: Optional[bool] = None
    stall_type: Optional[StallType] = None
    operating_hours: Optional[str] = None
    image_url: Optional[str] = None


class StallResponse(StallBase):
    id: int
    menu_items: list[MenuItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


MenuItemResponse.model_rebuild()
StallResponse.model_rebuild()