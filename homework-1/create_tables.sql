-- SQL-команды для создания таблиц
-- Создаем базу north
CREATE DATABASE north;

-- Создаем таблицы 

CREATE TABLE customers(
	customer_id varchar(10) NOT NULL PRIMARY KEY,
	company_name varchar(50) NOT NULL,
	contact_name varchar(50)
);

CREATE TABLE employees(
	employee_id int NOT NULL PRIMARY KEY, 
	first_name varchar(50) NOT NULL, 
	last_name varchar(50),
	title varchar(100),
	birth_date date,
	notes text 
); 

-- отношение один к многим 

CREATE TABLE orders(
	order_id int NOT NULL PRIMARY KEY, 
	customer_id varchar(10) NOT NULL REFERENCES customers(customer_id),
	employee_id int NOT NULL REFERENCES employees(employee_id),
	order_date date,
	ship_city varchar(50)
);
