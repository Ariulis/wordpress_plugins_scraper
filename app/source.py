from logging.config import listen
from time import perf_counter
from functools import wraps
from csv import DictWriter, DictReader, reader

from colorama import init
from loguru import logger

logger.add('log/debug.log', level='DEBUG',
           format='{time} {level} {message}', rotation='10 KB', compression='zip')

init()

URL = 'https://wordpress.org/plugins/browse/blocks/page/{}'
ORDER = ['title', 'link', 'rating', 'src']


def time_counter():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start = perf_counter()
            result = f(*args, **kwargs)
            print(f'Execution time: {round(perf_counter() - start, 2)}s')
            return result
        return decorated_function
    return decorator


def write_csv(data):
    with open('plugins.csv', 'a') as f:
        writer = DictWriter(f, fieldnames=ORDER)
        writer.writerows(data)


def read_csv():
    with open('plugins.csv', encoding='utf-8') as f:
        reader = DictReader(f, fieldnames=ORDER)

        return list(reader)
