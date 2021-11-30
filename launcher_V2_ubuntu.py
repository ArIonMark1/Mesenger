import subprocess
import shlex
import time
import os
import signal


PROCESS = []

while True:

    ANSWER = input('Выберите действие: q - выход, s - запустить сервер и клиенты, x - закрыть все окна: ')

    if ANSWER == 'q':
        break
    elif ANSWER == 's':
        PROCESS.append(subprocess.Popen('gnome-terminal -- python3 server.py', shell=True))
        time.sleep(0.5)
        PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -n Test_1', shell=True))
        PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -n Test_2', shell=True))
        PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -n Test_3', shell=True))
    elif ANSWER == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
            VICTIM.terminate()
