from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .. import models


async def post_stall(request, db):
    new_stall = models.Stall(
        name=request.name,
        location=request.location,
        stall_type=request.stall_type,
        is_open=request.is_open,
        operating_hours=request.operating_hours,
        image_url=request.image_url
    )
    db.add(new_stall)
    await db.commit()

    result = await db.execute(
        select(models.Stall)
        .options(selectinload(models.Stall.menu_items))
        .where(models.Stall.id == new_stall.id)
    )
    return result.scalars().first()