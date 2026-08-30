-- Part 3: run this in MySQL Workbench to create the company database with
-- the same schema as the SQLite version, so the agent can be pointed at
-- either backend and get the same table shape.

CREATE DATABASE IF NOT EXISTS company;
USE company;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    employee_id INT,
    amount INT,
    sale_date DATE
);

INSERT INTO employees (id, name, department, salary) VALUES
    (1, 'Aditi Rao', 'Engineering', 95000),
    (2, 'Rohan Mehta', 'Sales', 62000),
    (3, 'Neha Kulkarni', 'Engineering', 88000),
    (4, 'Sameer Joshi', 'Sales', 71000),
    (5, 'Priya Nair', 'Marketing', 58000),
    (6, 'Karan Verma', 'Engineering', 102000),
    (7, 'Ishita Sharma', 'HR', 54000),
    (8, 'Arjun Patil', 'Sales', 67000),
    (9, 'Meera Iyer', 'Marketing', 60000),
    (10, 'Devansh Gupta', 'Engineering', 91000);

INSERT INTO sales (sale_id, employee_id, amount, sale_date) VALUES
    (1, 2, 15000, '2025-01-14'),
    (2, 2, 9800, '2025-02-03'),
    (3, 4, 21000, '2025-01-22'),
    (4, 4, 13500, '2025-03-11'),
    (5, 8, 18700, '2025-02-19'),
    (6, 8, 9400, '2025-04-02'),
    (7, 2, 12300, '2025-04-18'),
    (8, 4, 16800, '2025-05-05'),
    (9, 8, 11200, '2025-05-21'),
    (10, 2, 20500, '2025-06-09'),
    (11, 4, 8900, '2025-06-27'),
    (12, 8, 14600, '2025-07-15');
