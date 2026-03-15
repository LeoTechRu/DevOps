#Находим дубликаты символов в ведённой строке, игнорируя пробел. Выводим символ и его количество в строке. 

def agent_P():
    txt = input()
    txt2 = ''
    for i in txt:
        if i!=' ' and i not in txt2:
            txt2+=i
            txt2 += str(txt.count(i))
            if txt.count(i)>1:
                continue
    print(txt2)
agent_P()
