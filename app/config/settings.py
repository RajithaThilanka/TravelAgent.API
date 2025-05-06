import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Settings
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "Travel Agent API"

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# CORS Settings
CORS_ORIGINS = ["*"]  # In production, replace with your frontend URL
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Session Settings
SESSION_EXPIRY = 3600  # 1 hour in seconds 