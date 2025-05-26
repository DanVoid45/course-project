import asyncio
import datetime
import signal
from vtubestudio import vts
import functions

running = True

def signal_handler(sig, frame):
    global running
    print("\nЗавершение работы...")
    running = False

async def main():
    # Подключение к VTube Studio
    try:
        await vts.connect()
        print("Успешное подключение к VTube Studio")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return

    # Определение времени суток
    now = datetime.datetime.now()
    greeting = ""
    
    if 6 <= now.hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= now.hour < 16:
        greeting = "Добрый день!"
    elif 16 <= now.hour < 23:
        greeting = "Добрый вечер!"
    else:
        greeting = "Доброй ночи!"

    # Произнесение приветствия
    functions.speak(greeting)
    
    # Запуск фонового прослушивания
    functions.listen()
    
    # Основной цикл
    while running:
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nРабота ассистента завершена")