import json
import os

CONTACTS_FILE = "contacts.json"


def load_contacts():
    """Загружает контакты из файла JSON с обработкой ошибок"""
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:  # Пустой файл
                    raise ValueError("Файл пустой")
                return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            print("Файл поврежден. Создается новый файл.")
            save_contacts([])  # Перезаписываем поврежденный файл
    return []


def save_contacts(contacts):
    """Сохраняет контакты в файл JSON с обработкой ошибок"""
    try:
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, ensure_ascii=False, indent=4)
        return True
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")
        return False


def show_all_contacts(contacts):
    """Выводит все контакты"""
    if not contacts:
        print("Телефонный справочник пуст.")
        return
    for contact in contacts:
        print(f"ID: {contact['id']}, Имя: {contact['name']}, "
              f"Телефон: {contact['phone']}, Комментарий: {contact['comment']}")


def create_contact(contacts):
    """Создает новый контакт и сразу сохраняет в файл"""
    name = input("Введите имя: ").strip()
    phone = input("Введите номер телефона: ").strip()
    comment = input("Введите комментарий: ").strip()

    new_id = max((c["id"] for c in contacts), default=0) + 1
    contacts.append({
        "id": new_id,
        "name": name,
        "phone": phone,
        "comment": comment
    })

    if save_contacts(contacts):
        print("Контакт добавлен и сохранен.")
    else:
        print("Контакт добавлен в память, но не сохранен в файл!")


def find_contact(contacts):
    """Ищет контакт по ключевому слову во всех полях"""
    query = input("Введите поисковое слово: ").lower().strip()
    results = [c for c in contacts if any(query in str(v).lower() for v in c.values())]

    if results:
        print(f"\nРезультаты поиска ({len(results)}):")
        show_all_contacts(results)
    else:
        print("Контакты не найдены.")


def edit_contact(contacts):
    """Изменяет существующий контакт"""
    try:
        contact_id = int(input("Введите ID контакта для изменения: "))
        for contact in contacts:
            if contact["id"] == contact_id:
                contact["name"] = input(f"Новое имя ({contact['name']}): ").strip() or contact["name"]
                contact["phone"] = input(f"Новый телефон ({contact['phone']}): ").strip() or contact["phone"]
                contact["comment"] = input(f"Новый комментарий ({contact['comment']}): ").strip() or contact["comment"]

                if save_contacts(contacts):
                    print("Контакт успешно обновлен и сохранен.")
                else:
                    print("Контакт изменен, но не сохранен в файл!")
                return
        print("Контакт с таким ID не найден.")
    except ValueError:
        print("Некорректный ввод ID. Введите число.")


def delete_contact(contacts):
    """Удаляет контакт по ID"""
    try:
        contact_id = int(input("Введите ID контакта для удаления: "))
        for i, contact in enumerate(contacts):
            if contact["id"] == contact_id:
                del contacts[i]
                if save_contacts(contacts):
                    print("Контакт удален и изменения сохранены.")
                else:
                    print("Контакт удален из памяти, но не сохранен в файл!")
                return
        print("Контакт с таким ID не найден.")
    except ValueError:
        print("Некорректный ввод ID. Введите число.")


def main():
    contacts = load_contacts()
    print(f"Файл контактов: {os.path.abspath(CONTACTS_FILE)}")  # Информация о расположении файла

    while True:
        print("\nМеню телефонного справочника:")
        print("1. Показать все контакты")
        print("2. Добавить контакт")
        print("3. Найти контакт")
        print("4. Изменить контакт")
        print("5. Удалить контакт")
        print("6. Сохранить файл")
        print("7. Выйти")

        choice = input("Выберите действие (1-7): ").strip()

        if choice == "1":
            show_all_contacts(contacts)
        elif choice == "2":
            create_contact(contacts)
        elif choice == "3":
            find_contact(contacts)
        elif choice == "4":
            edit_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            if save_contacts(contacts):
                print("Файл успешно сохранен.")
            else:
                print("Ошибка сохранения файла!")
        elif choice == "7":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите число от 1 до 7.")


if __name__ == "__main__":
    main()