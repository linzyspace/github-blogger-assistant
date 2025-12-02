from responses import get_predefined_response
from blog_lookup import search_blog_posts

def get_predefined_or_blog_response(text: str, lang: str = "en"):
    res = get_predefined_response(text, lang)
    if res:
        return {"type": "predefined", "response": res}

    posts = search_blog_posts(text)
    if posts:
        return {"type": "blog_match", "posts": posts}

    return None

