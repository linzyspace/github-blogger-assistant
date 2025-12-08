import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    PORT = int(os.getenv("PORT", 5000))
    BLOG_ID = os.getenv("BLOG_ID")
    API_KEY = os.getenv("API_KEY")

config = Config()

