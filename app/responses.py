from app.utils import load_yaml

responses = load_yaml("responses.yaml")

def find_predefined_response(topic: str, lang: str):
    lang_responses = responses.get(lang, {})

    for key, value in lang_responses.items():
        if key.lower() in topic.lower():
            return value

    return None
