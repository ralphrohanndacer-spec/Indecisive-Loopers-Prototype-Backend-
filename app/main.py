from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import menu_items, stalls
from app import models, database


async def lifespan(app_: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield

    await database.engine.dispose()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:5501",
    "http://localhost:5501",
    "http://localhost:5500",
    "http://127.0.0.1:57903",
    "https://indecisive-loopers.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stalls.router)
app.include_router(menu_items.router)


@app.get("/")
def home():
    return {"Hello": "World"}