# C:\Users\leon\PycharmProjects\studyPython\13\view\console_view.py
class ConsoleView:
    def show_menu(self):
        """Показывает меню"""
        print("\nМеню телефонного справочника:")
        print("1. Показать все контакты")
        print("2. Добавить контакт")
        print("3. Найти контакт")
        print("4. Изменить контакт")
        print("5. Удалить контакт")
        print("6. Выход")

    def get_user_choice(self):
        """Получает выбор пользователя"""
        return input("Выберите действие (1-6): ").strip()

    def show_contacts(self, contacts):
        """Показывает список контактов"""
        if not contacts:
            print("Телефонный справочник пуст.")
            return

        for contact in contacts:
            print(str(contact))

    def show_message(self, message):
        """Показывает сообщение"""
        print(message)

    def get_contact_input(self):
        """Получает данные для нового контакта"""
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        comment = input("Введите комментарий: ")
        return name, phone, comment

    def get_search_query(self):
        """Получает поисковый запрос"""
        return input("Введите поисковое слово: ")

    def get_edit_input(self, contact):
        """Получает данные для редактирования контакта"""
        print(f"Текущие данные: {contact}")
        name = input(f"Новое имя ({contact.name}): ").strip() or None
        phone = input(f"Новый телефон ({contact.phone}): ").strip() or None
        comment = input(f"Новый комментарий ({contact.comment}): ").strip() or None
        return name, phone, comment

    def get_contact_id(self):
        """Получает ID контакта"""
        return input("Введите ID контакта: ").strip()