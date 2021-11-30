import sys
import inspect
import logging
import traceback
from pathlib import Path
import proj_logs.configs.conf_client
import proj_logs.configs.conf_server


def decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.debug(f'Function started {func.__name__} with params {args} {kwargs}'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return res

    return wrapper


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('app.sever')
else:
    LOGGER = logging.getLogger('app.client')
