import functions
def calculator():
    try:
        list_of_nums = functions.voice.split()
        num_1,num_2 = int((list_of_nums[-3]).strip()), int((list_of_nums[-1]).strip())
        opers = [list_of_nums[0].strip(),list_of_nums[-2].strip()]
        for i in opers:
            if 'дел' in i or 'множ' in i or 'лож' in i or 'приба' in i or 'выч' in i or i == 'x' or i == '/' or i =='+' or i == '-' or i == '*':
                oper = i
                break
            else:
                oper = opers[1]
        if oper == "+" or 'слож' in oper:
            ans = num_1 + num_2
        elif oper == "-" or 'выче' in oper:
            ans = num_1 - num_2
        elif oper == "х" or 'множ' in oper:
            ans = num_1 * num_2
        elif oper == "/" or 'дел' in oper:
            if num_2 != 0:
                ans = num_1 / num_2
            else:
                return ("Делить на ноль невозможно")
        elif "степен" in oper:
            ans = num_1 ** num_2
        return ("{0} {1} {2} = {3}".format(list_of_nums[-3], list_of_nums[-2], list_of_nums[-1], ans))
    except:
        return ("Скажите, например: Сколько будет 5+5?")