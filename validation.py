from math import isclose, isfinite

from constants import SCALE_NAMES, SCALE_SYMBOLS, TEMPERATURE_LIMITS


BOUNDARY_TOLERANCE = 1e-12


_SCALE_ALIASES = {
    "C": "C",
    "CELSIUS": "C",
    "ЦЕЛЬСИЙ": "C",
    "ЦЕЛЬСИЯ": "C",
    "F": "F",
    "FAHRENHEIT": "F",
    "ФАРЕНГЕЙТ": "F",
    "ФАРЕНГЕЙТА": "F",
    "K": "K",
    "KELVIN": "K",
    "КЕЛЬВИН": "K",
    "КЕЛЬВИНА": "K",
    "RE": "RE",
    "RÉAUMUR": "RE",
    "REAUMUR": "RE",
    "РЕОМЮР": "RE",
    "РЕОМЮРА": "RE",
    "R": "R",
    "RANKINE": "R",
    "РАНКИН": "R",
    "РАНКИНА": "R",
    "DE": "DE",
    "DELISLE": "DE",
    "ДЕЛИЛЬ": "DE",
    "ДЕЛИЛЯ": "DE",
}


def parse_temperature(value: str) -> float:
    """Преобразовать строку в конечное число с плавающей точкой."""
    normalized_value = value.strip().replace(",", ".")

    if not normalized_value:
        raise ValueError("Введите числовое значение.")

    try:
        number = float(normalized_value)
    except ValueError as exc:
        raise ValueError("Введите числовое значение.") from exc

    if not isfinite(number):
        raise ValueError("Температура должна быть конечным числом.")

    return number


def normalize_scale(scale: str) -> str:
    """Привести обозначение или название шкалы к внутреннему коду."""
    normalized_scale = scale.strip().upper()

    try:
        return _SCALE_ALIASES[normalized_scale]
    except KeyError as exc:
        message = f'Неизвестная температурная шкала: "{scale.strip()}".'
        raise ValueError(message) from exc


def validate_temperature(value: float, scale: str) -> None:
    """Проверить температуру с учётом физических границ шкалы."""
    normalized_scale = normalize_scale(scale)

    if not isfinite(value):
        raise ValueError("Температура должна быть конечным числом.")

    limits = TEMPERATURE_LIMITS[normalized_scale]
    minimum = limits["min"]
    maximum = limits["max"]

    if (
        minimum is not None
        and value < minimum
        and not isclose(value, minimum, rel_tol=0.0, abs_tol=BOUNDARY_TOLERANCE)
    ):
        symbol = SCALE_SYMBOLS[normalized_scale]
        raise ValueError(
            f"Значение {value:g} {symbol} невозможно: температура не может "
            f"быть ниже абсолютного нуля ({minimum:g} {symbol})."
        )

    if (
        maximum is not None
        and value > maximum
        and not isclose(value, maximum, rel_tol=0.0, abs_tol=BOUNDARY_TOLERANCE)
    ):
        symbol = SCALE_SYMBOLS[normalized_scale]
        raise ValueError(
            f"Значение {value:g} {symbol} невозможно: оно соответствует "
            "температуре ниже абсолютного нуля "
            f"(максимально допустимо {maximum:g} {symbol})."
        )


def validate_conversion_scales(from_scale: str, to_scale: str) -> tuple[str, str]:
    """Нормализовать две шкалы и проверить, что они различаются."""
    normalized_from = normalize_scale(from_scale)
    normalized_to = normalize_scale(to_scale)

    if normalized_from == normalized_to:
        name = SCALE_NAMES[normalized_from]
        raise ValueError(f"Исходная и целевая шкалы совпадают ({name}).")

    return normalized_from, normalized_to
