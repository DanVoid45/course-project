import webbrowser
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
            break

