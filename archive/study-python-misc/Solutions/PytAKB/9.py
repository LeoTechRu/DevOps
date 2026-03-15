"""Импортируйте библиотеку Tkinter в вашем Python-скрипте.
Создайте основное окно приложения.
Добавьте виджет Entry (поле для ввода текста) в основное окно.
Создайте кнопку (Button), которая будет запускать функцию при нажатии.
Создайте функцию, которая будет вызываться при нажатии кнопки и будет отображать
введенный пользователем текст в новом окне или под полем для ввода.
Добавьте кнопку которая будет очищать поле ввода.
Добавьте проверку, чтобы при попытке запустить с пустым полем выводилось сообщение что поле пустое."""
import tkinter as tk
from tkinter import messagebox

def displaytext():
    if entry.get() == "":
        messagebox.showinfo("Ошибка", "Поле пустое.")
    else:
        messagebox.showinfo("Введенный текст", entry.get())

def cleartext():
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Мое приложение")

entry = tk.Entry(root)
entry.pack()

buttondisplay = tk.Button(root, text="Показать текст", command=displaytext)
buttondisplay.pack()

buttonclear = tk.Button(root, text="Очистить поле", command=cleartext)
buttonclear.pack()

root.mainloop()