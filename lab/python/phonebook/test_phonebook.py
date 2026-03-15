# C:\Users\leon\PycharmProjects\studyPython\13\test_phonebook.py
import pytest
import os
from model.phonebook import PhoneBook
from model.contact import Contact
from model.exceptions import (
    FileReadError, FileWriteError, ContactNotFoundError, InvalidContactDataError
)


# Фикстура для создания временного телефонного справочника
@pytest.fixture
def phonebook(tmpdir):
    """Создает временный файл контактов и возвращает экземпляр PhoneBook"""
    contacts_file = tmpdir.join("contacts.json")
    PhoneBook.CONTACTS_FILE = str(contacts_file)
    book = PhoneBook()
    # Очистка контактов перед каждым тестом
    book.contacts = []
    book._save_contacts()
    return book


# Тесты для базовых операций
def test_add_contact(phonebook):
    contact = phonebook.add("Иван", "+79031234567", "Работа")
    assert contact.name == "Иван"
    assert contact.phone == "+79031234567"
    assert contact.comment == "Работа"
    assert len(phonebook.get_all()) == 1


def test_add_invalid_contact(phonebook):
    with pytest.raises(InvalidContactDataError):
        phonebook.add("", "+79031234567", "Работа")  # Пустое имя
    with pytest.raises(InvalidContactDataError):
        phonebook.add("Иван", "", "Работа")  # Пустой телефон


def test_edit_contact(phonebook):
    contact = phonebook.add("Иван", "+79031234567", "Работа")
    updated = phonebook.edit(contact.id, name="Петр", phone="+79037654321")
    assert updated.name == "Петр"
    assert updated.phone == "+79037654321"


def test_edit_nonexistent_contact(phonebook):
    with pytest.raises(ContactNotFoundError):
        phonebook.edit(999, name="Неизвестный")  # Несуществующий ID


def test_delete_contact(phonebook):
    contact = phonebook.add("Иван", "+79031234567", "Работа")
    phonebook.delete(contact.id)
    assert len(phonebook.get_all()) == 0


def test_delete_nonexistent_contact(phonebook):
    with pytest.raises(ContactNotFoundError):
        phonebook.delete(999)  # Несуществующий ID


def test_search_contact(phonebook):
    phonebook.add("Иван", "+79031234567", "Работа")
    phonebook.add("Петр", "+79037654321", "Дом")

    results = phonebook.search("Иван")
    assert len(results) == 1
    assert results[0].name == "Иван"

    results = phonebook.search("+79037654321")
    assert len(results) == 1
    assert results[0].phone == "+79037654321"


# Тесты для работы с файлами
def test_file_corruption_recovery(tmpdir):
    contacts_file = tmpdir.join("contacts.json")
    contacts_file.write(b'{"invalid": ')  # Поврежденный JSON в байтах

    PhoneBook.CONTACTS_FILE = str(contacts_file)
    try:
        book = PhoneBook()
        assert len(book.get_all()) == 0  # Ожидается пустой список
    except FileReadError:
        pytest.fail("Файл должен быть восстановлен автоматически")


def test_file_permissions(tmpdir, monkeypatch):
    contacts_file = tmpdir.join("contacts.json")
    PhoneBook.CONTACTS_FILE = str(contacts_file)

    # Блокируем запись в файл
    def mock_open(*args, **kwargs):
        raise PermissionError("Нет прав на запись")

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(FileWriteError):
        book = PhoneBook()
        book.add("Иван", "+79031234567", "Работа")


# Параметризованные тесты
@pytest.mark.parametrize("name, phone, comment, expected_error", [
    ("Иван", "+79031234567", "Работа", None),
    ("Петр", "+79037654321", "", None),  # Пустой комментарий
    ("", "+79031234567", "Работа", InvalidContactDataError),  # Пустое имя
    ("Иван", "", "Работа", InvalidContactDataError),  # Пустой телефон
    ("   ", "+79031234567", "Работа", InvalidContactDataError),  # Пробелы в имени
])
def test_add_contact_variants(name, phone, comment, expected_error, phonebook):
    if expected_error:
        with pytest.raises(expected_error):
            phonebook.add(name, phone, comment)
    else:
        contact = phonebook.add(name, phone, comment)
        assert contact.name == name.strip()
        assert contact.phone == phone.strip()
        assert contact.comment == comment.strip()


# Тесты для граничных условий
def test_empty_search(phonebook):
    results = phonebook.search("")
    assert len(results) == 0  # Пустой запрос не должен вызывать ошибок


def test_search_nonexistent(phonebook):
    results = phonebook.search("Неизвестный")
    assert len(results) == 0  # Поиск несуществующего контакта


def test_large_id(phonebook):
    contact = phonebook.add("Иван", "+79031234567", "Работа")
    with pytest.raises(ContactNotFoundError):
        phonebook.delete(contact.id + 1000)  # Большой ID