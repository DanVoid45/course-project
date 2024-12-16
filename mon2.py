import pyttsx3
import speech_recognition as sr
import random
import functions
# Инициализация голосового движка
speak_engine = pyttsx3.init()


def toss_coin():
    """Функция для подбрасывания монетки."""
    result = random.choice(['Орёл', 'Решка'])
    return result


def listen():
    """Функция для прослушивания команд."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            command = r.recognize_google(audio, language="ru-RU").lower()
            print(f"Команда распознана: {command}")
            if "монетку" or "монету" in command:
                result = toss_coin()
                print("Выпало:", result)
                functions.speak(f"Выпало: {result}")

        except sr.UnknownValueError:
            print("Голос не распознан!")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")

if __name__ == "__main__":
    listen()
