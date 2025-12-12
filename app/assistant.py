from app.responses import PREDEFINED_REPLIES
from app.blog_lookup import find_blog_match

def find_predefined_response(topic: str):
    topic = topic.lower().strip()
    for item in PREDEFINED_REPLIES:
        if any(word in topic for word in item["keywords"]):
            return item["reply"]
    return None

def get_predefined_or_blog_response(topic: str):
    # 1️⃣ Predefined reply
    predefined = find_predefined_response(topic)
    if predefined:
        return {"type": "predefined", "match": "keyword", "response": predefined}

    # 2️⃣ Blog post
    blog = find_blog_match(topic)
    if blog:
        return {"type": "blog", "match": "blogger", "response": blog}

    # 3️⃣ Nothing found
    return {"type": "none", "response": "No predefined answer and no blog posts found."}
