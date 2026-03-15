import string as st

special = '_!@#$%^&'
_allowed = set(st.digits + st.ascii_lowercase + st.ascii_uppercase + special)


def check_password(pwd):
    """
    Проверка пароля по правилам задачи.

    Возвращает:
        (True, "пароль подходит") или (False, "пояснение что исправить")
    """
    reasons = []

    # 1) Длина
    if len(pwd) < 8:
        reasons.append("длина меньше 8 символов")
    if len(pwd) > 15:
        reasons.append("длина больше 15 символов")

    # 2) Наличие обязательных типов символов
    if not any(ch in st.digits for ch in pwd):
        reasons.append("добавьте хотя бы одну цифру")
    if not any(ch in st.ascii_lowercase for ch in pwd):
        reasons.append("добавьте хотя бы одну строчную латинскую букву")
    if not any(ch in st.ascii_uppercase for ch in pwd):
        reasons.append("добавьте хотя бы одну прописную (заглавную) латинскую букву")
    if not any(ch in special for ch in pwd):
        reasons.append(f"добавьте хотя бы один спецсимвол из набора: {special}")

    # 3) Только разрешённые символы
    invalid = [ch for ch in pwd if ch not in _allowed]
    if invalid:
        # Выводим уникальные запрещённые символы для наглядности
        uniq = "".join(sorted(set(invalid)))
        reasons.append(f"обнаружены запрещённые символы: {repr(uniq)}")

    if reasons:
        return (False, "; ".join(reasons))
    return (True, "пароль подходит")


def main():
    max_tries = 5
    for attempt in range(1, max_tries + 1):
        pwd = input(f"Попытка {attempt}/{max_tries}. Введите пароль: ")
        ok, msg = check_password(pwd)
        if ok:
            print(f"Пароль подходит -> {pwd}")
            return
        else:
            print("Пароль не подходит:", msg)

    print("Превышено число попыток. Доступ запрещён.")


if __name__ == "__main__":
    main()
