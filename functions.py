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

def callback(recognizer, audio, messages_list=None):
    global voice
    try:
        # Распознаем голос с использованием Google Speech API
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()

        # Пытаемся извлечь команду из распознанного текста
        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()

            for x in opts["tbr"]:
                cmd = cmd.replace(x, "").strip()

            # Сохраняем распознанную команду в messages_list, если он передан
            if messages_list is not None:
                messages_list.insert(0, voice)  # Добавляем в начало списка

            # Распознаем команду и выполняем ее
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd["cmd"])

    except sr.UnknownValueError:
        if messages_list is not None:
            messages_list.insert(0, "Голос не распознан!")

    except sr.RequestError as e:
        if messages_list is not None:
            messages_list.insert(0, "Неизвестная ошибка, проверьте интернет!")


def listen(messages_list=None):
    with m as source:
        r.adjust_for_ambient_noise(source)
    top_listening = r.listen_in_background(m, lambda audio: 
                                           callback(r, audio, messages_list))
    while True:
        time.sleep(0.1)


def recognize_cmd(cmd):
    #пропискать, если слишком маленькие проценты то выводить "не распознано"
    RC = {"cmd": "", "percent": 0}
    for c, v in opts["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = vrt
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
    else:
        print("Команда не распознана!")
