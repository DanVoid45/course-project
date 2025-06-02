"""import webbrowser
import functions

def browser():
    sites = {
        "https://vk.com": ["vk", "вк", "вконтакте"],
        'https://www.youtube.com/': ['youtube', 'ютуб'],
        'https://ru.wikipedia.org': ["вики", "wiki"],
        'https://ru.aliexpress.com': ['али', 'ali', 'aliexpress', 'алиэспресс'],
        'http://google.com': ['гугл', 'google'],
        'https://www.amazon.com': ['амазон', 'amazon'],
        'https://www.apple.com/ru': ['apple', 'эпл'],
        'https://telete.in/gurupython': ['пайтонгуру', 'pythonguru'],
        "https://github.com/DanVoid45/course-project": ['курсач', "курсовая", "проект", 'курса'],
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": ["рик"]
    }
    
    command = functions.voice  # Получаем строку с голосовой командой
    site = command.split()  # Разбиваем строку на слова
    
    # Проверяем, есть ли запрос на поиск в Google
    if "найди" in site or "поиск" in site:
        query = " ".join(site[2:])  # Предполагаем, что запрос идет после команды "найди"
        search_url = f"https://www.google.com/search?q={query}"
        functions.speak("Выполняю поиск в Google")
        webbrowser.open_new_tab(search_url)
        return

    open_tab = None
    for k, v in sites.items():
        for i in v:
            # Приводим текущую команду к нижнему регистру для сравнения
            if i not in command.lower():  
                open_tab = None
            else:
                functions.speak("Выполняю")
                open_tab = webbrowser.open_new_tab(k)
                break
        if open_tab is not None:
            break"""
            
import webbrowser

def browser(command):
    sites = {
        "https://vk.com": ["vk", "вк", "вконтакте"],
        'https://www.youtube.com/': ['youtube', 'ютуб'],
        'https://ru.wikipedia.org': ["вики", "wiki"],
        'https://ru.aliexpress.com': ['али', 'ali', 'aliexpress', 'алиэспресс'],
        'http://google.com': ['гугл', 'google'],
        'https://www.amazon.com': ['амазон', 'amazon'],
        'https://www.apple.com/ru': ['apple', 'эпл'],
        'https://telete.in/gurupython': ['пайтонгуру', 'pythonguru'],
        "https://github.com/DanVoid45/course-project": ['курсач', "курсовая", "проект", 'курса'],
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ": ["рик"]
    }

    command_lower = command.lower()

    # Распознавание команды на воспроизведение музыки
    # Распознавание команды на воспроизведение музыки
    music_triggers = [
        "включи музыку", "включи трек", "воспроизведи музыку",
        "поставь песню", "воспроизведи", "включи песню", "запусти музыку"
    ]

    for trigger in music_triggers:
        if trigger in command_lower:
            track_name = command_lower.replace(trigger, "").strip()
            if not track_name:
                track_name = "музыка"
            search_url = f"https://music.yandex.ru/search?text={track_name}"
            webbrowser.open_new_tab(search_url)
            return f"Ищу и включаю: {track_name}"


    # Поиск в Google
    if "сайт" in command_lower or "страницу" in command_lower:
        words = command.split()
        query = " ".join(words[2:])  # или адаптировать точнее под ключевые слова
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open_new_tab(search_url)
        return "Выполняю поиск в Google"

    # Открытие сайта по ключевым словам
    for url, keywords in sites.items():
        if any(keyword in command_lower for keyword in keywords):
            webbrowser.open_new_tab(url)
            return "Открываю сайт"

    return "Не удалось распознать команду для браузера"
