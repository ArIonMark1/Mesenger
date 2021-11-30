import os
import sys
import logging
from pathlib import Path
from datetime import datetime


time = datetime.now()
NAME = f'server_log_{time.hour}-{time.minute}-{time.second}.log'

root_path = Path(__file__).parents[1]
server_log_path = os.path.join(root_path, f'logs_doc/{NAME}')

# формат сообщения formatter
server_formatter = logging.Formatter('%(levelname)-10s %(process)-8d %(asctime)s %(message)s')

# файловый обработчик handler
handler_file = logging.FileHandler(server_log_path, encoding='utf-8')
handler_stream = logging.StreamHandler(sys.stderr)

# в хендлер передаем формат сообщения
handler_file.setFormatter(server_formatter)
handler_stream.setFormatter(server_formatter)

# уровень хендлера
handler_file.setLevel(logging.DEBUG)
handler_stream.setLevel(logging.CRITICAL)

# логгер
server_log = logging.getLogger('app.server')
# передаем хендлеры в лог
server_log.addHandler(handler_file)
server_log.addHandler(handler_stream)
# уровень лога
server_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # определяем текст сообщений уровня(без сообщений нету результатов, будет пустой лог)
    server_log.info('Информация.')
    server_log.debug('Дебагинг.')
    server_log.warning('Предупреждение!')
    server_log.critical('Critical Error!!')
    server_log.error('Some error.')
