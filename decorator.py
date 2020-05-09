import datetime
from contextlib import contextmanager
from datetime import datetime
import os.path

param_for_decorator = 'logg'

def logger_decor(param):
    def my_decorator(old_function):
        output_file = 'log.txt'
        path = param + '/' + output_file

        def new_foonction(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as file:

                file.write(f'{datetime.now()}\n')
                print(datetime.now())
                file.write(f'Имя функции: {old_function.__name__}\n')
                print(f'Имя функции: {old_function.__name__}')
                file.write(f'Аргументы: {args}\n')
                print(f'Аргументы: {args}')
                file.write(f'Результат: {old_function(*args, **kwargs)}\n\n')
                file.write(f'Путь к логам: {os.path.abspath(path)}\n\n')

            return old_function(*args, **kwargs)

        return new_foonction

    return my_decorator


