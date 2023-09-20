SELECT * from shippers
where company_name='United Package'

SELECT * from customers
where city = 'London'

SELECT CONCAT(first_name, ' ', last_name) from employees
where city = 'London'

select * from orders


select * from suppliers

select * from categories
where category_name in ('Dairy Products', 'Condiments')
