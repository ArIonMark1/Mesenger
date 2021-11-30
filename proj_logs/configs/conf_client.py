import os
import sys
import logging
from pathlib import Path
from datetime import datetime

time_name = 'client_log_{:%H-%M-%S}.log'.format(datetime.now())

root_path = Path(__file__).parents[1]
client_log_path = os.path.join(root_path, f'logs_doc/{time_name}')

# =========================================
# формат сообщения formater
formatter = logging.Formatter('%(levelname)-10s %(process)-8d %(asctime)-26s %(message)s')

# файловый обработчик handler
file_handler1 = logging.FileHandler(client_log_path, encoding='utf-8')
stream_handler = logging.StreamHandler(sys.stderr)

# в хендлер передаем формат сообщения
file_handler1.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# индивидуальный уровень для каждого вывода
file_handler1.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.CRITICAL)

# ======================================
# логгер
clt_logger = logging.getLogger('app.client')
#  уровень данных (для лога) передаем в логгер через комманду
clt_logger.setLevel(logging.DEBUG)
# логеру передаем через комманду "добавить обработчик" файловый обработчик( обработчик подключим к регистратору )
clt_logger.addHandler(file_handler1)
clt_logger.addHandler(stream_handler)

# определяем текст сообщений уровня(без сообщений нету результатов, будет пустой лог)
if __name__ == '__main__':
    clt_logger.critical('Критическая ошибка!!')
    clt_logger.info('Информация.')
    clt_logger.debug('Дебагинг.')
    clt_logger.error('Простая ошибка.')
    clt_logger.warning('Предупреждение!')
