import random
import functions

def toss_coin():
    result = random.choice(['Орёл', 'Решка'])
    if result == "Орёл":
        functions.speak("Выпал орёл")
    else: functions.speak("Выпала решка")
    return
