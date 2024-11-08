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

opts = {
    "alias": ("айрис", "арис", "рис", "аис", "iris", "airis", "ириска", "кизару", "kizaru"),
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
        "stupid1": (
            "расскажи анекдот",
            "рассмеши меня",
            "ты знаешь анекдоты",
            "шутка",
            "прикол",
        ),
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
        "shutdown": (
            "выключи",
            "выключить",
            "отключение",
            "отключи",
            "выключи компьютер",
        ),
        "conv": ("валюта", "конвертер", "доллар", "руб", "евро"),
        "internet": ("открой", "вк", "гугл", "сайт", "вконтакте", "ютуб"),
        "translator": ("переводчик", "переведи", "translate"),
        "deals": ("дела", "делишки", "как сам", "как дела"),
    },
}
startTime = 0
speak_engine = pyttsx3.init()
voices = speak_engine.getProperty("voices")
speak_engine.setProperty("voice", voices[1].id)
r = sr.Recognizer()
m = sr.Microphone(device_index=1)
voice = "str"



def recogniseVoice(voice: str):
    """Распознаем комманду из строки голоса
        Например    voice = "<Имя> <Команда> <Параметры....>"\n
        Или         voice = "<Распознанный голос> <Имя> <Команда> <Параметры....>"

    Args:
        voice (str): строка голоса
    """
    
    splited_voice = voice.split(' ')
    recognised_alias = [alias for alias in opts["alias"] if alias in splited_voice]
    prepared_voice = splited_voice
    
    recoginesed_command = ''
    
    alias_ids = []

    if recognised_alias:
        for alias in recognised_alias:
            alias_ids += [index for index, word in enumerate(splited_voice) if word == alias]

        prepared_voice = prepared_voice[alias_ids[-1]:][1:] # Убираем все лишнее, берем последнее обращение без имени
        
    for command in opts['cmds']:
        command_words = opts['cmds'][command]
        
        if prepared_voice:
            if prepared_voice[0] in command_words: # Смотри есть ли глагол в списке комманд, если да, возвращаем
                recoginesed_command = command
                prepared_voice = ' '.join(prepared_voice[1:])
                break
        
    if recoginesed_command:
        return  [recoginesed_command, prepared_voice]
    else:
        return None
    
    

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


def callback(recognizer, audio):

    try:
        global voice
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()

        print("Распознано: " + voice)
        
        recognised = recogniseVoice(voice)
        print(recognised)
        
        if recognised:
            command, text = recognised
            execute_cmd(command, text)


        # if voice.startswith(opts["alias"]):
        #     cmd = voice

        #     for x in opts["alias"]:
        #         cmd = cmd.replace(x, "").strip()

        #     for x in opts["tbr"]:
        #         cmd = cmd.replace(x, "").strip()
        #     voice = cmd
        #     # распознаем и выполняем команду
        #     cmd = recognize_cmd(cmd)
        #     execute_cmd(cmd["cmd"])

    except sr.UnknownValueError:
        print("Голос не распознан!")
    except sr.RequestError as e:
        print("Неизвестная ошибка, проверьте интернет!")


def listen():
    with m as source:
        r.adjust_for_ambient_noise(source)
    stop_listening = r.listen_in_background(m, callback)
    while True:
        time.sleep(0.1)


def recognize_cmd(cmd):
    RC = {"cmd": "", "percent": 0}
    for c, v in opts["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC["percent"]:
                RC["cmd"] = c
                RC["percent"] = vrt
    return RC


def execute_cmd(cmd, text=''):
    global startTime
    if cmd == "ctime":
        now = datetime.datetime.now()
        speak("Сейчас {0}:{1}".format(str(now.hour), str(now.minute)))
    elif cmd == "shutdown":
        open_tab = webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        os.system("shutdown -s -t 90")
        speak("Выключаю...")
    elif cmd == "calc":
        calculator.calculator()
    elif cmd == "conv":
        envelope.convertation()
    elif cmd == "translator":
        print("пытаемся залесть в переводчик")
        translator.translate(text)
    # elif cmd == 'stupid1':
    #    anekdot.fun()
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
    elif cmd == "deals":
        speak("Пока отлично.")
    else:
        print("Команда не распознана!")
