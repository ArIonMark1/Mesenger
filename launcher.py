# лаунчер

import subprocess

PROCESS = []

while True:

    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python3 server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for i in range(3):
            PROCESS.append(subprocess.Popen('python3 client.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
