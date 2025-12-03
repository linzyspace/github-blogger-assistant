import yaml
import os

def get_category(topic: str, lang: str):
    base_path = os.path.join(os.path.dirname(__file__), "data")
    file_path = os.path.join(base_path, "categories.yaml")
    
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        categories = yaml.safe_load(f)

    return categories.get(topic)

