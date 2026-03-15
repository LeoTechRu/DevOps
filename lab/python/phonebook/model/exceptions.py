# C:\Users\leon\PycharmProjects\studyPython\13\model\exceptions.py
class PhoneBookError(Exception):
    """Базовый класс для ошибок телефонного справочника"""
    pass

class FileReadError(PhoneBookError):
    """Ошибка чтения файла"""
    def __init__(self, message="Не удалось прочитать файл"):
        self.message = message
        super().__init__(message)

class FileWriteError(PhoneBookError):
    """Ошибка записи файла"""
    def __init__(self, message="Не удалось записать в файл"):
        self.message = message
        super().__init__(message)

class ContactNotFoundError(PhoneBookError):
    """Контакт не найден"""
    def __init__(self, contact_id=None):
        self.message = f"Контакт с ID {contact_id} не найден" if contact_id else "Контакт не найден"
        super().__init__(self.message)

class InvalidContactDataError(PhoneBookError):
    """Некорректные данные контакта"""
    def __init__(self, message="Некорректные данные контакта"):
        self.message = message
        super().__init__(message)