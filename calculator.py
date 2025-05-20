import functions
import math

def sqrt(x):
    return math.sqrt(x)
def pow(x, k):
    return x ** k
def sqr(x):
    return x ** 2
def sin(x):
    return(math.sin(x / 180 * math.pi))
def cos(x):
    return(math.cos(x / 180 * math.pi))
def tg(x):
    return math.tan(x / 180 * math.pi)
def ctg(x):
    return 1 / math.tan(x / 180 * math.pi)
def log(x, k):
    return math.log(k) / math.log(x)

# все команды
commands = ('+', '-', '*', '/', 'sqrt', 'pow', 'sqr', 'sin', 'cos', 'tg', 'ctg', 'log')

function_recognation = {
    '+': '+',
    'сложить': '+',
    'прибавить': '+',
    'плюс': '+',
    '-': '-',
    'вычесть': '-',
    'минус': '-',
    '*': '*',
    'умножить': '*',
    '/': '/', 
    'разделить': '/',
    'поделить': '/',
    'делить': '/'
}

specific_function_recognition = {
    'корень': 'sqrt',
    'квадрат': 'sqr',
    'синус': 'sin',
    'косинус': 'cos',
    'тангенс': 'tg',
    'котангенс': 'ctg'
}

dificult_function_recognition = {
    'степень': 'pow',
    'логарифм': 'log'
}

# [sin(, [...], )]
# [sin(, [cos(, [1, +, 2], )], )]
# sin(, ..., ) 
def calculator(user_command: str = '') -> str:

    # дебаг режим
    if __name__ == '__main__':
        print('\ndebug', '-'*10, sep='\n')

    # поиск "слов" при неявном вводе
    words: list = []

    # вызов функции с параметром (например, ввод пользователем команды через интерфейс)
    if user_command != '':
        try:
            # попытка вычислить значение выражения в лоб
            if eval(user_command) != '':
                return eval(user_command.replace(' '))
        # разделение команды на список слов
        except:
            words = user_command.split()

    # голосовой ввод
    else:
        words = functions.voice.split()

    # части команды
    command_parts: list = []
    
    # буфер
    buffer: str = ''

    # проходимся по словам (i - номер слова)
    for i in range(len(words)):

        # если найденное слово является числом
        try:
            # добавление числа в command_parts
            number = str(int(words[i]))
            command_parts.append(number)

            # сложить 2 и 3 -> buffer == + -> command_parts == [..., 2, +, 3, ...]
            if buffer != '':
                command_parts.append(buffer)
                buffer = ''
            
        # поиск команды
        except:
            # ()
            if words[i] == 'скобка' or words[i] == '(':
                if i + 1 == len(words):
                    command_parts.append(')')
                elif words[i+1] == 'закрывается':
                    command_parts.append(')')
                else:
                    command_parts.append('(')

            # число pi
            elif words[i] == 'пи':
                command_parts.append('math.pi')
            
            # число e
            elif words[i] == 'е':
                command_parts.append('math.e')
                    
            # + - * /
            elif words[i] in function_recognation:
                if len(command_parts) == 0:
                    buffer = function_recognation[words[i]]
                elif '0' <= command_parts[-1] <= '9' or command_parts[-1] == ')':
                    command_parts.append(function_recognation[words[i]])
                else:
                    buffer = function_recognation[words[i]]
            
            # sqrt(a) sqr(a) sin(a) cos(a) tg(a) ctg(a)
            elif words[i] in specific_function_recognition:
                command_parts.append(specific_function_recognition[words[i]] + '(')
            
            # pow(a,b), log(a, b)
            elif words[i] in dificult_function_recognition:
                command_parts.append(dificult_function_recognition[words[i]] + '(')
                if i+1 < len(words):
                    if words[i+1] == 'десятичный':
                        command_parts.append('10')
                        command_parts.append(',')
                        continue
                    if words[i+1] == 'натуральный':
                        command_parts.append('math.e')
                        command_parts.append(',')
                        continue
                if i > 0:
                    if words[i-1] == 'десятичный':
                        command_parts.append('10')
                        command_parts.append(',')
                        continue
                    if words[i-1] == 'натуральный':
                        command_parts.append('math.e')
                        command_parts.append(',')
                        continue
                
                # проблема в этом месте связана с тем, что если мы введём как первый аргумент сложное выражение, то всё полетит
                # результат: логарифм корень 2 3 -> log(sqrt(2,3))
                buffer = ','

            # в квавдрате, в кубе
            elif words[i] == 'в':
                if words[i+1] == 'квадрате':
                    command_parts.append('**2')
                if words[i+1] == 'кубе':
                    command_parts.append('**3')

    # добавление закрывающихся скобок в конец, если пользователь забыл закрыть
    while command_parts.count('(') > command_parts.count(')'):
        command_parts.append(')')

    if __name__ == '__main__':
        print('command_parts:', command_parts)
    
    # команда, которая должна быть выполнена
    command = ''

    # сцепление всего, что находится между пользовательскими скобками воедино
    while '(' in command_parts and ')' in command_parts:
        j = command_parts.index(')')
        i = len(command_parts) - command_parts[j::-1].index('(') - 1

        piece = ''

        for part in range(i, j+1):
            
            if command_parts[part] in function_recognation:
                while piece.count('(') > piece.count(')') + 1:
                    piece += ')'

            piece += command_parts[part]

            if __name__ == '__main__':
                print('Объединённая часть между скобок:', piece)

        while piece.count('(') > piece.count(')'):
            piece += ')'

        command_parts = command_parts[:i] + [piece] + command_parts[j+1:]

    i = 0

    # sin( cos( ( sin( 2 + 3 + 2) + 1 -> sin(cos((sin(2)+3)))+1
    # pow( pow( 1, 2, 2
    # sin( 2
    # ( + 2 3) * 3
    # (2 / (1 + 1) + 1)
    # ['sin(', 'cos(', '(', ')']
    
    while i < len(command_parts):

        # закрытие скобок от функций sin(cos(...*))* <-
        if command_parts[i] in function_recognation:
            while command.count('(') > command.count(')'):
                command += ')'
        
        # соединение кусков воедино
        command += command_parts[i]

        if __name__ == '__main__':
            print('command in build:', command)
    
        i += 1

    # Добавляет недосатющие закрывающие скобки
    while command.count('(') > command.count(')'):
            command += ')'

    if __name__ == '__main__':
        print('command_parts:', command_parts)
        print('\ncommand:', command)
        print('-'*10, 'debug ends here', sep='\n', end= '\n\n')

    # результат
    try:
        result = round(float(eval(command)), 10)
        if result == int(result):         
            result = int(result)
        return result
    # ------ ТЕБЕ НА РАССМОТРЕНИЕ -----
    except:
        if user_command == '':
            print('Скажите, например: Сколько будет 5+5?')
        else:
            print('Неверная команда')
        return ''

if __name__ == '__main__':
    print('. - для выхода')
    inp = input()
    while inp != '.':
        print(calculator(inp), end='\n\n')
        inp = input()