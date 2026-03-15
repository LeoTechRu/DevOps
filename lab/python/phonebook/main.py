# C:\Users\leon\PycharmProjects\studyPython\13\main.py
from model.phonebook import PhoneBook
from view.console_view import ConsoleView
from controller.phonebook_controller import PhoneBookController


def main():
    try:
        # Инициализация компонентов
        model = PhoneBook()
        view = ConsoleView()
        controller = PhoneBookController(model, view)

        # Запуск приложения
        controller.run()

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        print("Программа будет завершена.")


if __name__ == "__main__":
    main()