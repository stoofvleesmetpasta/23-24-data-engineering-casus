from prefect import flow
from setup_database import connect_and_setup
from import_raw import import_raw
from data_cleaning import data_cleaning

@flow
def run():
    setup_flow = connect_and_setup()
    import_raw_flow = import_raw()
    cleaning_flow = data_cleaning()

if __name__ == '__main__':
    run()