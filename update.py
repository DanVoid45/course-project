import subprocess, os
subprocess.run(["powershell", 'pip freeze > .\\venv\\requirements.txt'])
os.system('cls')