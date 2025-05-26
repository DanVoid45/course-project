import pyttsx3
import speech_recognition as sr
import os
import win32com.client
from fuzzywuzzy import fuzz
import datetime
import time
import asyncio
from vtubestudio import vts
import BrowserHandler
import calculator
import mon2
import envelope
import translator
import weather

opts = {
    "alias": ("айрис", "арис", "рис", "аис", "iris", "airis", "ириска", "алиса"),
    "tbr": (
        "скажи",
        "расскажи",
        "покажи",
        "сколько",
        "произнеси",
        "как",
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
        "money": ("подбрось", "брось", "кинь"),
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
        "weather": ("прогноз", "погода", "abc"),
        "nothing": ("Не распознано"),
    },
}

startTime = 0

# Асинхронное озвучивание с анимацией
async def async_speak(what: str):
    """Асинхронное произнесение текста с синхронизацией анимации"""
    try:
        await vts.trigger_hotkey("LipSync_Start")
        
        # Озвучка через SAPI
        engine = win32com.client.Dispatch("Sapi.SpVoice")
        voices = engine.GetVoices()
        target_voice = next(
            v for v in voices 
            if "VE_Russian_Milena_22kHz" in v.GetDescription()
        )
        engine.Voice = target_voice
        engine.Rate = 2
        engine.Volume = 100
        engine.Speak(what)
        
        await vts.trigger_hotkey("LipSync_Stop")
        
    except Exception as e:
        print(f"Ошибка анимации: {e}")
        try: 
            await vts.trigger_hotkey("LipSync_Stop")
        except: 
            pass

# Синхронная обертка для обратной совместимости
def speak(what: str):
    """Синхронный интерфейс для озвучки"""
    print(what)
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(async_speak(what))
        else:
            loop.run_until_complete(async_speak(what))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_speak(what))
        loop.close()

def callback(recognizer, audio):
    """Обработка аудиовхода"""
    global voice
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"Распознано: {voice}")

        if any(alias in voice for alias in opts["alias"]):
            cmd = voice
            for x in opts["alias"] + opts["tbr"]:
                cmd = cmd.replace(x, "").strip()
            
            recognized = recognize_cmd(cmd)
            execute_cmd(recognized["cmd"])

    except sr.UnknownValueError:
        print("Голос не распознан!")
    except sr.RequestError:
        print("Ошибка соединения с сервисом распознавания!")

def listen():
    """Запуск фонового прослушивания"""
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        r.adjust_for_ambient_noise(source)
    
    stop_listening = r.listen_in_background(
        sr.Microphone(device_index=1), 
        callback
    )
    return stop_listening

def recognize_cmd(cmd: str) -> dict:
    """Распознавание команды с использованием fuzzy-логики"""
    best_match = {"cmd": "nothing", "percent": 0}
    for command, patterns in opts["cmds"].items():
        for pattern in patterns:
            similarity = fuzz.ratio(cmd, pattern)
            if similarity > best_match["percent"]:
                best_match = {"cmd": command, "percent": similarity}
    return best_match if best_match["percent"] >= 40 else {"cmd": "nothing", "percent": 0}

def execute_cmd(command: str):
    """Выполнение распознанной команды"""
    global startTime
    try:
        if command == "ctime":
            now = datetime.datetime.now()
            speak(f"Сейчас {now.hour}:{now.minute:02}")
            
        elif command == "shutdown":
            os.system("shutdown /s /t 30")
            speak("Компьютер выключится через 30 секунд")
            
        elif command == "calc":
            calculator.calculator()
            
        elif command == "money":
            mon2.toss_coin()
            
        elif command == "conv":
            envelope.convertation()
            
        elif command == "translator":
            translator.translate()
            
        elif command == "internet":
            BrowserHandler.browser()
            
        elif command == "startStopwatch":
            startTime = time.time()
            speak("Секундомер запущен")
            
        elif command == "stopStopwatch":
            if startTime:
                elapsed = time.time() - startTime
                speak(f"Прошло: {elapsed:.2f} секунд")
                startTime = 0
            else:
                speak("Секундомер не активен")
                
        elif command == "weather":
            weather.weather()
            
        else:
            speak("Команда не распознана")
            
    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        speak("Произошла ошибка при выполнении команды")