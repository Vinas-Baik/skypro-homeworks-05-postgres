-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника,
-- работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London,
-- а доставку заказа ведет компания United Package (company_name в табл shippers)

-- SELECT * from shippers
-- where company_name='United Package'

-- SELECT * from customers
-- where city = 'London'

-- SELECT CONCAT(first_name, ' ', last_name) from employees
-- where city = 'London'

-- select * from orders

SELECT customers.company_name, CONCAT(employees.first_name, ' ', employees.last_name)
from orders
INNER JOIN customers USING (customer_id)
INNER JOIN employees USING (employee_id)
INNER JOIN shippers ON shippers.shipper_id=orders.ship_via
where shippers.company_name='United Package' and
      customers.city = 'London' and
      employees.city = 'London'



-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.


-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа


-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.
