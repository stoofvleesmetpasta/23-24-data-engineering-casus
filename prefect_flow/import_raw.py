from sqlalchemy import create_engine, types as sqlalchemytypes
import pandas as pd
from prefect import task, flow

tables = {
    'aankomst': './source_data/export_aankomst.txt',
    'banen': './source_data/export_banen.csv',
    'klant': './source_data/export_klant.csv',
    'luchthavens': './source_data/export_luchthavens.txt',
    'maatschappijen': './source_data/export_maatschappijen.txt',
    'planning': './source_data/export_planning.txt',
    'vertrek': './source_data/export_vertrek.txt',
    'vliegtuig': './source_data/export_vliegtuig.txt',
    'vliegtuigtype': './source_data/export_vliegtuigtype.csv',
    'vlucht': './source_data/export_vlucht.txt',
    'weer': './source_data/export_weer.txt'
}


@task
def load_data_to_db(table, file_path, engine, column_types_raw):
    if table in ['banen', 'klant', 'vliegtuigtype']:
        try:
            df = pd.read_csv(file_path, sep=';', dtype=str, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, sep=';', dtype=str, encoding='latin1')
    else:
        try:
            df = pd.read_csv(file_path, sep='\t', dtype=str, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, sep='\t', dtype=str, encoding='latin1')
    
    df.to_sql(table, con=engine, schema='raw', if_exists='append', index=False, dtype=column_types_raw[table])

@flow
def import_raw():
    column_types_raw = {
    'aankomst': {
        "Vluchtid": sqlalchemytypes.String,
        "Vliegtuigcode": sqlalchemytypes.String,
        "Terminal": sqlalchemytypes.String,
        "Gate": sqlalchemytypes.String,
        "Baan": sqlalchemytypes.String,
        "Bezetting": sqlalchemytypes.String,
        "Vracht": sqlalchemytypes.String,
        "Aankomsttijd": sqlalchemytypes.String,
    },
    'banen': {
        "Baannummer": sqlalchemytypes.String,
        "Code": sqlalchemytypes.String,
        "Naam": sqlalchemytypes.String,
        "Lengte": sqlalchemytypes.String,
    },
    'klant': {
        "Vluchtid": sqlalchemytypes.String,
        "Operatie": sqlalchemytypes.String,
        "Faciliteiten": sqlalchemytypes.String,
        "Shops": sqlalchemytypes.String,
    },
    'luchthavens': {
        "Airport": sqlalchemytypes.String,
        "City": sqlalchemytypes.String,
        "Country": sqlalchemytypes.String,
        "IATA": sqlalchemytypes.String,
        "ICAO": sqlalchemytypes.String,
        "Lat": sqlalchemytypes.String,
        "Lon": sqlalchemytypes.String,
        "Alt": sqlalchemytypes.String,
        "TZ": sqlalchemytypes.String,
        "DST": sqlalchemytypes.String,
        "TzName": sqlalchemytypes.String,
    },
    'maatschappijen': {
        "Name": sqlalchemytypes.String,
        "IATA": sqlalchemytypes.String,
        "ICAO": sqlalchemytypes.String,
    },
    'planning': {
        "Vluchtnr": sqlalchemytypes.String,
        "Airlinecode": sqlalchemytypes.String,
        "Destcode": sqlalchemytypes.String,
        "Planterminal": sqlalchemytypes.String,
        "Plangate": sqlalchemytypes.String,
        "Plantijd": sqlalchemytypes.String,
    },
    'vertrek': {
        "Vluchtid": sqlalchemytypes.String,
        "Vliegtuigcode": sqlalchemytypes.String,
        "Terminal": sqlalchemytypes.String,
        "Gate": sqlalchemytypes.String,
        "Baan": sqlalchemytypes.String,
        "Bezetting": sqlalchemytypes.String,
        "Vracht": sqlalchemytypes.String,
        "Vertrektijd": sqlalchemytypes.String,
    },
    'vliegtuig': {
        "Airlinecode": sqlalchemytypes.String,
        "Vliegtuigcode": sqlalchemytypes.String,
        "Vliegtuigtype": sqlalchemytypes.String,
        "Bouwjaar": sqlalchemytypes.String,
    },
    'vliegtuigtype': {
        "IATA": sqlalchemytypes.String,
        "ICAO": sqlalchemytypes.String,
        "Merk": sqlalchemytypes.String,
        "Type": sqlalchemytypes.String,
        "Wake": sqlalchemytypes.String,
        "Cat": sqlalchemytypes.String,
        "Capaciteit": sqlalchemytypes.String,
        "Vracht": sqlalchemytypes.String,
    },
    'vlucht': {
        "Vluchtid": sqlalchemytypes.String,
        "Vluchtnr": sqlalchemytypes.String,
        "Airlinecode": sqlalchemytypes.String,
        "Destcode": sqlalchemytypes.String,
        "Vliegtuigcode": sqlalchemytypes.String,
        "Datum": sqlalchemytypes.String,
    },
    'weer': {
        "Datum": sqlalchemytypes.String,
        "DDVEC": sqlalchemytypes.String,
        "FHVEC": sqlalchemytypes.String,
        "FG": sqlalchemytypes.String,
        "FHX": sqlalchemytypes.String,
        "FHXH": sqlalchemytypes.String,
        "FHN": sqlalchemytypes.String,
        "FHNH": sqlalchemytypes.String,
        "FXX": sqlalchemytypes.String,
        "FXXH": sqlalchemytypes.String,
        "TG": sqlalchemytypes.String,
        "TN": sqlalchemytypes.String,
        "TNH": sqlalchemytypes.String,
        "TX": sqlalchemytypes.String,
        "TXH": sqlalchemytypes.String,
        "T10N": sqlalchemytypes.String,
        "T10NH": sqlalchemytypes.String,
        "SQ": sqlalchemytypes.String,
        "SP": sqlalchemytypes.String,
        "Q": sqlalchemytypes.String,
        "DR": sqlalchemytypes.String,
        "RH": sqlalchemytypes.String,
        "RHX": sqlalchemytypes.String,
        "RHXH": sqlalchemytypes.String,
        "PG": sqlalchemytypes.String,
        "PX": sqlalchemytypes.String,
        "PXH": sqlalchemytypes.String,
        "PN": sqlalchemytypes.String,
        "PNH": sqlalchemytypes.String,
        "VVN": sqlalchemytypes.String,
        "VVNH": sqlalchemytypes.String,
        "VVX": sqlalchemytypes.String,
        "VVXH": sqlalchemytypes.String,
        "NG": sqlalchemytypes.String,
        "UG": sqlalchemytypes.String,
        "UX": sqlalchemytypes.String,
        "UXH": sqlalchemytypes.String,
        "UN": sqlalchemytypes.String,
        "UNH": sqlalchemytypes.String,
        "EV2": sqlalchemytypes.String,
    }
}
    engine = create_engine('postgresql://postgres:Newpassword@192.168.56.1:5433/postgres')

    for table, file_path in tables.items():
        load_data_to_db(table, file_path, engine, column_types_raw)

