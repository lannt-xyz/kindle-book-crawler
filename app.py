from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from controller import craw_api, pages

# Create a FastAPI instance
app = FastAPI()

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(craw_api.router, prefix="/api/craw")
app.include_router(pages.router, prefix="")
