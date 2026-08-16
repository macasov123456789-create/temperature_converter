from pathlib import Path

from constants import INPUT_FILE, OUTPUT_FILE, SCALE_SYMBOLS
from converter import convert_temperature
from history import save_history
from validation import normalize_scale, parse_temperature


def _process_line(line: str) -> tuple[float, str, float, str]:
    parts = [part.strip() for part in line.split(";")]

    if len(parts) != 3 or any(not part for part in parts):
        raise ValueError(
            "ожидается формат: значение;исходная_шкала;целевая_шкала"
        )

    value_text, from_scale_text, to_scale_text = parts
    value = parse_temperature(value_text)
    from_scale = normalize_scale(from_scale_text)
    to_scale = normalize_scale(to_scale_text)
    result = convert_temperature(value, from_scale, to_scale)

    return value, from_scale, result, to_scale


def process_batch_file(
    input_path: str | Path = INPUT_FILE,
    output_path: str | Path = OUTPUT_FILE,
) -> None:
    """Обработать файл температур, не останавливаясь из-за ошибок строк."""
    input_file = Path(input_path)
    output_file = Path(output_path)

    print(f"\nОбработка файла {input_file.name}\n")

    if not input_file.exists():
        print(f"Ошибка: файл {input_file} не найден.")
        return

    try:
        lines = input_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        print(f"Ошибка: не удалось прочитать файл {input_file}: {exc}")
        return

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_lines: list[str] = []
    successful = 0
    errors = 0
    processed = 0

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        processed += 1

        try:
            value, from_scale, result, to_scale = _process_line(line)
            message = (
                f"Строка {line_number}: "
                f"{value:g} {SCALE_SYMBOLS[from_scale]} -> "
                f"{result:.2f} {SCALE_SYMBOLS[to_scale]}"
            )
            print(message)
            output_lines.append(message)
            save_history(value, from_scale, result, to_scale)
            successful += 1
        except (ValueError, OSError) as exc:
            message = f"Строка {line_number}: ошибка — {exc}"
            print(message)
            output_lines.append(message)
            errors += 1

    summary = (
        f"\nОбработано: {processed}\n"
        f"Успешно: {successful}\n"
        f"Ошибок: {errors}"
    )
    print(summary)
    output_lines.extend(["", *summary.splitlines()])

    try:
        output_file.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"Ошибка: не удалось записать файл {output_file}: {exc}")
