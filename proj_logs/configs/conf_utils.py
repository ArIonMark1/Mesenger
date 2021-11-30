import logging
import os
import sys
from datetime import datetime
from pathlib import Path

time_name = 'utils_log_{:%H-%M-%S}.log'.format(datetime.now())

root_path = Path(__file__).parents[1]
utils_log_path = os.path.join(root_path, f'logs_doc/{time_name}')

formatter = logging.Formatter('%(levelname)-10s %(process)-8d %(asctime)-26s %(message)s')

file_handler = logging.FileHandler(utils_log_path, encoding='utf-8')
stream_handler = logging.StreamHandler(sys.stdout)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

file_handler.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('app.utils')
logger.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

if __name__ == '__main__':
    logger.info('Оповещение в utils файле.')
    logger.debug('Отладка в utils файле.')
    logger.error('Ошибка в utils файле!!')
    logger.warning('Предупреждение в utils файле!')
