from app.blog_lookup import lookup_blog
from app.categories import get_category
from app.responses import get_response  # if you have a responses.py

def get_predefined_or_blog_response(topic: str, lang: str):
    # Check predefined categories first
    category = get_category(topic, lang)
    if category:
        return {"type": "predefined", "response": category}

    # Fallback: check blog
    blog_result = lookup_blog(topic, lang)
    if blog_result:
        return {"type": "blog", "response": blog_result}

    # Optional: check responses.py
    resp = get_response(topic, lang)
    if resp:
        return {"type": "response", "response": resp}

    return None
