import argparse
import sys
import threading
import time
from common.utils import *
from common.variables import *
import proj_logs.configs.conf_client
from decorators import decorator
from common.utils import *

# логгер
client_log = logging.getLogger('app.client')

# Класс Клиент
# class Client(Socket):
#     def __init__(self, ip_address, server_port, client_name):
#         super(Client, self).__init__()
#
#         self.address = ip_address
#         self.port = server_port
#         self.name = client_name
#
#     def message_from_server(self):
#         """ Получение сообщения от клиентов """
#         while True:
#             try:
#                 # =====================================
#                 message = self.get_message(self.socket)
#                 # =====================================
#                 if ACTION in message and message[ACTION] == MESSAGE and \
#                         SENDER in message and MESSAGE_TEXT in message:
#
#                     print(f'Получено сообщение от пользователя '
#                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
#                     client_log.info(f'Получено сообщение от пользователя '
#                                     f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
#                 else:
#                     client_log.error(f'Получено некорректное сообщение с сервера: {message}')
#                     print(message)
#
#             except ConnectionRefusedError:
#                 client_log.critical(f'{self.name}: потеряная связь с сервером')
#                 break
#
#     def create_message(self):
#         """ Отправка сообщения для других клиентов """
#         while True:
#             message = input('Ваше сообщение: ')
#
#             message_out = {
#                 ACTION: MESSAGE,
#                 TIME: time.ctime(),
#                 USER: {ACCOUNT_NAME: self.name},
#                 MESSAGE_TEXT: message,
#             }
#             client_log.info('Сформированый словать сообщения для клиентов.')
#             try:
#                 self.send_message(self.socket, message_out)
#                 client_log.info(f'{message_out} сообщение было отправленно на сервер.')
#
#             except ConnectionRefusedError:
#                 client_log.critical('Потеряно соединение с сервером!')
#                 sys.exit(1)
#
#     @decorator
#     def create_presence(self):
#         '''
#         Функция генерирует запрос о присутствии клиента
#         :param account_name:
#         :return:
#         '''
#         out_message = {
#             ACTION: PRESENCE,
#             TIME: time.ctime(),
#             USER: {ACCOUNT_NAME: self.name, STATUS: 'online'},
#             TYPE: STATUS,
#         }
#         client_log.info(f'Сформированое сообщение для сервера {out_message}')
#         return out_message
#
#     # ============================================================================
#
#     @decorator
#     def process_ans(self, message):
#         if message:
#             if message[RESPONSE] == 200:
#                 client_log.info(f'Успешный ответ сервера {message[RESPONSE]}')
#                 return f'{message[RESPONSE]}, {message[SUCCESS]}'
#             client_log.error(f'Ошибка соединения с сервером!!{message[RESPONSE]}')
#             return f'{message[RESPONSE]}, {message[ERROR]}'
#
#     def set_up(self):
#         try:
#             # Подключение к серверу и отправка сообщения о присутствии
#             self.socket.connect((self.address, self.port))
#             # отправка серверу запрос на подключение
#             self.send_message(self.socket, self.create_presence())
#             client_log.info('Сообщение серверу отправленно')
#
#             # прием подтверждения от сервера
#             answer = self.get_message(self.socket)
#             checked_response = self.process_ans(answer)
#             client_log.info(f'Сообщение от сервера: {checked_response}')
#             print(checked_response)
#
#         except ConnectionRefusedError:
#             client_log.critical(
#                 f'Не удалось подключиться к серверу, '
#                 f'конечный компьютер отверг запрос на подключение.')
#             sys.exit(1)
#             # =====================================================
#             # Если соединение с сервером установлено корректно,
#             # начинаем обмен с ним, согласно требуемому режиму.
#             # основной цикл прогрммы:
#             # receiver = threading.Thread(target=self.message_from_server)
#         receiver = threading.Thread(target=self.message_from_server)
#         receiver.daemon = True
#         receiver.start()
#         receiver.join()
#
#         sender = threading.Thread(target=self.create_message)
#         sender.daemon = True
#         sender.start()
#         sender.join()

