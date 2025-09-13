@echo off
if not exist "venv\" (
    python -m venv venv
    call venv\Scripts\activate.bat
    .\venv\Scripts\python.exe -m pip install -r requirements.txt
)
call venv\Scripts\activate.bat
.\venv\Scripts\python.exe app.py