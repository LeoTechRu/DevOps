"""Задание 1:
Напишите программу, которая будет находить наименьшее общее кратное двух чисел.
Ввод: два числа a и b
Вывод: наименьшее общее кратное чисел a и b"""


def find_lcm(a, b):
    max_num = max(a, b)
    lcm = max_num
    while True:
        if lcm % a == 0 and lcm % b == 0:
            break
        lcm += max_num
    return lcm


print("Наименьшее общее кратное:", find_lcm(int(input("Введите первое число: ")), int(input("Введите второе число: "))))
"""Задание 2:
Напишите программу, которая будет находить все простые числа от 1 до n.
Ввод: число n
Вывод: список простых чисел от 1 до n"""


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


n = int(input("Введите число: "))

print(f"Список простых чисел:, {[num for num in range(1, n + 1) if is_prime(num)]}")

"""Задание 3:
Напишите программу, которая будет находить все делители числа n.
Ввод: число n
Вывод: список делителей числа n"""
n = int(input("Введите число: "))

print(f"Список делителей числа {n}: {[num for num in range(1, n + 1) if n %num == 0]}")
