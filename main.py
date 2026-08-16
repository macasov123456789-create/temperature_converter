from batch import process_batch_file
from constants import SCALE_NAMES, SCALE_SYMBOLS
from converter import convert_temperature
from history import save_history, show_history
from validation import parse_temperature, validate_temperature


SCALE_MENU = {
    "1": "C",
    "2": "F",
    "3": "K",
    "4": "RE",
    "5": "R",
    "6": "DE",
}


def print_main_menu() -> None:
    print(
        "\n====================================\n"
        "       КОНВЕРТЕР ТЕМПЕРАТУР\n"
        "====================================\n\n"
        "1. Конвертировать температуру\n"
        "2. Просмотреть историю\n"
        "3. Пакетная конвертация из файла\n"
        "4. Справка по шкалам\n"
        "0. Выход\n"
    )


def print_scale_menu() -> None:
    print("\nДоступные шкалы:\n")
    for number, scale in SCALE_MENU.items():
        print(f"{number}. {SCALE_NAMES[scale]} ({scale.title()})")


def choose_scale(prompt: str) -> str:
    while True:
        choice = input(prompt).strip()
        scale = SCALE_MENU.get(choice)

        if scale is not None:
            return scale

        print("Ошибка: выберите номер шкалы от 1 до 6.")


def read_temperature(scale: str) -> float:
    while True:
        raw_value = input("Введите температуру: ")

        try:
            value = parse_temperature(raw_value)
            validate_temperature(value, scale)
            return value
        except ValueError as exc:
            print(f"Ошибка: {exc}")


def handle_conversion() -> None:
    print_scale_menu()
    from_scale = choose_scale("\nВыберите исходную шкалу: ")

    while True:
        to_scale = choose_scale("Выберите целевую шкалу: ")
        if to_scale != from_scale:
            break
        print("Ошибка: исходная и целевая шкалы не должны совпадать.")

    while True:
        value = read_temperature(from_scale)

        try:
            result = convert_temperature(value, from_scale, to_scale)
            break
        except ValueError as exc:
            print(f"Ошибка: {exc}")

    print("\nРезультат:\n")
    print(
        f"{value:.2f} {SCALE_SYMBOLS[from_scale]} = "
        f"{result:.2f} {SCALE_SYMBOLS[to_scale]}"
    )

    try:
        save_history(value, from_scale, result, to_scale)
        print("\nОперация сохранена в истории.")
    except OSError as exc:
        print(
            "\nПредупреждение: результат получен, но историю "
            f"сохранить не удалось: {exc}"
        )


def show_scale_help() -> None:
    print("\n========== СПРАВКА ПО ШКАЛАМ ==========")
    for scale, name in SCALE_NAMES.items():
        print(f"{scale.title():>2} — {name}, обозначение: {SCALE_SYMBOLS[scale]}")
    print("========================================")


def main() -> None:
    while True:
        print_main_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            handle_conversion()
        elif choice == "2":
            show_history()
        elif choice == "3":
            process_batch_file()
        elif choice == "4":
            show_scale_help()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Ошибка: неизвестная команда меню.")


if __name__ == "__main__":
    main()
