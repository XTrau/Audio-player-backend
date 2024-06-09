from fastapi import FastAPI
from src.database import drop_tables, create_tables

app = FastAPI()


@app.get("/")
async def root():
    await create_tables()
    return {"Server": "Working!"}


@app.post("/reset_db")
async def reset_database():
    await drop_tables()
    await create_tables()
    return {"msg": "Database reset!"}
