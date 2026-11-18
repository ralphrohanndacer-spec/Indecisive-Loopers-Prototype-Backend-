from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .. import models


async def remove_stall(id, db):
    result = await db.execute(select(models.Stall).where(models.Stall.id == id))
    stall = result.scalars().first()

    if not stall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such stall with an id {id} found.")

    await db.delete(stall)
    await db.commit()

    return {"detail": f"Stall with id {id} successfully deleted."}


async def update_stall(id, request, db):
    result = await db.execute(select(models.Stall).where(models.Stall.id == id))
    stall = result.scalars().first()

    if not stall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No such stall with an id {id} found.")

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(stall, key, value)

    await db.commit()

    result = await db.execute(
        select(models.Stall)
        .options(selectinload(models.Stall.menu_items))
        .where(models.Stall.id == id)
    )
    return result.scalars().first()