import webbrowser
import functions

def browser():
    sites = {"https://vk.com":["vk","вк","вконтакте"],'https://www.youtube.com/':['youtube', 'ютуб'],'https://ru.wikipedia.org': ["вики", "wiki"],'https://ru.aliexpress.com':['али', 'ali', 'aliexpress', 'алиэспресс'],'http://google.com':['гугл','google'],'https://www.amazon.com':['амазон', 'amazon'],'https://www.apple.com/ru':['apple','эпл'], 'https://telete.in/gurupython':['пайтонгуру', 'pythonguru'],"https://github.com/DanVoid45/course-project":['курсач',"курсовая","проект",'курса'], "https://www.youtube.com/watch?v=dQw4w9WgXcQ":["рик"]}
    site = functions.voice.split()[-1]
    for k, v in sites.items():
        for i in v:
            if i not in site.lower():
                open_tab = None
            else:
                functions.speak("Выполняю")
                open_tab = webbrowser.open_new_tab(k)

        if open_tab is not None:
            break