import socket
import sys
import threading
import time
from common.variables import *
from common.utils import *
from descriptors import ControlServerParam


# логгер
# client_log = logging.getLogger('app.client')

class Client(Socket):
    host = ControlServerParam()
    port = ControlServerParam()

    def __init__(self, address, port, name):
        self.host = address
        self.port = port
        self.name = f'{name}_{self.port}'
        # self.name = f'arion_{self.port}'
        super(Client, self).__init__()

    # ========================================================================
    def confirm_connection(self):
        """ Генерируем сообщение для сервера """
        confirm_message = {
            ACTION: PRESENCE,
            TIME: time.ctime(),
            USER: {ACCOUNT_NAME: self.name, STATUS: 'online'}
        }
        sys.stdout.write(f'Сообщение подтверждения {confirm_message} отправленно на сервер.\n')
        # client_log.info(f'Сформированое сообщение для сервера {out_message}')
        return confirm_message

    # ========================================================================
    @staticmethod
    def control_response(message):
        if message:
            if message[RESPONSE] == 200:
                # client_log.critical('Client connected to server')
                # sys.stdout.write(f'Успешный ответ от сервера {message[RESPONSE]}')
                return f'{message[RESPONSE]}, {message[SUCCESS]}'
            # sys.stdout.write(f'Ошибка соединения с сервером!! {message[RESPONSE]}')
            return f'{message[RESPONSE]}{message[ERROR]}'

    # ========================================================================

    def create_message(self):
        while True:
            mess = input('>>> ')

            message_out = {
                ACTION: MESSAGE,
                TIME: time.ctime(),
                USER: {ACCOUNT_NAME: self.name},
                MESSAGE_TEXT: mess,
            }
            try:
                self.send_message(self.socket, message_out)
            except ConnectionRefusedError:
                sys.stderr.write('Потеряно соединение с сервером!\n')
                sys.exit(1)

    def receive_message(self):
        while True:
            try:
                response = self.get_message(self.socket)
                if ACTION in response and response[ACTION] == MESSAGE and \
                        MESSAGE_TEXT in response:
                    sys.stdout.write(f'{response[USER[ACCOUNT_NAME]]} {response[MESSAGE_TEXT]}\n')
                sys.stdout.write(f'Получено некорректное сообщение с сервера: {response}')

            except ConnectionRefusedError:
                sys.stderr.write('Потеряно соединение с сервером!\n')
                sys.exit(1)

    def set_up(self):
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            # =================================================
            # Отправка сообщения для подтверждения подключения
            self.send_message(self.socket, self.confirm_connection())
            # =================================================
            # Проверка успешности подключения к серверу, ловим ответ от сервера
            response = self.get_message(self.socket)
            control_response = self.control_response(response)
            sys.stdout.write(f'Сообщение от сервера: {control_response}.\n')

        except ConnectionRefusedError:
            # client_log.critical(
            #     f'Не удалось подключиться к серверу, '
            #     f'конечный компьютер отверг запрос на подключение.')
            sys.stderr.write('Не удалось подключиться к серверу!\n')
            sys.exit(1)

        sending = threading.Thread(target=self.create_message)
        sending.daemon = True
        sending.start()
        sending.join()

        receiver = threading.Thread(target=self.receive_message)
        receiver.daemon = True
        receiver.start()
        receiver.join()


# if __name__ == '__main__':
#     # client_log.info('Client Started!')
#     client = Client('127.0.0.1', 8888)
#     client.set_up()
#


if __name__ == '__main__':
    client_log.info('Client Started!')
    client_log.critical('Client connected to server')

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', default='Guest', nargs='?')
    parser.add_argument('-a', '--address', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, type=int, nargs='?')

    client_name = parser.parse_args().name
    args = parser.parse_args()

    address = args.address
    try:
        port = args.port
        if 65535 < port < 1024:
            raise IndexError
    except IndexError:
        client_log.critical('Неправильно указан порт: может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    client = Client(address, port, client_name)
    client.set_up()
