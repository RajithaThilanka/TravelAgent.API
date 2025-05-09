from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .database import engine, get_db
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API configuration
API_PREFIX = os.getenv("API_PREFIX", "/api")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

app = FastAPI(
    title="Travel Agent API",
    description="A FastAPI-based travel agent chatbot using GPT-3.5 Turbo",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with the configured API prefix
app.include_router(router, prefix=API_PREFIX)

@app.on_event("startup")
async def startup_event():
    """Check database connection on startup"""
    try:
        # Try to create a connection
        with engine.connect() as connection:
            logger.info("✅ Database connection successful!")
            logger.info(f"Connected to database: {os.getenv('DATABASE_URL', '').split('/')[-1]}")
            logger.info(f"Using model: {MODEL_NAME} with temperature: {TEMPERATURE}")
    except Exception as e:
        logger.error("❌ Database connection failed!")
        logger.error(f"Error: {str(e)}")
        raise e

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "model": MODEL_NAME,
            "temperature": TEMPERATURE,
            "api_prefix": API_PREFIX,
            "message": "All systems operational"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        } 