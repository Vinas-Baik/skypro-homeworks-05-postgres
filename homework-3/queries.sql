-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника,
-- работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London,
-- а доставку заказа ведет компания United Package (company_name в табл shippers)


SELECT customers.company_name as "Название компании",
       CONCAT(employees.first_name, ' ', employees.last_name) as "ФИО сотрудника"
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

select products.product_name as "Наименование продукта",
       products.units_in_stock as "Количество товара",
       suppliers.contact_name as "Имя поставщика",
       suppliers.phone as "Телефон поставщика"
from products
inner join categories USING (category_id)
inner join suppliers USING (supplier_id)
where products.discontinued = 0 and
      products.units_in_stock < 25 and
      categories.category_name in ('Dairy Products', 'Condiments')
order by products.units_in_stock


-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа

select company_name as "Заказчик без заказов"
from customers
where customer_id NOT in (select customer_id
                          from orders
                          group by customer_id
                          having count(*) > 0 )


-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц
-- (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.

-- Запрос написан с использованием подзапроса

SELECT DISTINCT product_name
FROM products
where product_id in (SELECT product_id
                     from order_details
                     where quantity = 10)
ORDER BY product_name

-- Запрос написан с JOIN

SELECT DISTINCT products.product_name
FROM products
INNER JOIN order_details USING (product_id)
where order_details.quantity = 10
ORDER BY products.product_name