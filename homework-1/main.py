"""Скрипт для заполнения данными таблиц в БД Postgres."""

import psycopg2
import csv
import os

from utils.svn_utils import *

TABLES = [{'file_name': os.getcwd() + 'north_data\\customers_data.csv',
           'table': 'customers',
           'values': 'customer_id, company_name, contact_name',
           'type_values': 'int, str, str'
           },
          {'file_name': os.getcwd() + 'north_data\\orders_data.csv',
           'table': 'orders',
           'values': 'order_id, customer_id, employee_id, order_date, ship_city',
           'type_values': 'int, str, int, date, str'
           },
          {'file_name': os.getcwd() + 'north_data\\employees_data.csv',
           'table': 'employees',
           'values': 'employee_id, first_name, last_name, title, birth_date, notes',
           'type_values': 'int, str, str, str, date, str'
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

    pass


def main():

    while True:
        user_input = user_menu()
        if user_input == '0':
            print('\n\t\t ---= Пока =---')
            break
        elif user_input == '1':
            pass

        elif user_input == '2':
            print('{0:^30}'.format('Грузим данные с CSV в базу данных'))
            for table in TABLES:
                print(
                    f"из файла \033[32m{table['file_name']}\033[39m в таблицу "
                    f"\033[33m{table['table'].upper()}\033[39m")
                load_from_csv_in_table(table)


if __name__ == '__main__':
    main()

