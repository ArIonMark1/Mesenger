import select
import socket
from ipaddress import ip_address
import sys


class ControlServerParam:

    def __set__(self, instance, value):

        if self.my_attr == 'port':
            try:
                if value < 1024 or value > 65535:
                    raise IndexError
            except IndexError:
                sys.stderr.write(
                    'Неправильно указан порт: может быть указано только число в диапазоне от 1024 до 65535.\n')
                sys.exit(0)

        if self.my_attr == 'address':
            try:
                if not ip_address(value):
                    raise ValueError
            except ValueError:
                sys.stderr.write('Некорректно заданый адрес!\n')
                sys.exit(0)

        instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner, my_attr):  # вместо __init__
        self.my_attr = my_attr
