#Данный калькулятор написан строго по ТЗ одной задачи с курса https://stepik.org/course/127389

q = input('Введите квадратное уравнение: ').replace(' ', '')

if q.count('x') > 1 and q[q.find('x') + 1] == '=':
    a = q[0:q.find('x')]
    b = q[q.find('x') + 3:q.rfind('x')]
    c = '0'

elif q.count('x') > 1:
    a = q[0:q.find('x')]
    b = q[q.find('x') + 3:q.rfind('x')]
    c = q[q.rfind('x') + 1:q.find('=')]

elif q.count('x') == 1 and q[q.find('x') + 1] == '^':
    a = q[0:q.find('x')]
    b = 0
    c = q[q.rfind('x') + 3:q.find('=')]

elif q.count('x') == 1:
    a = '0'
    b = q[0:q.find('x')]
    c = q[q.rfind('x') + 1:q.find('=')]

print(a, b, c)
def kvad_uravnenie(a, b, c):
    a = int(a)
    b = int(a)
    c = int(a)
    if a == 0:
        x = round((-1 * c) / b, 2)
        return [x]
    D = b * b - 4 * a * c
    if D > 0:
        x1 = round((-b + D ** 0.5) / (2 * a), 2)
        x2 = round((-b - D ** 0.5) / (2 * a), 2)
        return [x1, x2]
    elif D == 0:
        x = round((-b) / (2 * a), 2)
        return [x]
    else:
        return ['Уравнение не имеет действительных решений']



if 'Уравнение не имеет действительных решений' in kvad_uravnenie(a, b, c):
    print(kvad_uravnenie(a, b, c)[0])
elif q.count('x') > 1:
    print(f'x1 = {kvad_uravnenie(a, b, c)[0]}\nx2 = {kvad_uravnenie(a, b, c)[1]}')
elif q.count('x') == 1:
    print(f'x = {kvad_uravnenie(a, b, c)[0]}')
