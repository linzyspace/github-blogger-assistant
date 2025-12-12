import os
from functools import lru_cache

class Settings:
    """Load Blogger configuration from environment variables."""
    BLOGGER_API_KEY: str
    BLOG_ID: str

    def __init__(self):
        self.BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")
        self.BLOG_ID = os.getenv("BLOGGER_BLOG_ID")

        if not self.BLOGGER_API_KEY:
            raise RuntimeError("BLOGGER_API_KEY environment variable not set")
        if not self.BLOG_ID:
            raise RuntimeError("BLOGGER_BLOG_ID environment variable not set")


@lru_cache()
def get_settings():
    """Cached settings for fast access."""
    return Settings()
