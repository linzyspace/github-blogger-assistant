from .responses import get_predefined_response
from .blog_lookup import search_blogger_posts


async def process_user_message(message: str, lang: str = "en"):
    """
    Primary assistant logic.
    """

    # 1️⃣ Predefined responses
    predefined = get_predefined_response(message)
    if predefined:
        return {
            "type": "predefined",
            "response": predefined
        }

    # 2️⃣ Blogger Lookup
    blogger_post = await search_blogger_posts(message)
    if blogger_post:
        return {
            "type": "blogger",
            "title": blogger_post["title"],
            "content": blogger_post["content"],
            "url": blogger_post["url"]
        }

    # 3️⃣ Default
    return {
        "type": "none",
        "response": "No predefined answer or blog match found."
    }
