# Как установить виртуальное окружение
## Python 3.12

- Создать виртуальное окружение
    ```python -m venv ./venv/```

- Активировать venv
    ```venv\Scripts\Activate.ps1```

- Загрузить все библиотеки
    ```pip install -r requirements.txt```

- Создать список установленных библиотек
    ```pip freeze > requirements.txt```