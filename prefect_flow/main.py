from prefect import flow
from setup_database import setup_database
from import_raw import import_raw
from data_cleaning import data_cleaning

@flow
def run():
    setup_task = setup_database()
    import_raw_task = import_raw()
    data_cleaning_task = data_cleaning()

if __name__ == '__main__':
    run()