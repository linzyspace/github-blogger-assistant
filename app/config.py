import os
from functools import lru_cache

class Settings:
    BLOGGER_API_KEY: str
    BLOG_ID: str

    def __init__(self):
        self.BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")
        self.BLOG_ID = os.getenv("BLOG_ID")

        if not self.BLOGGER_API_KEY:
            raise RuntimeError("BLOGGER_API_KEY environment variable not set")

        if not self.BLOG_ID:
            raise RuntimeError("BLOG_ID environment variable not set")


@lru_cache()
def get_settings():
    return Settings()
