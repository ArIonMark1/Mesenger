"""Данный вариант будет работать  Ubuntu v.20"""

import os
import time
import subprocess
from pathlib import Path
ROOT_DIR = Path(__file__).parents[0]

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        p = f'python3 "{ROOT_DIR}/server.py"'
        PROCESS.append(subprocess.Popen(['gnome-terminal', p]))
        print(p)
        time.sleep(0.1)
        for i in range(2):
            p = f'python3 "{ROOT_DIR}/client.py"'
            # p = f'python3 "{ROOT_DIR}/client.py" -m send -u userS{i}'
            PROCESS.append(subprocess.Popen(['gnome-terminal', p]))
            print(p)
            time.sleep(0.1)
        for i in range(2):
            p = f'python3 "{ROOT_DIR}/client.py"'
            # p = f'python3 "{ROOT_DIR}/client.py" -m listen -u userL{i}'
            PROCESS.append(subprocess.Popen(['gnome-terminal', p]))
            print(p)
            time.sleep(0.1)
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()

