# cd python_data_course (make sure all 4 provided csvs are in this folder)
# python -m venv etlproject
# etlproject\Scripts\Activate.ps1
# pip install numpy pandas matplotlib folium seaborn psycopg2-binary sqlalchemy python-dotenv pywaffle wordcloud plotly dash statsmodels
# & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -h localhost -p 5432 
# create database bookook;
# \q

## Step 1: Table Creation

import os 
from dotenv import load_dotenv 
from sqlalchemy import (
create_engine, Column, Integer, String, Numeric, Date,
ForeignKey, CheckConstraint, func
)
from sqlalchemy.orm import declarative_base, relationship

load_dotenv() 

password = os.environ["DB_PASSWORD"] #¬ os.environ is a dictionary of environment values; this looks up

DATABASE_URL = (f"postgresql+psycopg2://postgres:{password}@localhost:5432/booknook") 

# Base is a special class that every model below inherits from -- it's how
# SQLAlchemy keeps track of all your table definitions together, so it can
# create them all at once later.

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20))
    city = Column(String(50))
    signup_date = Column(Date, nullable=False, server_default=func.current_date())
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    __table_args__ = (CheckConstraint("unit_price >= 0", name="ck_products_unit_price"),)

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable
    =False)
    order_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, server_default="Completed")
    __table_args__ = (
    CheckConstraint("status IN ('Completed','Cancelled','Pending')", name="ck_orders_status"),
    )
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "orderitems"
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    __table_args__ = (
    CheckConstraint("quantity > 0", name="ck_orderitems_quantity"),
    CheckConstraint("unit_price >= 0", name="ck_orderitems_unit_price"),
    )
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

def create_all_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine) # creates any table that doesn't exist yet; safe to re-run
    print("All Booknook tables created (or already existed).")
    return engine

if __name__ == "__main__":
    create_all_tables()
	
	
