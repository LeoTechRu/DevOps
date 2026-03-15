def decoder(arg):
    for i in arg:
        if i == ' ':
            continue
        else:
            a, b = (input().replace(' ', '')).split('-')
            arg = arg.replace(a,b)
    return arg, a, b
print(decoder(input()))