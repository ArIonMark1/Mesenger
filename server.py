import select

import time
import socket
import argparse
from descriptors import ControlServerParam
from common.utils import *
from threading import Thread
from metaclass import Meta

from common.variables import USER, ACTION, TIME, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    MAX_CONNECTIONS, SUCCESS, MESSAGE, MESSAGE_TEXT, SENDER, PRESENCE, STATUS
import proj_logs.configs.conf_server
from decorators import decorator

""" 
    Загрузка параметров из коммандной строки, если нет параметров, задаём параметры по умолчанию
    Обрабатываем хост и порт. Пример ввода: python server.py -p 888 -a 192.168.0.10
"""
# logger
server_log = logging.getLogger('app.sever')


# проверка на наличие порта,(число) если порт указан проверка на правильность Использовать try, except
# проверка на наличие хоста,(строка) если указан проверка на валидность Использовать try, except

# запуск сервера, accept, recv, print(message), client.send(message)
# проверить валидность прилетевшего сообщения: все ок - error 200, неверно заполнен - error 400
# =============================================================

# =============================================================

class Server(Socket):
    port = ControlServerParam()
    address = ControlServerParam()

    def __init__(self, ip_address, server_port):

        # Список подключенных клиентов
        self.all_clients = []
        # сообщения от клиентов
        self.messages = []

        self.address = ip_address
        self.port = server_port
        super(Server, self).__init__()

    @decorator
    def check_message(self, message, client):
        sys.stdout.write(f'Прилетело сообщение {message[MESSAGE_TEXT]}\n')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            server_log.info(
                f'{client.getpeername()}: '
                f'name "{message[USER][ACCOUNT_NAME]}"'
                f'status "{message[USER][STATUS]}"')
            response = {RESPONSE: 200, SUCCESS: 'Welcome Guest!'}
            # ==================================
            self.send_message(response, client)
            # ==================================

        elif ACTION in message and message[ACTION] == MESSAGE and \
                TIME in message and MESSAGE_TEXT in message:
            self.messages.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))

        else:

            server_log.critical('Неверный формат сообщения!!')
            response = {RESPONSE: 400, ERROR: 'Not correct sent message!'}
            self.send_message(response, client)

    def set_up(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)
        self.socket.listen(MAX_CONNECTIONS)

        sys.stdout.write(f'Запущен сервер {self.socket}\n')

        while True:
            try:
                client, client_addr = self.socket.accept()
                sys.stdout.write(f'Подтвержденно соединение с клиентом {client_addr}\n')
            except OSError:
                pass
            else:
                # приняли
                server_log.info(f'Start connection with: {client.getpeername()}\n')
                self.all_clients.append(client)
                sys.stdout.write(f'клиетн добавлен в список {self.all_clients}\n')

            recv_message_lst = []
            send_message_lst = []

            try:
                if self.all_clients:
                    recv_message_lst, send_message_lst, err_lst = select.select(self.all_clients, self.all_clients, [],
                                                                                0)
                    sys.stdout.write(f'Получатели: {recv_message_lst}\nОтправители: {send_message_lst}\n')
            except OSError:
                pass

            if recv_message_lst:
                for client_with_message in recv_message_lst:
                    try:
                        # ===========================================================================================
                        self.check_message(self.get_message(client_with_message), client_with_message)
                    except:
                        server_log.info(f'Клиент {client_with_message.getpeername()} '
                                        f'отключился от сервера.')
                        self.all_clients.remove(client_with_message)
            # -------------------
            if self.messages and send_message_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: self.messages[0][0],
                    TIME: time.time(),
                    MESSAGE_TEXT: self.messages[0][1]
                }
                del self.messages[0]

                for client in send_message_lst:
                    try:
                        self.send_message(client, message)
                    except:
                        server_log.info(f'Клиент {client.getpeername()} '
                                        f'отключился от сервера.')
                        self.all_clients.remove(client)


if __name__ == '__main__':
    server_log.info('Server Started!')
    server_log.critical('Running')
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default=DEFAULT_IP_ADDRESS, nargs='?',
                        help=f'server ip-address, default - {DEFAULT_IP_ADDRESS}')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int, nargs='?',
                        help=f'server port, default - {DEFAULT_PORT}')
    args = parser.parse_args()

    address = args.address

    # try:
    port = args.port

    server = Server(address, port)
    server.set_up()
