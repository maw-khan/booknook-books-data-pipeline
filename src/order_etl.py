
# Step 3: Order Transformation and Loading

import os 
from dotenv import load_dotenv 
from sqlalchemy import create_engine 

load_dotenv() 

password = os.environ["DB_PASSWORD"] #¬ os.environ is a dictionary of environment values; this looks up

DATABASE_URL = (f"postgresql+psycopg2://postgres:{password}@localhost:5432/booknook") 
engine = create_engine(DATABASE_URL) 


from sqlalchemy import text 
import pandas as pd 
from datetime import datetime

raw = pd.read_csv("C:\\Users\\user\\python_data_course\\booknook_raw_orders.csv") 
print(f"Read {len(raw)} rows!") 
raw.head()

raw["customer_email"] = raw["customer_email"].str.strip().str.lower() 
		
def parse_date(value):
    for fmty in ("%Y-%m-%d", "%m/%d/%Y"):
        try: 
             return datetime.strptime(str(value).strip(), fmty).date()
        except ValueError:
	         continue
    return pd.NaT
	 
raw["order_date"] = raw["order_date"].apply(parse_date)

from sqlalchemy import text  # Marks the SQL string that follows as real SQL to run.
with engine.connect() as conn:  # Opens a temporary, auto-closing connection named conn.
    rows = conn.execute(text("SELECT customer_id, email FROM customers;"))
    customer_lookup = {r.email: r.customer_id for r in rows}

before = len(raw)
raw = raw.dropna(subset=["order_date"])
raw = raw[raw["customer_email"].isin(customer_lookup.keys())]
print(raw)
print(f"Dropped {before - len(raw)} unsafe row(s).")


raw["customer_id"] = raw["customer_email"].map(customer_lookup)

print(raw)

with engine.begin() as conn: 

     for _, order_row in raw.iterrows():

        result = conn.execute(text(""" 
        INSERT INTO orders (customer_id, order_date, status)
        VALUES (:customer_id, :order_date, :status)
        RETURNING order_id;"""),

        {"customer_id": int(order_row.customer_id
),
        "order_date": order_row.order_date, 
        "status": order_row.status})
        

DATA_DIR=r"C:\Users\user\python_data_course"

def load_seed_table(engine,csv_filename:str,table_name:str)->None:
	csv_path=f"{DATA_DIR}\\{csv_filename}"
	df=pd.read_csv(csv_path)
	df.to_sql(table_name,con=engine,if_exists="append",index=False, method="multi")
	print(f"Loaded {len(df)} rows from {csv_path} into '{table_name}'") 
	
def sync_sequence(engine, table_name: str, id_column: str) -> None:
	with engine.begin() as conn:
		conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{table_name}', '{id_column}'), "f"(SELECT MAX({id_column}) FROM {table_name}));"		))
	print(f"Synced auto-increment sequence for '{table_name}.{id_column}'")

def run_seed():
    engine = create_engine(DATABASE_URL)

    load_seed_table(engine, "booknook_orderitems_seed.csv", "orderitems")
    sync_sequence(engine, "orderitems", "order_item_id")
    
    print("Seed data loaded successfully.")
    
if __name__ == "__main__":
	run_seed()



with engine.connect() as conn:
    result1 = conn.execute(text("""
        SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
        UNION ALL
        SELECT 'products', COUNT(*) FROM products
        UNION ALL
        SELECT 'orders', COUNT(*) FROM orders
        UNION ALL
        SELECT 'orderitems', COUNT(*) FROM orderitems;
    """))

    for row in result1:
        print(f"{row.table_name}: {row.row_count}")