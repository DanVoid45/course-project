import random

def toss_coin():
    result = random.choice(['Орёл', 'Решка'])
    if result == "Орёл":
        return("Выпал орёл")
    else: return("Выпала решка")
