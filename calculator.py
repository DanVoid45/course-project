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
    'sqrt': 'sqrt',
    'квадрат': 'sqr',
    'sqr': 'sqr',
    'синус': 'sin',
    'sin': 'sin',
    'cos': 'cos',
    'косинус': 'cos',
    'тангенс': 'tg',
    'котангенс': 'ctg',
}

dificult_function_recognition = {
    'степень': 'pow',
    'логарифм': 'log',
    'log': 'log',
    'pow': 'pow'
}

# [sin(, [...], )]
# [sin(, [cos(, [1, +, 2], )], )]
# sin(, ..., ) 
def calculator(user_command: str = '') -> str:
    print(user_command)
    print("я вызвался!!")
    # дебаг режим
    if __name__ == '__main__':
        print('\ndebug', '-'*10, sep='\n')

    # поиск "слов" при неявном вводе
    words: list = []

    # нужен для добавления запятой в сложных функциях (так же хранит номера функций, которые дожны не быть учтены дважды)
    commas: list = []

    # вызов функции с параметром (например, ввод пользователем команды через интерфейс)
    if user_command != '':
        try:
            # попытка вычислить значение выражения в лоб
            if eval(user_command.replace(' ', '')) != '':
                return eval(user_command.replace(' ', ''))
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

            number = str(int(words[i]))

            # sin cos log 2 4
            # log sqrt 2 4
            # log sqrt ( 2 + 1 ) sin 4
            if commas.count(',') > 0:
                # log( or pow( already here
                ignored = []
                for i in commas:
                    if i != ',':
                        ignored.append(int(commas[i]))
                
                for i in range(len(command_parts)-1, -1, -1):
                    if command_parts[i] in ('log(', 'pow(') and not (i in ignored):
                        if i + 1 == len(command_parts):
                            break
                        if len(command_parts) > i + 2:
                            if command_parts[i+1] == '(' and ')' in command_parts[i:]:
                                command_parts.insert(len(command_parts) - command_parts[::-1].index(')'), commas.pop())
                                commas.insert(0, str(i))
                                break
                        if command_parts[i+1] != '(':
                            try:
                                int(command_parts[-1])
                                command_parts.append(commas.pop())
                                commas.insert(str(i))
                            except: ()
                        break

            # добавление числа в command_parts
            command_parts.append(number)
            print(command_parts)

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
                print ("aboba")
                print(command_parts)
            
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
                
                commas.append(',')

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
        print(command_parts)
        
        j = command_parts.index(')')
        i = j - command_parts[j::-1].index('(')

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


    # для недопуска повторов при rfind
    #          pow log
    ignored = [[], []]
    def d_f_find(s: str, part: str, k: int) -> int:
        if s.rfind(part) in ignored[k]:
            return d_f_find(s[:s.rfind(part)] + s[s.rfind(part) + len(part):], part, k)
        else:
            return s.rfind(part)
        
    
    i = 0

    # sin( cos( ( sin( 2 + 3 + 2) + 1 -> sin(cos((sin(2)+3)))+1
    # pow( pow( 1, 2, 2
    # sin( 2
    # ( + 2 3) * 3
    # (2 / (1 + 1) + 1)
    # ['sin(', 'cos(', '(', ')']

    while i < len(command_parts):
        # ,
        if command_parts[i] == ',':
            index = [-1, -1]
            if command.find('pow(') != -1:
                index[0] = d_f_find(command, 'pow(', 0)
            if command.find('log(') != -1:
                index[1] = d_f_find(command, 'log(', 1)
            if index[0] > index[1]:
                ignored[0].append(index[0])
            if index[0] < index[1]:
                ignored[1].append(index[1])
            print(index, ignored)
            if max(index) != -1:
                while command[max(index)+4:].count('(') != command[max(index)+1:].count(')'):
                    command += ')'

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
        return str(result)
    # ------ ТЕБЕ НА РАССМОТРЕНИЕ -----
    except:
        if user_command == '':
            return('Скажите, например: Сколько будет 5+5?')
        else:
            return('Неверная команда' + ' '.join(commands))


def temp(string: str):
    return string

if __name__ == '__main__':
    print('. - для выхода')
    inp = input()
    while inp != '.':
        temp(calculator(inp))
        inp = input()