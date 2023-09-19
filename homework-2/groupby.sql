-- Напишите запросы, которые выводят следующую информацию:
-- 1. заказы, отправленные в города, заканчивающиеся на 'burg'.
-- Вывести без повторений две колонки (город, страна)
-- (см. таблица orders, колонки ship_city, ship_country)
SELECT DISTINCT ship_city, ship_country
from orders
where ship_city LIKE '%burg'
group by ship_city, ship_country

-- 2. из таблицы orders идентификатор заказа, идентификатор заказчика,
-- вес и страну отгрузки. Заказ отгружен в страны, начинающиеся на 'P'.
-- Результат отсортирован по весу (по убыванию). Вывести первые 10 записей.
SELECT order_id, customer_id, freight, ship_country
from orders
where ship_country LIKE 'P%'
LIMIT 10

-- 3. фамилию, имя и телефон сотрудников, у которых в данных отсутствует регион (см таблицу employees)
SELECT last_name, first_name, home_phone
from employees
where region IS NULL


-- 4. количество поставщиков (suppliers) в каждой из стран.
-- Результат отсортировать по убыванию количества поставщиков в стране
select country, count(country) as count_country
from suppliers
group by country
order by count_country DESC

-- 5. суммарный вес заказов (в которых известен регион) по странам,
-- но вывести только те результаты, где суммарный вес на страну больше 2750.
-- Отсортировать по убыванию суммарного веса
-- (см таблицу orders, колонки ship_region, ship_country, freight)
SELECT DISTINCT ship_region, ship_country, SUM(freight) as sum_freight
from orders
where ship_region IS NOT NULL
group by ship_region, ship_country
HAVING SUM(freight) > 30
order by SUM(freight) DESC


-- 6. страны, в которых зарегистрированы и заказчики (customers)
-- и поставщики (suppliers) и работники (employees).
select country from customers
INTERSECT
select country from suppliers
INTERSECT
select country from employees


-- 7. страны, в которых зарегистрированы и заказчики (customers) и
-- поставщики (suppliers), но не зарегистрированы работники (employees).
select country from customers
INTERSECT
select country from suppliers
EXCEPT
select country from employees
