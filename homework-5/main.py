import json
import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'
    conn = None
    # читаем параметры для подключения из ini файла
    try:
        # params = config(filename="database.ini", section="postgresql")
        params = config()
    except Exception as error:
        print(error)
        return

    # Если БД существует, то удаляем

    try:
        remove_database(params, db_name)
        print(f"старая БД {db_name} успешно удалена")
    except Exception as error:
        # print(f"БД {db_name} нет ")
        pass

    # Создаем новую БД
    try:
        create_database(params, db_name)
        print(f"БД {db_name} успешно создана")

        params.update({'dbname': db_name})
    except Exception as error:
        print(error)
        return

    try:
        with psycopg2.connect(**params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")
                conn.commit()

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")
                conn.commit()

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")
                conn.commit()

                add_foreign_keys(cur)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()


def create_database(params, db_name):
    """Создает новую базу данных."""
    try:
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        sql_create_database = f'CREATE DATABASE {db_name}'
        cur.execute(sql_create_database)

        sql_create_database = f"ALTER ROLE {params['user']} " \
                              f"SET client_encoding TO 'utf8'"
        cur.execute(sql_create_database)

        # print(params)
    except (Exception, Error) as error:
        # print("Ошибка при работе с PostgreSQL: ", error)
        raise Exception(f"Ошибка при работе с PostgreSQL: {error}")
    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()
            # print("Соединение с PostgreSQL закрыто")

def remove_database(params, db_name):
    """Удаляем базу данных."""
    try:
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        sql_create_database = f'DROP DATABASE {db_name} WITH (FORCE)'
        cur.execute(sql_create_database)
        # print(cur.statusmessage)
    except (Exception, Error) as error:
        # print("Ошибка при работе с PostgreSQL: ", error)
        raise Exception(f"Ошибка при работе с PostgreSQL: {error}")
    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()
            # print("Соединение с PostgreSQL закрыто")

def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""

    with open(os.getcwd() + '\\' + script_file, 'r') as f:
         cur.execute(f.read())



def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    cur.execute('CREATE TABLE suppliers(supplier_id smallint PRIMARY KEY NOT NULL,'
                                       'company_name varchar(50) NOT NULL,'
                                       'contact varchar(50) NOT NULL,'
                                       'address varchar(100) NOT NULL,'
                                       'phone varchar(15),'
                                       'fax varchar(15),'
                                       'homepage varchar(150) NOT NULL);')

    # Создаем таблицу supplier_product для хранения ссылок на продукты поставщиков.
    cur.execute('CREATE TABLE supplier_product(supplier_id smallint,'
                'product_id smallint,'
                'sup_prod_id serial PRIMARY KEY NOT NULL);')

def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    """
    Загрузка JSON словаря с файла
    name_file:  имя файла c JSON словарем
    :return: список JSON
    """
    json_list = None  # словарь
    # формируем полный путь до файла
    name_file = os.getcwd() + '\\' + json_file

    try:
        if os.path.exists(name_file):
            with open(name_file, 'r', encoding='UTF-8') as file:
                json_list = json.load(file)
        else:                                       # если файла нет, то ошибка
            # print(text_error('Файл ' + name_file + ' не существует, проверьте наличие файла по указанному пути'))
            json_list = None

    except json.JSONDecodeError:                    # если ошибка чтения JSON словаря, то выводим ошибку
        # print(text_error('Файл ' + name_file + ' не является JSON файлом'))
        json_list = None

    return json_list


# def replace_appostrof(st: str) -> str:
#     return st.replace('\'', '\'\'')


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    for t_key, t_sup in enumerate(suppliers):
        # print(t_sup)
        #     'CREATE TABLE suppliers(
        #     supplier_id smallint PRIMARY KEY NOT NULL,'
        #     company_name varchar(50) NOT NULL,'
        #     contact varchar(50) NOT NULL,'
        #     address varchar(50) NOT NULL,'
        #     phone varchar(15),'
        #     fax varchar(15),'
        #     homepage varchar(150) NOT NULL);')
        supp_id = t_key + 1
        # cur.execute(sql_command)
        cur.execute('INSERT INTO suppliers(supplier_id, company_name, ' \
                    'contact, address, phone, fax, homepage) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s);',
                    (supp_id, t_sup["company_name"], t_sup["contact"],
                     t_sup["address"], t_sup["phone"], t_sup["fax"],
                     t_sup["homepage"]))
        # print(t_sup['products'])
        for t_key, t_prod in enumerate(t_sup['products']):
            t_sup['products'][t_key] = t_prod.replace('\'', '\'\'')

        sql_command = ("SELECT product_id FROM products "
                       "WHERE product_name IN %s") %t_sup['products']

        sql_command = sql_command.replace('[', '(').replace(']', ')').replace('"', "'")
        # print(sql_command)
        cur.execute(sql_command)
        prod_list = cur.fetchall()
        # print(prod_list)
        for prod_id in prod_list:
            # print(f'{supp_id} | {prod_id[0]}')
            cur.execute('INSERT INTO supplier_product(supplier_id, product_id) '
                        'VALUES (%s, %s)', (supp_id, prod_id[0]))

        # print('--------------------')


def add_foreign_keys(cur) -> None:
    """
    Добавляет foreign key со ссылкой на supplier_id в таблицу products.
    """

    cur.execute('ALTER TABLE ONLY supplier_product '
                'ADD CONSTRAINT fk_supplier_supprod FOREIGN KEY (supplier_id) '
                'REFERENCES suppliers;')
    cur.execute('ALTER TABLE ONLY supplier_product '
                'ADD CONSTRAINT fk_products_supprod FOREIGN KEY (product_id) '
                'REFERENCES products;')




if __name__ == '__main__':
    main()
