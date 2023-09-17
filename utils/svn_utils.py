import os


def text_error(text=''):
    """
    Формирование сообщения об ошибку с выделением красным цветом
    вызов функции без параметра выдает просто сообщение ОШИБКА
    """
    return '\033[31m' + '>> ОШИБКА - ' + text + ' << ' + '\033[39m'
    # return text

def full_path_name_file(name_file):
    """
    формируем полный путь до файла
    :param name_file: имя файла с указанием подпапки
    :return: полный пусть в UNIX системы
    """
    return os.getcwd() + '\\' + name_file
    # return os.path.join(*name_file.replace('\\','/').spl


def check_line_entry(text='', allowed_сhars='', error_string=''):
    """
    Функция проверяет введенную пользователем строку на пустой ввод и разрешенные символы
    :param text: строка для пользователя
    :param allowed_сhars: разрешенные символы, если список пустой, то разрешены любые символы
    :param error_string: строка с ошибкой, если строка содержит запрещенные символы
    :return: возвращаем введенную строку от пользователя
    """
    allowed_сhars = allowed_сhars.strip()
    while True:
        input_string = input(f'{text}: ').strip().lower()
        if input_string == '':
            print(text_error('Пустой ввод'))
        elif allowed_сhars == '':
            break
        else:
            is_chars_allowed = True
            for i_s in input_string:
                if i_s not in allowed_сhars:
                    is_chars_allowed = False
                    break
            if is_chars_allowed:
                break
            else:
                print(text_error(error_string))

    return input_string
