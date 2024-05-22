import re
from sqlalchemy import create_engine, inspect
import pandas as pd
import sqlalchemy.types as sqlalchemytypes
from prefect import task, flow
import psycopg2


@task
def clean_data(df, table_name, column_types):
    special_char_pattern = re.compile(r'[^a-zA-Z0-9\s]')
    
    df.dropna(how='all', inplace=True)
    df.drop_duplicates(inplace=True)

    if 'aankomsttijd' in df.columns:
        df['aankomsttijd'] = pd.to_datetime(df['aankomsttijd'], errors='coerce')
        df = df[df['aankomsttijd'].notnull()]

    if 'vertrektijd' in df.columns:
        df['vertrektijd'] = pd.to_datetime(df['vertrektijd'], errors='coerce')
        df = df[df['vertrektijd'].notnull()]

    if 'terminal' in df.columns and 'gate' in df.columns:
        df.loc[(df['terminal'] == 'F') & (df['gate'].isnull()), 'gate'] = 'F1'
        df.loc[(df['terminal'] == 'G') & (df['gate'].isnull()), 'gate'] = 'G1'

    if 'bezetting' in df.columns and 'vracht' in df.columns:
        df.loc[df['bezetting'].isnull() & df['vracht'].notnull(), 'bezetting'] = 0
        df.loc[df['vracht'].isnull() & df['bezetting'].notnull(), 'vracht'] = 0
        df = df.dropna(subset=['bezetting', 'vracht'], how='all')

    if table_name == 'maatschappijen' or table_name == 'vliegtuig':
        columns_to_check = df.columns[df.columns != 'name']
        df = df[~df[columns_to_check].apply(lambda row: row.astype(str).str.contains(special_char_pattern).any(), axis=1)]

    if 'icao' in df.columns:
        df = df[df['icao'].notnull() & (df['icao'] != '/N')]

    if 'iata' in df.columns:
        df = df[df['iata'].notnull()]
        df = df[df['iata'].str.match(r'^[a-zA-Z0-9]*$')]
        df['iata'] = df['iata'].astype(str).str.slice(0, 5)

    if 'cat' in df.columns:
        df = df[df['cat'].notnull()]

    if table_name == 'vliegtuigtype':
        df = df.dropna(thresh=df.shape[1]-1)

    return df

@task
def archive_deleted_and_upload_clean(engine, df_raw, df_clean, table_name, column_types):
    deleted_indices = df_raw.index.difference(df_clean.index)
    deleted_records = df_raw.loc[deleted_indices]
    deleted_records_filtered = deleted_records[[col for col in deleted_records.columns if col in column_types[table_name]]]
    deleted_records_filtered.to_sql(table_name, con=engine, schema='archived', if_exists='append', index=False, dtype=column_types[table_name])
    df_clean.to_sql(table_name, con=engine, schema='cleansed', if_exists='append', index=False, dtype=column_types[table_name])

