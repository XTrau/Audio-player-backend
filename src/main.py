import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import drop_tables, create_tables


from auth.router import router as auth_router
from artists.router import router as artists_router
from albums.router import router as albums_router
from tracks.router import router as tracks_router
from files.router import router as file_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(artists_router)
app.include_router(albums_router)
app.include_router(tracks_router)
app.include_router(file_router, prefix="/files")

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
    "X-CSRF-Token",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=allow_headers,
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
