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
import hello
import webbrowser
import mon2
import random
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
        "stopStopwatch": ("останови секундомер", "выключи секундомер", "останови", "отключи секундомер"),
        "calc": (
            "прибавить",
            "умножить",
            "разделить",
            "степень",
            "вычесть",
            "поделить",
            "сложить",
            "степени",
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
            "выключи компьютер",
            "отключи ноут",
        ),
        "conv": ("валюта", "конвертер", "доллар", "руб", "евро"),
        "internet": ("открой", "вк", "гугл", "сайт", "вконтакте", "ютуб"),
        "translator": ("переводчик", "translate", "переведи"),
        "weather": ("прогноз","погода","abc"),
        "hello": ("привет", "здравствуйте", "категорически"),
        "stop": ("хватит","стоп","остановись"),
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

def callback_for_text_input(request, callback_ui=None):
    request = request.lower()

    for x in opts["alias"]:
        request = request.replace(x, "").strip()
    for x in opts["tbr"]:
        request = request.replace(x, "").strip()
    
    recognized = recognize_cmd(request)
    response = execute_cmd(request, recognized["cmd"])

    return response


def callback(recognizer, audio, callback_ui=None):
    try:
        global voice
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        
        if callback_ui:
                callback_ui(voice, is_voice=True)     # показываем распознанный текст пользователя

        if voice.startswith(opts["alias"]):
            cmd_text = voice

            for x in opts["alias"]:
                cmd_text = cmd_text.replace(x, "").strip()


            for x in opts["tbr"]:
                cmd_text = cmd_text.replace(x, "").strip()

            recognized = recognize_cmd(cmd_text) 

            response = execute_cmd(cmd_text, recognized["cmd"])



    except sr.UnknownValueError:
        if callback_ui:
            callback_ui("Голос не распознан!", is_voice=True)

    except sr.RequestError:
        if callback_ui:
            callback_ui("Ошибка соединения!", is_voice=True)

stopper = None


def listen(callback_ui=None):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    def background_callback(recognizer, audio):
        callback(recognizer, audio, callback_ui=callback_ui)
        
    stop_listening = recognizer.listen_in_background(mic, background_callback)
    return stop_listening


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
    elif cmd == "hello":
        return hello.hie()
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
    elif cmd == "weather":
        return weather.weather()
    #elif cmd == "stop":

    elif cmd == 'nothing':
        return "Не распознано"
    else:
        print("Команда не распознана!")