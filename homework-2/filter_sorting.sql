-- Напишите запросы, которые выводят следующую информацию:

-- 1. заказы, доставленные в страны France, Germany, Spain (таблица orders,
-- колонка ship_country)
SELECT *
from orders
where ship_country in ('France', 'Germany', 'Spain')

-- 2. уникальные страны и города, куда отправлялись заказы, отсортировать по
-- странам и городам (таблица orders, колонки ship_country, ship_city)
select DISTINCT ship_country, ship_city
from orders
order by ship_country, ship_city


-- 3. сколько дней в среднем уходит на доставку товара в Германию
-- (таблица orders, колонки order_date, shipped_date, ship_country)
select AVG(shipped_date-order_date)
from orders
where ship_country like '%ermany%'

-- 4. минимальную и максимальную цену среди продуктов, не снятых с продажи
-- (таблица products, колонки unit_price, discontinued не равно 1)
SELECT MIN(unit_price) as min_price, MAX(unit_price)
FROM products
where discontinued <> 1


-- 5. минимальную и максимальную цену среди продуктов, не снятых с продажи и
-- которых имеется не меньше 20 (таблица products, колонки unit_price,
-- units_in_stock, discontinued не равно 1)
