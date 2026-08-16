from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
HISTORY_FILE = DATA_DIR / "history.txt"
INPUT_FILE = DATA_DIR / "input.txt"
OUTPUT_FILE = DATA_DIR / "output.txt"

SCALE_NAMES = {
    "C": "Цельсий",
    "F": "Фаренгейт",
    "K": "Кельвин",
    "RE": "Реомюр",
    "R": "Ранкин",
    "DE": "Делиль",
}

SCALE_SYMBOLS = {
    "C": "°C",
    "F": "°F",
    "K": "K",
    "RE": "°Re",
    "R": "°R",
    "DE": "°De",
}

TEMPERATURE_LIMITS = {
    "C": {"min": -273.15, "max": None},
    "F": {"min": -459.67, "max": None},
    "K": {"min": 0.0, "max": None},
    "RE": {"min": -218.52, "max": None},
    "R": {"min": 0.0, "max": None},
    "DE": {"min": None, "max": 559.725},
}
