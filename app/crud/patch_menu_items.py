from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .. import models


async def remove_menu_item(id, stall_id, db):
    result = await db.execute(
        select(models.MenuItem).where(models.MenuItem.id == id, models.MenuItem.stall_id == stall_id)
    )
    menu_item = result.scalars().first()

    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No menu item found with id {id} for stall {stall_id}.",)

    await db.delete(menu_item)
    await db.commit()

    return {"detail": f"Menu item with id {id} successfully deleted."}


async def update_menu_item(id, stall_id, request, db):
    result = await db.execute(
        select(models.MenuItem)
        .where(models.MenuItem.id == id, models.MenuItem.stall_id == stall_id)
    )
    menu_item = result.scalars().first()

    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such menu id with an id {id} found.")

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(menu_item, key, value)

    await db.commit()

    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(models.MenuItem.id == id, models.MenuItem.stall_id == stall_id)
    )
    return result.scalars().first()