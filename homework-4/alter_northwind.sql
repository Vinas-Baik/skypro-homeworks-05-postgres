-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products
-- (цена должна быть больше 0)
ALTER TABLE products
ADD CONSTRAINT chk_products_unit_price CHECK (unit_price >=0);

-- 2. Добавить ограничение, что поле discontinued таблицы products может
-- содержать только значения 0 или 1
ALTER TABLE products
ADD CONSTRAINT chk_products_discontinued CHECK (discontinued IN (0, 1));



-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)


-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key. Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.
