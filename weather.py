import functions
from pyowm import OWM
from pyowm.owm import OWM

def weather():
    owm = OWM('612241020da2c549277a75336b0afe80')
    mgr = owm.weather_manager()
    
    weather_status_translation = {
    "clear sky": "ясное небо",
    "few clouds": "малооблачно",
    "scattered clouds": "рассеянные облака",
    "broken clouds": "облачно с прояснениями",
    "overcast clouds": "пасмурно",
    "shower rain": "ливень",
    "rain": "дождь",
    "thunderstorm": "гроза",
    "snow": "снег",
    "mist": "туман",
    }
    
    location = 'Vologda, RU'
    # Получение текущей погоды
    observation = mgr.weather_at_place(location)
    weather = observation.weather
    # Извлечение данных
    temperature = weather.temperature('celsius')  # Температура в градусах Цельсия
    status = weather.detailed_status              # Состояние погоды (например, "облачно")
    wind = weather.wind()                         # Скорость и направление ветра
    
    translated_status = weather_status_translation.get(status, status)
    
    # Формирование строки прогноза
    forecast = (
        f"Погода в {location}:\n"
        f"- Температура: {temperature['temp']}°\n"
        f"- Ощущается как: {temperature['feels_like']}°\n"
        f"- Состояние: {translated_status.capitalize()}\n"
        f"- Ветер: {wind['speed']} метров в секунду"
    )
    return(forecast)
        