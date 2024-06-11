from fastapi import FastAPI
from src.database import drop_tables, create_tables

from src.artists.router import router as artists_router
from src.albums.router import router as album_router

app = FastAPI()
app.include_router(artists_router)
app.include_router(album_router)


@app.get("/")
async def root():
    try:
        await create_tables()
    except Exception as e:
        return {"error": "Failed connect to database"}
    return {"Server": "Working!"}


@app.post("/reset_db")
async def reset_database():
    await drop_tables()
    await create_tables()
    return {"msg": "Database reset!"}
