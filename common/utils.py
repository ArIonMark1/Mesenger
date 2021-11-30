import json
import logging
from socket import socket
import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parents[1]
import proj_logs.configs.conf_utils
from socket import socket, AF_INET, SOCK_STREAM
import common.variables as variables

# logger
logger = logging.getLogger('app.utils')
logger.setLevel(logging.DEBUG)


class Socket:
    def __init__(self, host=variables.DEFAULT_IP_ADDRESS, port=variables.DEFAULT_PORT):
        # =======================================
        self.socket = None
        # self.socket = socket(AF_INET, SOCK_STREAM)

        self.host = host
        self.port = port

    @staticmethod
    def get_message(sock=None):  # возвр. словарь
        try:
            encode_response = sock.recv(variables.MAX_DATA_LENGTH)
            # encode_response = sock.recv(MAX_DATA_LENGTH)  # прилетает сообщение указанного размера
            if isinstance(encode_response, bytes):  # является ли значение байтами
                js_response = encode_response.decode(variables.ENCODING)
                response = json.loads(js_response)  # считывает json-строку и возвращает python-обьект

                if isinstance(response, dict):  # является ли ответ словарем
                    logger.info(f'Возврат словаря {response}')
                    return response  # возвращаем данные-словарь

                raise ValueError  # иначе ошибка
            raise ValueError  # ошибка
        except ValueError:
            err = '400: Ошибка данных сообщения!!!!'
            logger.critical(err)
            sock.send(err.encode('utf-8'))

    @staticmethod
    def send_message(sock, message):
        """ Кодировка и отправка сообщения """
        logger.info(f'Кодирование сообщения {message}')
        js_message = json.dumps(message)  # возвращает в переменную json-строку
        logger.info('Возвращаем json-строку')
        encode_message = js_message.encode(variables.ENCODING)  # энкодируем строку в байты
        logger.info(f'энкодированая строка: {encode_message}')
        if sock.send(encode_message):  # отправляем сообщение
            logger.info('Сообщение успешно отправленно')
        else:
            logger.critical('Ошибка отправки сообщения!!!')

    def set_up(self):
        raise NotImplementedError()


if __name__ == '__main__':
    print(f'Current file is: {__name__}')
    logger.info(f'Start logger in file: {__name__}')
