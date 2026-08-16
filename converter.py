from validation import validate_conversion_scales, validate_temperature


def to_celsius(value: float, scale: str) -> float:
    """Преобразовать температуру из указанной шкалы в Цельсий."""
    if scale == "C":
        return value
    if scale == "F":
        return (value - 32) * 5 / 9
    if scale == "K":
        return value - 273.15
    if scale == "RE":
        return value * 5 / 4
    if scale == "R":
        return value * 5 / 9 - 273.15
    if scale == "DE":
        return 100 - value * 2 / 3

    raise ValueError(f'Неизвестная температурная шкала: "{scale}".')


def from_celsius(value: float, scale: str) -> float:
    """Преобразовать температуру из Цельсия в указанную шкалу."""
    if scale == "C":
        return value
    if scale == "F":
        return value * 9 / 5 + 32
    if scale == "K":
        return value + 273.15
    if scale == "RE":
        return value * 4 / 5
    if scale == "R":
        return (value + 273.15) * 9 / 5
    if scale == "DE":
        return (100 - value) * 3 / 2

    raise ValueError(f'Неизвестная температурная шкала: "{scale}".')


def convert_temperature(
    value: float,
    from_scale: str,
    to_scale: str,
) -> float:
    """Конвертировать температуру между любыми поддерживаемыми шкалами."""
    normalized_from, normalized_to = validate_conversion_scales(
        from_scale,
        to_scale,
    )
    validate_temperature(value, normalized_from)

    value_in_celsius = to_celsius(value, normalized_from)
    result = from_celsius(value_in_celsius, normalized_to)

    # Проверка результата защищает от физических и вычислительных ошибок.
    validate_temperature(result, normalized_to)
    return result
