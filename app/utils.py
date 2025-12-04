import pathlib
import yaml
from typing import Any

BASE_DIR = pathlib.Path(__file__).parent

def load_yaml(filename: str) -> Any:
    """
    Load a YAML file from app/data safely.
    """
    path = BASE_DIR / "data" / filename
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

