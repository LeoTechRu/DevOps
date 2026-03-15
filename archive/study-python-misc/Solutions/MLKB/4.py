"""Вводится строка. Превратить строку в список, разбив строку на слова и вывести список в обратном порядке.
Ввод:Death there mirth way the noisy merit
Вывод:['merit', 'noisy', 'the', 'way', 'mirth', 'there', 'Death']"""
print(list(reversed("Death there mirth way the noisy merit".split())))
# Сплитанул строку, сделал её реверс и вывел итоговый список. Переменные не использую без необходимости.
"""Вводится строка из не менее 15 символов, выводятся символы с чётными номерами (нумерация с 0).
Ввод: In the hole in the ground there lived a hobbit
Вывод: I h oei h rudteelvdahbi"""
print('In the hole in the ground there lived a hobbit'[::2])  # Вывел каждый второй символ

"""Ввод: список чисел через пробел и натуральное число n - степень. Возвести в заданную степень n все введенные числа.
Ввод:3 5 -7 -13 43 8 0 -13 8 -1 2
Вывод: [9, 25, 49, 169, 1849, 64, 0, 169, 64, 1]"""
List1 = list(map(int, '3 5 -7 -13 43 8 0 -13 8 -1 2'.split()))  # Сплитанул, перевёл в целочисленные
for i in List1[:-1:]:  # на уровне цикла убрал включение последнего символа
    List1[List1.index(i)] = i ** List1[-1]  # заменяю каждое значение на возведённое в степень
print(List1)  # Вывел итог

"""Вводится строка с текстом и символ. Требуется удвоить вхождение введённого символа в текст. 
Текст состоит из слов, записанных латинскими буквами через пробел, знаков препинания.
Подсказка: вспомните, как работает метод  replace"""
Str1 = 'In the hole, in the ground there lived a hobbit!'  # Строка согласно ТЗ
print(Str1.replace(Str1[-1], Str1[-1] * 2))  # Удваиваем, как и просили

"""Дана строка. Программа подсчитывает количество символов x и y и выводит строку вида "x: (число), y: (число)."
Подсказка: вспомните метод count, изученный на занятии"""
Str2 = 'In the hole, in the ground there lived a hobbit!'
print(Str2.count('x'), Str2.count('y'))

"""Вводится текст со сбалансированными скобками, программа выводит на экран текст без скобок и их содержимого. 
На пробелы и знаки препинания внимание не обращать, вложенных скобок в исходной строке нет.
Подсказка: вспомните метод find, изученный на занятии.
Ввод:When he saw Sally (a girl he used to go to school with) in the shop, he could not believe his eyes. 
She was fantastic (as always)!
Вывод: a girl he used to go to school with
as always"""
text = "'When (he saw) (S)ally (a girl he used to go to school with) in the shop, he could not believe ''his eyes. ''She (was fantastic) (as always)!')"
res = ""

while '(' in text:
    res += text[text.find('(') + 1:text.find(')')] + '\n'
    text = text[:text.find('(')] + text[text.find(')') + 1:]

print(res)
#Либо так:
text = input()
res = ""

for i in range(text.find('(')):
    res += text[text.find('(') + 1:text.find(')')] + '\n'
    text = text[:text.find('(')] + text[text.find(')') + 1:]

print(res)
