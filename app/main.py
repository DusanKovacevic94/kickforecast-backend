from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import auth, users, posts, media
from .database import engine, Base

# Create tables (for simple setup, usually handled by alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KickForecast CMS",
    description="Headless CMS for KickForecast football predictions",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost:3000", # Next.js frontend
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(media.router)

# Serve uploaded media
MEDIA_ROOT = Path(__file__).resolve().parent / "media"
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

@app.get("/")
def read_root():
    return {"message": "Welcome to KickForecast API"}
