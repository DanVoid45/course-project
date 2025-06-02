import pyttsx3
import speech_recognition as sr
import os
import win32com.client
from fuzzywuzzy import fuzz
import datetime
import win32com.client as wincl
import BrowserHandler
from calculator import calculator
import time
import envelope
import translator
import webbrowser
import mon2
import weather
import re

opts = {
    "alias": ("айрис", "арис", "рис", "аис", "iris", "airis", "ириска","алиса"),
    "tbr": (
        "скажи",
        "расскажи",
        "покажи",
        "сколько",
        "произнеси",
        "как",
        "сколько",
        "поставь",
        "переведи",
        "засеки",
        "запусти",
        "сколько будет",
    ),
    "cmds": {
        "ctime": (
            "текущее время",
            "сейчас времени",
            "который час",
            "время",
            "какое сейчас время",
        ),
        "startStopwatch": ("запусти секундомер", "включи секундомер", "засеки время"),
        "stopStopwatch": ("останови секундомер", "выключи секундомер", "останови"),
        "calc": (
            "прибавить",
            "умножить",
            "разделить",
            "степень",
            "вычесть",
            "поделить",
            "сложить",
            "логарифм",
            "sin",
            "cos",
            "tg",
            "ctg",
            "pow",
            "log",
            "х",
            "+",
            "-",
            "/",
        ),
        "play_music": 
        ("включи музыку",
        "воспроизведи",
        "поставь песню", 
        "включи трек"),

        "money": (
            "подбрось",
            "брось",
            "кинь",
        ),
        "shutdown": (
            "выключи",
            "выключить",
            "отключение",
            "отключи",
            "выключи компьютер",
        ),
        "conv": ("валюта", "конвертер", "доллар", "руб", "евро"),
        "internet": ("открой", "вк", "гугл", "сайт", "вконтакте", "ютуб"),
        "translator": ("переводчик", "translate"),
        "weather": ("прогноз","погода","abc"),
        "nothing": ("Не распознано"),
    },
}
startTime = 0
speak_engine = pyttsx3.init()
voices = speak_engine.getProperty("voices")
speak_engine.setProperty("voice", voices[1].id)
r = sr.Recognizer()
m = sr.Microphone(device_index=1)
voice = "str"


def speak(what):
    print(what)
    speak = win32com.client.Dispatch("Sapi.SpVoice")
    voices = speak.GetVoices()
    voices_names = [voice.GetDescription() for voice in voices]

    namevoice = 'VE_Russian_Milena_22kHz'
    namevoiceID = voices_names.index(namevoice) if namevoice in voices_names else 0
    speak.Voice = voices[namevoiceID]

    speak.Rate = 2
    speak.Volume = 100
    speak.Speak(what)

def callback(recognizer, audio, callback_ui=None):
    try:
        global voice
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()

        print("Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()

            for x in opts["tbr"]:
                cmd = cmd.replace(x, "").strip()
            voice = cmd
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd["cmd"])

            # Очистили — теперь можно показывать пользователю и обрабатывать
            if callback_ui:
                callback_ui(cmd, is_voice=True)

            recognized = recognize_cmd(cmd)
            response = execute_cmd(cmd, recognized["cmd"])

            if response:
                speak(response)
                if callback_ui:
                    callback_ui(response, is_voice=True)

    except sr.UnknownValueError:
        if callback_ui:
            callback_ui("Голос не распознан!", is_voice=True)

    except sr.RequestError:
        if callback_ui:
            callback_ui("Ошибка соединения!", is_voice=True)





stopper = None

def listen(callback_ui=None):
    global stopper
    mic = sr.Microphone(device_index=1)
    with mic as source:
        r.adjust_for_ambient_noise(source)

    def wrapper(recognizer, audio):
        try:
            print(">>> Вызван wrapper")
            callback(recognizer, audio, callback_ui)
        except Exception as e:
            print("[Ошибка в wrapper]:", e)


    print(">>> Стартуем прослушивание в фоне")
    stopper = r.listen_in_background(mic, wrapper)


def recognize_cmd(cmd):
    for key, values in opts["cmds"].items():
        for phrase in values:
            if phrase in cmd:
                return {"cmd": key, "percent": 100}
    return {"cmd": "nothing", "percent": 0}



def execute_cmd(request, cmd):
    global startTime
    if cmd == "ctime":                                                                             
        now = datetime.datetime.now()
        return  ("Сейчас {0}:{1}".format(str(now.hour), str(now.minute)))
    elif cmd == "shutdown":                                                                        
        open_tab = webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        os.system("shutdown -s -t 90")
        return("Выключаю...")
    elif cmd == "calc":                                                                            
        return calculator(request)
    elif cmd == "play_music":
        return BrowserHandler.browser(request)
    elif cmd == "money":                                                                           
        return mon2.toss_coin()
    elif cmd == "conv":
        return envelope.convertation(request)
    elif cmd == "translator":                                                                 
        return translator.translate(request)
    elif cmd == "internet":                                                                        #нужно все проверить
        return (BrowserHandler.browser(request))
    elif cmd == "startStopwatch":                                                                   
        startTime = time.time()
        return("Секундомер запущен")
    elif cmd == "stopStopwatch":
        if startTime != 0:
            Time = time.time() - startTime
            startTime = 0
            return(
                f"{round(Time, 2)} секунд"
            )
        else:
            return("Секундомер не включен")
    elif cmd == "weather":                                                                          #нужно проверить
        return weather.weather()
    elif cmd == 'nothing':
        return "Не распознано"
    else:
        print("Команда не распознана!")
