import os, subprocess
subprocess.run(["powershell", "-noexit", '.\\venv\\Scripts\\Activate.ps1'])
os.system('cls')

import functions
import time
import datetime

now = datetime.datetime.now()

if now.hour >= 6 and now.hour < 12:
    functions.speak("Доброе утро!")
elif now.hour >= 12 and now.hour < 16:
    functions.speak("Добрый день!")

elif now.hour >= 16 and now.hour < 23:
    functions.speak("Добрый вечер!")
else:
    functions.speak("Доброй ночи!")

functions.listen()