from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from ..crud import get_menu_items, post_menu_items, patch_menu_items

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"],
)

@router.get("/id/{id}", response_model=MenuItemResponse, status_code=status.HTTP_200_OK)
async def get_menu_item_id(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_item_id(id, db)

@router.get("/", response_model=list[MenuItemResponse], status_code=status.HTTP_200_OK)
async def get_menu_items_all(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_items_all(db)

@router.get("/default", response_model=list[MenuItemResponse], status_code=status.HTTP_200_OK)
async def get_menu_items_default(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_items_default(db)

@router.get("/name/{name}", response_model=list[MenuItemResponse], status_code=status.HTTP_200_OK)
async def get_menu_item_name(name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_item_name(name, db)

@router.get("/location/{location}", response_model=list[MenuItemResponse], status_code=status.HTTP_200_OK)
async def get_menu_item_location(location: str, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_item_location(location, db)

@router.get("/category/{category}", response_model=list[MenuItemResponse], status_code=status.HTTP_200_OK)
async def get_menu_item_category(category: str, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_item_category(category, db)

@router.get("/budget/{budget}", response_model=list[MenuItemResponse], status_code=status.HTTP_200_OK)
async def get_menu_item_budget(budget: float, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_item_budget(budget, db)

@router.get("/best-seller", response_model=list[MenuItemResponse], status_code=status.HTTP_200_OK)
async def get_menu_item_best_seller(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_menu_items.get_menu_item_best_seller(db)

@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def post_menu_item(request: MenuItemCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await post_menu_items.post_menu_item(request, db)

@router.patch('/{id}/{stall_id}/remove', status_code=status.HTTP_200_OK)
async def remove_menu_item(id: int, stall_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await patch_menu_items.remove_menu_item(id, stall_id, db)

@router.patch('/{id}/{stall_id}/update', response_model=MenuItemResponse, status_code=status.HTTP_200_OK)
async def update_menu_item(id: int, stall_id: int, request: MenuItemUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await patch_menu_items.update_menu_item(id, stall_id, request, db)