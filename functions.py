import pyttsx3
import speech_recognition as sr
import os
import win32com.client
from fuzzywuzzy import fuzz
import datetime
import win32com.client as wincl
import BrowserHandler
import calculator
import time
import envelope
import translator
import webbrowser
import mon2
import weather

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
            "х",
            "+",
            "-",
            "/",
        ),
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
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()

        if any(alias in voice for alias in opts["alias"]):
            cmd = voice
            for x in opts["alias"]:
                cmd = cmd.replace(x, "")
            for x in opts["tbr"]:
                cmd = cmd.replace(x, "")
            cmd = cmd.strip()

            if callback_ui:
                callback_ui(voice, is_voice=True)

    except sr.UnknownValueError:
        if callback_ui:
            callback_ui("Голос не распознан!", is_voice=True)

    except sr.RequestError:
        if callback_ui:
            callback_ui("Ошибка соединения!", is_voice=True)



def listen(callback_ui=None):
    mic = sr.Microphone(device_index=1)
    with mic as source:
        r.adjust_for_ambient_noise(source)

    def wrapper(recognizer, audio):
        callback(recognizer, audio, callback_ui)

    r.listen_in_background(mic, wrapper)





def recognize_cmd(cmd):
    RC = {"cmd": "", "percent": 0}
    for c, v in opts["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = vrt
    if RC["percent"] < 20:
        RC ['cmd'] = "nothing"
    return RC


def execute_cmd(cmd):
    global startTime
    if cmd == "ctime":                                                                              #работает
        now = datetime.datetime.now()
        return  ("Сейчас {0}:{1}".format(str(now.hour), str(now.minute)))
    elif cmd == "shutdown":                                                                         #работает
        open_tab = webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        os.system("shutdown -s -t 90")
        return("Выключаю...")
    elif cmd == "calc":
        return calculator.calculator()
    elif cmd == "money":                                                                            #работает
        return mon2.toss_coin()
    elif cmd == "conv":
        envelope.convertation()
    elif cmd == "translator":
        print("пытаемся залесть в переводчик")
        translator.translate()
    elif cmd == "internet":
        BrowserHandler.browser()
    elif cmd == "startStopwatch":
        speak("Секундомер запущен")
        startTime = time.time()
    elif cmd == "stopStopwatch":
        if startTime != 0:
            Time = time.time() - startTime
            speak(
                f"Прошло {round(Time // 3600)} часов {round(Time // 60)} минут {round(Time % 60, 2)} секунд"
            )
            startTime = 0
        else:
            speak("Секундомер не включен")
    elif cmd == "weather":
        return weather.weather()
    elif cmd == 'nothing':
        return "Не распознано"
    else:
        print("Команда не распознана!")
