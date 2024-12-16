import functions
from pyowm import OWM
from pyowm.owm import OWM

def weather():
    owm = OWM('612241020da2c549277a75336b0afe80')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('London,GB')
    w = observation.weather
    w.detailed_status         # 'clouds'
    w.wind()                  # {'speed': 4.6, 'deg': 330}
    w.humidity                # 87
    w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    w.rain                    # {}
    w.heat_index              # None
    w.clouds                  # 75
    functions.speak("Погода", w.detailed_status)