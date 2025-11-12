from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base
from app.routes import countries

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="The Baking Atlas API",
    description="API for exploring global baking traditions",
    version="0.1.0"
)

# Configure CORS (allows your frontend to talk to the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Alternative
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(countries.router)

@app.get("/")
def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to The Baking Atlas API",
        "docs": "/docs",
        "version": "0.1.0"
    }