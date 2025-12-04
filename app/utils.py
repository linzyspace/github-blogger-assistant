import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_yaml(filename: str):
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {filename}")
    with open(path, "r") as f:
        return yaml.safe_load(f)
