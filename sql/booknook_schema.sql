-- BookNook Books — schema.sql
-- Plain-SQL equivalent of the SQLAlchemy models in create_tables.py.
-- Run this in psql/pgAdmin if you prefer raw SQL over SQLAlchemy for Task 1.1.

CREATE DATABASE booknook;
\c booknook

CREATE TABLE customers (
    customer_id  SERIAL PRIMARY KEY,
    first_name   VARCHAR(50)  NOT NULL,
    last_name    VARCHAR(50)  NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    phone        VARCHAR(20),
    city         VARCHAR(50),
    signup_date  DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE products (
    product_id    SERIAL PRIMARY KEY,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(50)  NOT NULL,
    unit_price    NUMERIC(10,2) NOT NULL,
    CONSTRAINT ck_products_unit_price CHECK (unit_price >= 0)
);

CREATE TABLE orders (
    order_id     SERIAL PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date   DATE NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'Completed',
    CONSTRAINT ck_orders_status CHECK (status IN ('Completed','Cancelled','Pending'))
);

CREATE TABLE orderitems (
    order_item_id  SERIAL PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    product_id     INTEGER NOT NULL REFERENCES products(product_id),
    quantity       INTEGER NOT NULL,
    unit_price     NUMERIC(10,2) NOT NULL,
    CONSTRAINT ck_orderitems_quantity   CHECK (quantity > 0),
    CONSTRAINT ck_orderitems_unit_price CHECK (unit_price >= 0)
);
