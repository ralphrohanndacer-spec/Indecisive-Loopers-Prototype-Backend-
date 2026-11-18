from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload
from .. import models


async def get_stall_id(id, db):

    result = await db.execute(
        select(models.Stall).options(selectinload(models.Stall.menu_items)).where(models.Stall.id == id)
    )
    stall = result.scalars().first()

    if not stall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such stall with an id {id} found.')

    return stall


async def get_stall_name(name, db):
    clean_name = name.strip()

    result = await db.execute(
        select(models.Stall)
        .options(selectinload(models.Stall.menu_items))
        .where(models.Stall.name.ilike(f"%{clean_name}%"))
    )
    stalls = result.scalars().all()

    if stalls:
        return stalls

    fuzzy_result = await db.execute(
        select(models.Stall)
        .options(selectinload(models.Stall.menu_items))
        .where(text("name % :search_term"))
        .params(search_term=clean_name)
    )
    fuzzy_stalls = fuzzy_result.scalars().all()

    if not fuzzy_stalls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such stall with name matching '{name}' found.")

    return fuzzy_stalls


async def get_stall_availability(is_open, db):
    result = await db.execute(
        select(models.Stall)
        .options(selectinload(models.Stall.menu_items))
        .where(models.Stall.is_open == is_open)
    )
    stalls = result.scalars().all()

    if not stalls:
        status_text = "open" if is_open else "closed"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No stalls found that are currently {status_text}.")

    return stalls