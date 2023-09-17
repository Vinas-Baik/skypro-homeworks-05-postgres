"""Скрипт для заполнения данными таблиц в БД Postgres."""

import psycopg2
import csv

from utils.svn_utils import *

# Описание таблиц
# file_name - имя файла
# table - имя таблицы
# values - список колонок, столбцов, атрибутов  таблицы
TABLES = [{'file_name': os.getcwd() + '\\north_data\\customers_data.csv',
           'table': 'customers',
           'values': 'customer_id, company_name, contact_name',
           # 'type_values': 'int, str, str'
           },
          {'file_name': os.getcwd() + '\\north_data\\employees_data.csv',
           'table': 'employees',
           'values': 'employee_id, first_name, last_name, title, birth_date, notes',
           # 'type_values': 'int, str, str, str, date, str'
           },
          {'file_name': os.getcwd() + '\\north_data\\orders_data.csv',
           'table': 'orders',
           'values': 'order_id, customer_id, employee_id, order_date, ship_city',
           # 'type_values': 'int, str, int, date, str'
           }
          ]

# параметры для подключения к базе данных
DB_HOST = 'localhost'
DB_BASE = 'north'
DB_USER = 'postgres'
DB_PASSWORD = '12345'


def user_menu() -> str:
    """
    меню выводимое для пользователя с запросом от пользователя выбора пункта меню
    """
    print('\n -----= Меню =----- ')
    print('\t\033[32m[1]\033[39m - Очистить таблицы в базе данных')
    print('\t\033[32m[2]\033[39m - считать данные из файлов в таблицы')
    print('\t\033[32m[3]\033[39m - посмотреть количество записей в таблицах')
    print()
    print('\t\033[31m[0]\033[39m - выход из программы')

    menu_item: str = '0123'.strip()

    user_input: str = check_line_entry(
        f'Выберите пункт меню ({", ".join(menu_item)})',
        ''.join(menu_item),
        f'разрешен ввод только {", ".join(menu_item)}')
    return user_input

def count_items_table(table_name: str) -> int:
    """
    подсчет количества записей в таблице базы данных
    """
    try:
        with psycopg2.connect(host=DB_HOST, database=DB_BASE,
                              user=DB_USER,
                              password=DB_PASSWORD) as conn_sql:
            # print(conn_sql.status)
            with conn_sql.cursor() as cur_sql:
                cur_sql.execute(f'SELECT COUNT(*) FROM {table_name}')
                count_items = int(cur_sql.fetchone()[0])

    finally:
        conn_sql.close()

    return count_items


def load_from_csv_in_table(table):
    """
    грузим данные с CSV файла в таблицу
    """

    try:
        with psycopg2.connect(host=DB_HOST, database=DB_BASE,
                              user=DB_USER,
                              password=DB_PASSWORD) as conn_sql:
            # print(conn_sql.status)
            with conn_sql.cursor() as cur_sql:
                with open(table['file_name'], 'r', encoding='UTF-8') as file:
                    rows = csv.reader(file)
                    count_row_csv = 0
                    for row in rows:
                        # пропускаем 1 строчку из CSV файла
                        if count_row_csv != 0:
                            # print(f'Оригинал - {row}')
                            tuple_row = []
                            # преобразуем символ ' в символ `, так есть проблемы с работой команды INSERT
                            for t_value in row:
                                tuple_row.append(t_value.replace('\'', '`'))

                            cur_sql.execute(f'INSERT INTO {table["table"]}({table["values"]}) '
                                            f'VALUES {tuple(tuple_row)};')

                        count_row_csv += 1

                conn_sql.commit()

                # запрашиваем количество записей в таблице

                cur_sql.execute(f'SELECT COUNT(*) FROM {table["table"]}')
                print(f'Добавлено в таблицу \033[34m{table["table"]}\033[39m '
                      f' (база данных \033[33m{DB_BASE.upper()}\033[39m):'
                      f'\033[34m{cur_sql.fetchone()[0]}\033[39m записей ')

    finally:
        conn_sql.close()


def clear_database(my_db_tables):
    """
    очищаем таблицу от записей
    my_db_tables - передаем список таблиц через запятую
    """
    try:
        with psycopg2.connect(host=DB_HOST, database=DB_BASE,
                              user=DB_USER, password=DB_PASSWORD) as conn_sql:
            # print(conn_sql.status)
            with conn_sql.cursor() as cur_sql:
                for table in my_db_tables.split(', '):
                    cur_sql.execute(f'SELECT COUNT(*) FROM {table}')

                    print(f'Очищаем таблицу \033[34m{table}\033[39m '
                          f'(количество записей = \033[34m{cur_sql.fetchone()[0]}\033[39m)'
                          f' в базе данных \033[33m{DB_BASE.upper()}\033[39m')

                    cur_sql.execute(f'DELETE FROM {table}')

            conn_sql.commit()

    finally:
        conn_sql.close()


def main():
    """
    главная часть программы
    """
    while True:
        user_input = user_menu()
        if user_input == '0':
            # выходим из программы
            print('\n\t\t ---= Пока =---')
            break
        elif user_input == '1':
            # пересобираем список таблиц для очистки наоборот
            my_db_tables = ''
            for table in TABLES:
                my_db_tables = table['table'].upper() + ', ' + my_db_tables

            clear_database(my_db_tables[:-2])

        elif user_input == '2':
            # Грузим данные из файлов CSV
            print('{0:^50}'.format('Грузим данные с CSV в базу данных'))
            for table in TABLES:
                count_items = count_items_table(table['table'])
                # проверяем количество записей в таблице
                if count_items != 0:
                    print(f'\033[31mТаблица {table["table"].upper()} содержит '
                          f'{count_items} записей \033[39m')
                    print(f'Таблицу {table["table"]} нужно очистить '
                          f'перед добавлением записей из файла')
                else:
                    # работаем только с пустой таблицей
                    print(f"из файла \033[32m{table['file_name']}\033[39m в таблицу "
                          f"\033[33m{table['table'].upper()}\033[39m")
                    load_from_csv_in_table(table)

        elif user_input == '3':
            # вывод количества записей в таблицах
            for table in TABLES:
                count_items = count_items_table(table['table'])
                print(f'Таблица \033[32m{table["table"].upper()}\033[39m содержит '
                      f'\033[33m{count_items} записей \033[39m')

if __name__ == '__main__':
    main()

