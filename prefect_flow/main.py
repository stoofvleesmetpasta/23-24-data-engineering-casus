from prefect import flow
from setup_database import connect_and_setup
from import_raw import import_raw
from data_cleaning import data_cleaning
from warehousing import run_all_inserts
from to_parquet import to_parquet
from upload_to_s3 import upload

@flow
def run():
    setup_flow = connect_and_setup()
    import_raw_flow = import_raw()
    cleaning_flow = data_cleaning()
    warehousing_flow = run_all_inserts()
    parquet_flow = to_parquet()
    upload_to_bucket_flow = upload()
    
if __name__ == '__main__':
    run()