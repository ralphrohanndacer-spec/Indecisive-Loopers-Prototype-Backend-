from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import StallCreate, StallUpdate, StallResponse
from ..crud import get_stalls, post_stalls, patch_stalls

router = APIRouter(
    prefix="/stalls",
    tags=["Stalls"],
)

@router.get("/id/{id}", response_model=StallResponse, status_code=status.HTTP_200_OK)
async def get_stall_id(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_stalls.get_stall_id(id, db)

@router.get("/name/{name}", response_model=list[StallResponse], status_code=status.HTTP_200_OK)
async def get_stall_name(name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_stalls.get_stall_name(name, db)

@router.get("/availability/{is_open}", response_model=list[StallResponse], status_code=status.HTTP_200_OK)
async def get_stall_availability(is_open: bool, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_stalls.get_stall_availability(is_open, db)

@router.post("/", response_model=StallResponse, status_code=status.HTTP_201_CREATED)
async def post_stall(request: StallCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await post_stalls.post_stall(request, db)

@router.patch('/{id}/remove', status_code=status.HTTP_200_OK)
async def remove_stall(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await patch_stalls.remove_stall(id, db)

@router.patch('/{id}/update', response_model=StallResponse, status_code=status.HTTP_200_OK)
async def update_stall(id: int, request: StallUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await patch_stalls.update_stall(id, request, db)
