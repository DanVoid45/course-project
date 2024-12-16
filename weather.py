import functions
from pyowm import OWM
from pyowm.owm import OWM

def weather():
    owm = OWM('612241020da2c549277a75336b0afe80')
    mgr = owm.weather_manager()
    location = 'Vologda, RU'
    # Получение текущей погоды
    observation = mgr.weather_at_place(location)
    weather = observation.weather
    # Извлечение данных
    temperature = weather.temperature('celsius')  # Температура в градусах Цельсия
    status = weather.detailed_status              # Состояние погоды (например, "облачно")
    wind = weather.wind()                         # Скорость и направление ветра
    # Формирование строки прогноза
    forecast = (
        f"Погода в {location}:\n"
        f"- Температура: {temperature['temp']}°C\n"
        f"- Ощущается как: {temperature['feels_like']}°C\n"
        f"- Максимальная: {temperature['temp_max']}°C, минимальная: {temperature['temp_min']}°C\n"
        f"- Состояние: {status.capitalize()}\n"
        f"- Ветер: {wind['speed']} м/с"
    )
    command = functions.voice
    site = command.split()
    if "прогноз" in site:
        functions.speak(forecast)
        return