from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .. import models


async def post_menu_item(request, db):
    stall_result = await db.execute(
        select(models.Stall).where(models.Stall.id == request.stall_id)
    )
    stall = stall_result.scalars().first()

    if not stall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Stall with id {request.stall_id} not found. Create the stall first!")

    new_menu_item = models.MenuItem(
        name=request.name,
        food_category=request.food_category,
        is_halal=request.is_halal,
        is_available=request.is_available,
        is_best_seller=request.is_best_seller,
        price=request.price,
        image_url=request.image_url,
        stall_id=request.stall_id
    )
    db.add(new_menu_item)
    await db.commit()

    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(models.MenuItem.id == new_menu_item.id)
    )
    return result.scalars().first()