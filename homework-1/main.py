"""Скрипт для заполнения данными таблиц в БД Postgres."""

import psycopg2
import csv
import os

from utils.svn_utils import *

TABLES = [{'file_name': os.getcwd() + '\\north_data\\customers_data.csv',
           'table': 'customers',
           # 'values': 'customer_id, company_name, contact_name',
           # 'type_values': 'int, str, str'
           },
          {'file_name': os.getcwd() + '\\north_data\\orders_data.csv',
           'table': 'orders',
           # 'values': 'order_id, customer_id, employee_id, order_date, ship_city',
           # 'type_values': 'int, str, int, date, str'
           },
          {'file_name': os.getcwd() + '\\north_data\\employees_data.csv',
           'table': 'employees',
           # 'values': 'employee_id, first_name, last_name, title, birth_date, notes',
           # 'type_values': 'int, str, str, str, date, str'
           }
          ]

DB_HOST = 'localhost'
DB_BASE = 'north'
DB_USER = 'postgres'
DB_PASSWORD = '12345'


def user_menu() -> str:
    print('\n -----= Меню =----- ')
    print(f'\t\033[32m[1]\033[39m - Очистить таблицы в базе данных')
    print('\t\033[32m[2]\033[39m - считать данные из файлов в таблицы')
    print()
    print('\t\033[31m[0]\033[39m - выход из программы')

    menu_item: str = '012'.strip()

    user_input: str = check_line_entry(
        f'Выберите пункт меню ({", ".join(menu_item)})',
        ''.join(menu_item),
        f'разрешен ввод только {", ".join(menu_item)}')
    return user_input

def load_from_csv_in_table(table):

    with open(table['file_name'], 'r', encoding='UTF-8') as file:
        rows = csv.reader(file)
        count_row_csv = 0
        values_file = ''
        for row in rows:
            if count_row_csv == 0:
                values_file = row
            else:
                # print(f'Оригинал - {row}')
                # print(f'Отрезка - {",".join(row)}')
                # try:
                #     with psycopg2.connect(host=DB_HOST, database=DB_BASE,
                #                           user=DB_USER,
                #                           password=DB_PASSWORD) as conn_sql:
                #         # print(conn_sql.status)
                #         with conn_sql.cursor() as cur_sql:
                #             # print(cur_sql.statusmessage)
                #             cur_sql.execute(f'INSERT INTO {table["table"]} '
                #                             f'VALUES ({row[1:-2]});')
                #
                #
                #         conn_sql.commit()
                #
                # finally:
                #     conn_sql.close()

            count_row_csv += 1

        with psycopg2.connect(host=DB_HOST, database=DB_BASE,
                              user=DB_USER, password=DB_PASSWORD) as conn_sql:
            # print(conn_sql.status)
            with conn_sql.cursor() as cur_sql:
                # print(cur_sql.statusmessage)
               cur_sql.execute(f'SELECT COUNT(*) FROM {table["table"]}')
               print(f'Добавлено в таблицу \033[34m{table["table"]}\033[39m '
                     f'\033[34m{cur_sql.fetchone()[0]}\033[39m записей '
                     f' (база данных \033[33m{DB_BASE.upper()}\033[39m)')
        conn_sql.close()
    pass


def clear_database(my_db_tables):
    try:
        with psycopg2.connect(host=DB_HOST, database=DB_BASE,
                              user=DB_USER, password=DB_PASSWORD) as conn_sql:
            # print(conn_sql.status)
            with conn_sql.cursor() as cur_sql:
                # print(cur_sql.statusmessage)
                # print(my_db_tables)
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

    while True:
        user_input = user_menu()
        if user_input == '0':
            print('\n\t\t ---= Пока =---')
            break
        elif user_input == '1':
            my_db_tables = ', '.join(table['table'].upper() for table in TABLES)

            # print('{0:^50}'.format(f'Очищаем таблицы '
            #                        f'\033[33m{my_db_tables}\033[39m '
            #                        f'в базе данных \033[33m{DB_BASE.upper()}\033[39m'))
            clear_database(my_db_tables)

        elif user_input == '2':
            print('{0:^50}'.format('Грузим данные с CSV в базу данных'))
            for table in TABLES:
                print(
                    f"из файла \033[32m{table['file_name']}\033[39m в таблицу "
                    f"\033[33m{table['table'].upper()}\033[39m")
                load_from_csv_in_table(table)


if __name__ == '__main__':
    main()

