import json

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
        params = config(filename="database.ini", section="postgresql")
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

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
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

    with open(script_file) as f:
         cur.execute(f.read())



def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    cur.execute('CREATE TABLE suppliers('
                ');')


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    pass


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    pass


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    pass


if __name__ == '__main__':
    main()
