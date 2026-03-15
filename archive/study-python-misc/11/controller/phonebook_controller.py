# C:\Users\leon\PycharmProjects\studyPython\13\controller\phonebook_controller.py
from model.exceptions import PhoneBookError, ContactNotFoundError
from view.console_view import ConsoleView


class PhoneBookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        """Запускает основной цикл программы"""
        print("Добро пожаловать в телефонный справочник!")

        while True:
            self.view.show_menu()
            choice = self.view.get_user_choice()

            try:
                if choice == "1":
                    contacts = self.model.get_all()
                    self.view.show_contacts(contacts)

                elif choice == "2":
                    name, phone, comment = self.view.get_contact_input()
                    contact = self.model.add(name, phone, comment)
                    self.view.show_message(f"Контакт добавлен: {contact}")

                elif choice == "3":
                    query = self.view.get_search_query()
                    results = self.model.search(query)
                    self.view.show_message(f"Найдено {len(results)} контактов:")
                    self.view.show_contacts(results)


                elif choice == "4":
                    contact_id = self.view.get_contact_id()
                    try:
                        contact_id = int(contact_id)
                        # Найти контакт в модели
                        contact_to_edit = None

                        for contact in self.model.contacts:
                            if contact.id == contact_id:
                                contact_to_edit = contact
                                break
                        if not contact_to_edit:
                            self.view.show_message("Контакт с таким ID не найден.")
                            continue
                        # Получить новые данные
                        name, phone, comment = self.view.get_edit_input(contact_to_edit)
                        # Редактировать контакт
                        updated = self.model.edit(contact_id, name, phone, comment)
                        self.view.show_message(f"Контакт обновлен: {updated}")
                    except ValueError:
                        self.view.show_message("Некорректный ID. Введите число.")


                elif choice == "5":
                    contact_id = self.view.get_contact_id()
                    try:
                        self.model.delete(contact_id)
                        self.view.show_message("Контакт удален.")
                    except ContactNotFoundError as e:
                        self.view.show_message(str(e))
                    except ValueError:
                        self.view.show_message("Некорректный ID. Введите число.")

                elif choice == "6":
                    self.view.show_message("Выход из программы")
                    break

                else:
                    self.view.show_message("Некорректный выбор. Пожалуйста, введите число от 1 до 6.")

            except PhoneBookError as e:
                self.view.show_message(f"Ошибка: {str(e)}")