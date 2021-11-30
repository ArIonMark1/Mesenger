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

    def __init__(self, address, port):
        self.host = address
        self.port = port
        self.name = f'arion_{self.port}'
        super(Client, self).__init__()

    # ========================================================================
    def confirm_connection(self):
        """ Генерируем сообщение для сервера """
        confirm_message = {
            ACTION: PRESENCE,
            'time': time.ctime(),
            'user': {'account_name': self.name, STATUS: 'online'}
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


if __name__ == '__main__':
    # client_log.info('Client Started!')
    client = Client('127.0.0.1', 8888)
    client.set_up()
