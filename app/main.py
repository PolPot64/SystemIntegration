import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import shipments

app = FastAPI()

# Mount the static folder to serve HTML and assets
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../static")
app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

# Include API routes
app.include_router(shipments.router)