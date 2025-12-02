import yaml
import os

DATA_PATH = "app/data/responses.yaml"

def load_responses():
    with open(DATA_PATH, "r") as f:
        return yaml.safe_load(f)

def get_predefined_response(text: str, lang: str = "en"):
    responses = load_responses()
    t = text.lower()

    for entry in responses:
        if any(keyword in t for keyword in entry.get("keywords", [])):
            return entry.get("responses", {}).get(lang) or entry.get("responses", {}).get("en")

    return None

