import math

def sqrt(x):
    return math.sqrt(x)
def pow(x, k):
    return x ** k
def sqr(x):
    return x ** 2
def sin(x):
    return(math.sin(x))
def cos(x):
    return(math.cos(x))
def tg(x):
    return math.tan(x)
def ctg(x):
    return 1 / math.tan(x)
def log2(x):
    return math.log2(x)
def log10(x):
    return math.log10(x)
def log(x, k):
    return math.log(x) / math.log(k)

commands = ('+', '-', '*', '/', 'sqrt', 'pow', 'sqr', 'sin', 'cos', 'tg', 'ctg', 'log2', 'log10', 'log')
print('Доступные команды:', str(commands).replace('\'', '').replace('(', '').replace(')', ''))
while True:
    chose = input('Введите команду: ')
    if commands.count(chose) != 0:
        if '+-/*'.find(chose) != -1:
            a = float(eval(input('Введите первое число: ')))
            b = float(eval(input('Введите второе число: ')))
            if chose == '/' and b == 0:
                print('Деление на 0!')
            else:
                print('Результат:', eval(str(a)+chose+str(b)))
        elif chose != 'log' and chose != 'pow':
            a = float(eval(input('Введите число: ')))
            if chose == 'sqrt' and a < 0:
                print('Корень отрицательного числа!')
            else:
                print('Результат:', eval(chose+'('+str(a)+')'))
        else:
            a = float(eval(input('Введите первое число: ')))
            b = float(eval(input('Введите второе число: ')))
            if chose == 'pow' and a == 0 and b == 0:
                print('0 в 0 степени!')
            elif chose == 'pow' and complex(pow(a, b)).imag != 0:
                print('Ошибка!')
            elif chose == 'log' and (a <= 0 or b <= 0 or b == 1):
                print('Неправильный ввод!')
            else:
                print('Результат:', eval(chose+'('+str(a)+','+str(b)+')'))

    else:
        try:
            print(eval(chose))
        except: 
            print('Неверная команда!')
    if (''.find(input('Для выхода их калькулятора введите любой символ: ')) == -1):
        break
    print()