@flow
def data_cleaning():
    engine = create_engine('postgresql://postgres:Newpassword@192.168.1.18:5433/postgres')
    inspector = inspect(engine)
    table_names = inspector.get_table_names(schema='raw')

    column_types_cleansed = {
        'aankomst': {
            "vluchtid": sqlalchemytypes.String,
            "vliegtuigcode": sqlalchemytypes.String,
            "terminal": sqlalchemytypes.String,
            "gate": sqlalchemytypes.String,
            "baan": sqlalchemytypes.String,
            "bezetting": sqlalchemytypes.SmallInteger,
            "vracht": sqlalchemytypes.String,
            "aankomsttijd": sqlalchemytypes.TIMESTAMP,
        },
        'banen': {
            "baannummer": sqlalchemytypes.String,
            "code": sqlalchemytypes.String,
            "naam": sqlalchemytypes.String,
            "lengte": sqlalchemytypes.SmallInteger,
        },
        'klant': {
            "vluchtid": sqlalchemytypes.String,
            "operatie": sqlalchemytypes.Numeric,
            "faciliteiten": sqlalchemytypes.Numeric,
            "shops": sqlalchemytypes.Numeric,
        },
        'luchthavens': {
            "airport": sqlalchemytypes.String,
            "city": sqlalchemytypes.String,
            "country": sqlalchemytypes.String,
            "iata": sqlalchemytypes.String,
            "icao": sqlalchemytypes.String,
            "lat": sqlalchemytypes.Float,
            "lon": sqlalchemytypes.Float,
            "alt": sqlalchemytypes.SmallInteger,
            "tz": sqlalchemytypes.String,
            "dst": sqlalchemytypes.String,
            "tzname": sqlalchemytypes.String,
        },
        'maatschappijen': {
            "name": sqlalchemytypes.String,
            "iata": sqlalchemytypes.String,
            "icao": sqlalchemytypes.String,
        },
        'planning': {
            "vluchtnr": sqlalchemytypes.String,
            "airlinecode": sqlalchemytypes.String,
            "destcode": sqlalchemytypes.String,
            "planterminal": sqlalchemytypes.String,
            "plangate": sqlalchemytypes.String,
            "plantijd": sqlalchemytypes.Time,
        },
        'vertrek': {
            "vluchtid": sqlalchemytypes.String,
            "vliegtuigcode": sqlalchemytypes.String,
            "terminal": sqlalchemytypes.String,
            "gate": sqlalchemytypes.String,
            "baan": sqlalchemytypes.String,
            "bezetting": sqlalchemytypes.SmallInteger,
            "vracht": sqlalchemytypes.String,
            "vertrektijd": sqlalchemytypes.TIMESTAMP,
        },
        'vliegtuig': {
            "airlinecode": sqlalchemytypes.String,
            "vliegtuigcode": sqlalchemytypes.String,
            "vliegtuigtype": sqlalchemytypes.String,
            "bouwjaar": sqlalchemytypes.Integer,
        },
        'vliegtuigtype': {
            "iata": sqlalchemytypes.String,
            "icao": sqlalchemytypes.String,
            "merk": sqlalchemytypes.String,
            "type": sqlalchemytypes.String,
            "wake": sqlalchemytypes.String,
            "cat": sqlalchemytypes.String,
            "capaciteit": sqlalchemytypes.Integer,
            "vracht": sqlalchemytypes.Integer,
        },
        'vlucht': {
            "vluchtid": sqlalchemytypes.Integer,
            "vluchtnr": sqlalchemytypes.String,
            "airlinecode": sqlalchemytypes.String,
            "destcode": sqlalchemytypes.String,
            "vliegtuigcode": sqlalchemytypes.String,
            "datum": sqlalchemytypes.Date,
        },
        'weer': {
            "datum": sqlalchemytypes.Date,
            "ddvec": sqlalchemytypes.Integer,
            "fhvec": sqlalchemytypes.Integer,
            "fg": sqlalchemytypes.Integer,
            "fhx": sqlalchemytypes.Integer,
            "fhxh": sqlalchemytypes.Integer,
            "fhn": sqlalchemytypes.Integer,
            "fhnh": sqlalchemytypes.Integer,
            "fxx": sqlalchemytypes.Integer,
            "fxxh": sqlalchemytypes.Integer,
            "tg": sqlalchemytypes.Integer,
            "tn": sqlalchemytypes.Integer,
            "tnh": sqlalchemytypes.Integer,
            "tx": sqlalchemytypes.Integer,
            "txh": sqlalchemytypes.Integer,
            "t10n": sqlalchemytypes.Integer,
            "t10nh": sqlalchemytypes.Integer,
            "sq": sqlalchemytypes.Integer,
            "sp": sqlalchemytypes.Integer,
            "q": sqlalchemytypes.Integer,
            "dr": sqlalchemytypes.Integer,
            "rh": sqlalchemytypes.Integer,
            "rhx": sqlalchemytypes.Integer,
            "rhxh": sqlalchemytypes.Integer,
            "pg": sqlalchemytypes.Integer,
            "px": sqlalchemytypes.Integer,
            "pxh": sqlalchemytypes.Integer,
            "pn": sqlalchemytypes.Integer,
            "pnh": sqlalchemytypes.Integer,
            "vvn": sqlalchemytypes.Integer,
            "vvnh": sqlalchemytypes.Integer,
            "vvx": sqlalchemytypes.Integer,
            "vvxh": sqlalchemytypes.Integer,
            "ng": sqlalchemytypes.Integer,
            "ug": sqlalchemytypes.Integer,
            "ux": sqlalchemytypes.Integer,
            "uxh": sqlalchemytypes.Integer,
            "un": sqlalchemytypes.Integer,
            "unh": sqlalchemytypes.Integer,
            "ev2": sqlalchemytypes.Integer,
        }
    }

    for table_name in table_names:
        df_raw = pd.read_sql_table(table_name, con=engine, schema='raw')
        df_raw.columns = df_raw.columns.str.lower()
        df_clean = clean_data(df_raw, table_name, column_types_cleansed)
        archive_deleted_and_upload_clean(engine, df_raw, df_clean, table_name, column_types_cleansed)
        
    print("Data cleaning and import complete.")


