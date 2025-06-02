import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index=1) # проверить микрофон для корректной работы

def callback(recognizer, audio):
    print("[callback] Вызвана функция callback")
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"[callback] Распознано: {voice}")
    except Exception as e:
        print(f"[callback] Ошибка распознавания: {e}")

stop_listening = r.listen_in_background(mic, callback)

import time
print("Начинаем слушать в фоне...")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_listening()
    print("Остановлено")
