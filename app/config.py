import os

# Blogger API configuration
BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")

if not BLOG_ID or not BLOGGER_API_KEY:
    print("[WARNING] BLOG_ID or BLOGGER_API_KEY not set. Blogger fallback will not work.")
