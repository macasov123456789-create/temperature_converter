from datetime import datetime
from pathlib import Path

from constants import HISTORY_FILE, SCALE_SYMBOLS


def format_temperature(value: float, scale: str, decimals: int = 2) -> str:
    """Отформатировать температуру с корректным обозначением единицы."""
    return f"{value:.{decimals}f} {SCALE_SYMBOLS[scale]}"


def save_history(
    value: float,
    from_scale: str,
    result: float,
    to_scale: str,
    history_path: Path = HISTORY_FILE,
) -> str:
    """Добавить успешную конвертацию в файл истории."""
    history_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = (
        f"{timestamp} | {format_temperature(value, from_scale)} -> "
        f"{format_temperature(result, to_scale)}"
    )

    with history_path.open("a", encoding="utf-8") as file:
        file.write(record + "\n")

    return record


def get_history(history_path: Path = HISTORY_FILE) -> list[str]:
    """Получить непустые строки истории."""
    if not history_path.exists():
        return []

    try:
        with history_path.open("r", encoding="utf-8") as file:
            return [line.rstrip("\n") for line in file if line.strip()]
    except OSError as exc:
        raise OSError(f"Не удалось прочитать историю: {exc}") from exc


def show_history(history_path: Path = HISTORY_FILE) -> None:
    """Вывести историю конвертаций в консоль."""
    try:
        records = get_history(history_path)
    except OSError as exc:
        print(f"\nОшибка: {exc}")
        return

    print("\n========== ИСТОРИЯ ==========")

    if not records:
        print("История пока пуста.")
    else:
        for index, record in enumerate(records, start=1):
            print(f"{index}. {record}")

    print("==============================")
