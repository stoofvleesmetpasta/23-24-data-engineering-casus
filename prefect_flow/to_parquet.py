import os
from prefect import task, flow
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Database connection setup
engine = create_engine('postgresql://postgres:Newpassword@192.168.1.18:5433/postgres')
inspector = inspect(engine)

@task
def data_to_parquet():   
    # Create the parquet directory if it does not exist
    output_dir = "parquet"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Retrieve the list of tables in the 'warehouse' schema
    tables = inspector.get_table_names(schema='warehouse')
    
    # Export each table to a Parquet file
    for table in tables:
        df = pd.read_sql_table(table, con=engine, schema='warehouse')
        output_file = os.path.join(output_dir, f"{table}.parquet")
        df.to_parquet(output_file)
        print(f"Exported {table} to {output_file}")

@flow
def to_parquet():
    data_to_parquet()



