import json
from pathlib import Path


def read_json(path: str | Path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: str | Path, data: dict | list) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def format_percentage(value: float, decimals: int = 2) -> str:
    return f"{value * 100:.{decimals}f}%"
