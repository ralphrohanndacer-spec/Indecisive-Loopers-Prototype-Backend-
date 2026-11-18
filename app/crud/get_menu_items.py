from fastapi import HTTPException, status
from sqlalchemy import select, text, func
from sqlalchemy.orm import selectinload
from .. import models

async def get_menu_item_id(id, db):

    result = await db.execute(
        select(models.MenuItem).options(selectinload(models.MenuItem.stall)).where(models.MenuItem.id == id)
    )
    menu_item = result.scalars().first()

    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such menu item with an id {id} found.')

    return menu_item


async def get_menu_items_all(db):
    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
    )
    menu_items = result.scalars().all()

    return menu_items


async def get_menu_items_default(db):
    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .order_by(func.random())
        .limit(9)
    )
    menu_items = result.scalars().all()

    return menu_items

async def get_menu_item_name(name, db):
    clean_name = name.strip()

    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(models.MenuItem.name.ilike(f"%{clean_name}%"))
    )
    menu_items = result.scalars().all()

    if menu_items:
        return menu_items

    fuzzy_result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(text("name % :search_term"))
        .params(search_term=clean_name)
    )
    fuzzy_menu_items = fuzzy_result.scalars().all()

    if not fuzzy_menu_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such menu item with name matching '{name}' found.")

    return fuzzy_menu_items


async def get_menu_item_location(location, db):
    clean_location = location.strip()

    result = await db.execute(
        select(models.MenuItem)
        .join(models.MenuItem.stall)
        .options(selectinload(models.MenuItem.stall))
        .where(models.Stall.location.ilike(f"%{clean_location}%"))
    )
    menu_items = result.scalars().all()

    if menu_items:
        return menu_items

    fuzzy_result = await db.execute(
        select(models.MenuItem)
        .join(models.MenuItem.stall)
        .options(selectinload(models.MenuItem.stall))
        .where(text("stalls.location % :search_term"))
        .params(search_term=clean_location)
    )
    fuzzy_menu_items = fuzzy_result.scalars().all()

    if not fuzzy_menu_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No menu items found for location '{location}'.")

    return fuzzy_menu_items


async def get_menu_item_category(category, db):
    clean_category = category.strip()

    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(models.MenuItem.food_category.ilike(f"%{clean_category}%"))
    )
    menu_items = result.scalars().all()

    if menu_items:
        return menu_items

    fuzzy_result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(text("food_category % :search_term"))
        .params(search_term=clean_category)
    )
    fuzzy_menu_items = fuzzy_result.scalars().all()

    if not fuzzy_menu_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No menu items found in category '{category}'.")

    return fuzzy_menu_items


async def get_menu_item_budget(budget, db):
    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(models.MenuItem.price <= budget)
        .order_by(models.MenuItem.price.asc())
    )
    menu_items = result.scalars().all()

    if not menu_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No menu items found under ₱{budget}.")

    return menu_items


async def get_menu_item_best_seller(db):
    result = await db.execute(
        select(models.MenuItem)
        .options(selectinload(models.MenuItem.stall))
        .where(models.MenuItem.is_best_seller == True)
    )
    menu_items = result.scalars().all()

    if not menu_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No best-seller menu items found.")

    return menu_items