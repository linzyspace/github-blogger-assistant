from app.utils import load_yaml

categories = load_yaml("categories.yaml")

def find_blog_match(topic: str, lang: str):
    lang_cats = categories.get(lang, {})

    for key, value in lang_cats.items():
        if key.lower() in topic.lower():
            return f"Blog post match found: {value}"

    return None
