from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import drop_tables, create_tables

from src.artists.router import router as artists_router
from src.albums.router import router as albums_router
from src.tracks.router import router as tracks_router
from src.files.router import router as file_router

app = FastAPI()
app.include_router(artists_router, prefix='/api')
app.include_router(albums_router, prefix='/api')
app.include_router(tracks_router, prefix='/api')
app.include_router(file_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

allow_headers = [
    "Content-Type",
    "Authorization",
    "X-Requested-With",
    "Accept",
    "Origin",
    "User-Agent",
    "DNT",
    "Cache-Control",
    "X-Mx-ReqToken",
    "Keep-Alive",
    "X-Requested-With",
    "If-Modified-Since",
    "X-CSRF-Token"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=allow_headers
)


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
