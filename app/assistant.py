from app.responses import find_predefined_response
from app.blog_lookup import find_blog_match

def get_predefined_or_blog_response(topic: str, lang: str):
    predefined = find_predefined_response(topic, lang)
    if predefined:
        return {"type": "predefined", "response": predefined}

    blog = find_blog_match(topic, lang)
    if blog:
        return {"type": "blog", "response": blog}

    return None
