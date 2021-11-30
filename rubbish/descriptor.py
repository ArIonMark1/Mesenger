import dis
import select
import socket
import sys
import ipaddress


class ControlServerParam:

    def __get__(self, instance, owner):
        return instance.__dict__[self.my_attr]

    def __set__(self, instance, value):
        # server_attributes = {}
        # server_attributes[self.my_attr] = value
        # for k, v in server_attributes.items():

        if self.my_attr == 'port':
            try:
                if value < 1024 or value > 65535:
                    raise IndexError
            except IndexError:
                sys.stderr.write(
                    'Неправильно указан порт: может быть указано только число в диапазоне от 1024 до 65535.')
                sys.exit(0)

        instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner, my_attr):  # вместо __init__
        self.my_attr = my_attr


class MyAge:
    # age = NonNegative()

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'Hello, my name is {self.name} and my age is {self.age}'


# print(MyAge('Arion', 23))


# ======================================================================
class Server:
    host = ControlServerParam()
    port = ControlServerParam()

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

        self.connected_users = []
        self.messages = []

    def main(self):
        sock = self.socket
        # ===============================
        # try:
        #     if self.port < 1024 or self.port > 65535:
        #         raise IndexError
        # except IndexError:
        #     sys.stderr.write(
        #         'Неправильно указан порт: может быть указано только число в диапазоне от 1024 до 65535.')
        #     sys.exit(0)
        # ===============================

        sock.bind((self.host, self.port))
        sys.stdout.write('Server is Binded!')
        sock.settimeout(1)
        sock.listen(5)

        while True:
            try:
                user, address = sock.accept()
                sys.stdout.write('Listening users...')

            except OSError:
                pass
            else:
                self.connected_users.append(user)

            user_send = []
            user_receive = []
            try:
                if self.connected_users:
                    user_send, user_erceive, error = select.select(self.connected_users, self.connected_users, [], 0)
            except OSError:
                pass

            for user_sender in user_send:
                message = sock.recv(1024)
                self.messages.append(message)
                print(message)

            for user_listener in user_receive:
                sock.send(self.messages.pop(0))


if __name__ == '__main__':
    serv = Server('127.0.0.1', 888)
    serv.main()
