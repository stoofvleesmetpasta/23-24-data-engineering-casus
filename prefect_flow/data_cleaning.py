import re
from sqlalchemy import create_engine, inspect
import pandas as pd
import sqlalchemy.types as sqlalchemytypes
from prefect import task
import psycopg2

@task
def data_cleaning():
    # Initialize variables
    aankomst_df = pd.DataFrame()
    banen_df = pd.DataFrame()
    klant_df = pd.DataFrame()
    luchthavens_df = pd.DataFrame()
    maatschappijen_df = pd.DataFrame()
    planning_df = pd.DataFrame()
    vertrek_df = pd.DataFrame()
    vliegtuig_df = pd.DataFrame()
    vliegtuigtype_df = pd.DataFrame()
    vlucht_df = pd.DataFrame()
    weer_df = pd.DataFrame()

    tables_raw = []
    tables_clean = []

    # Column types specified
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
            "plantijd": sqlalchemytypes.TIME,
        },
        'vertrek': {
            "vluchtid": sqlalchemytypes.String,
            "vliegtuigcode": sqlalchemytypes.String,
            "terminal": sqlalchemytypes.String,
            "gate": sqlalchemytypes.String,
            "baan": sqlalchemytypes.String,
            "bezetting": sqlalchemytypes.SmallInteger,
            "vracht": sqlalchemytypes.String,
            "vertrektijd": sqlalchemytypes.TIME,
        },
        'vliegtuig': {
            "airlinecode": sqlalchemytypes.String,
            "vliegtuigcode": sqlalchemytypes.String,
            "vliegtuigtype": sqlalchemytypes.String,
            "bouwjaar": sqlalchemytypes.String,
        },
        'vliegtuigtype': {
            "iata": sqlalchemytypes.String,
            "icao": sqlalchemytypes.String,
            "merk": sqlalchemytypes.String,
            "type": sqlalchemytypes.String,
            "wake": sqlalchemytypes.String,
            "cat": sqlalchemytypes.String,
            "capaciteit": sqlalchemytypes.String,
            "vracht": sqlalchemytypes.String,
        },
        'vlucht': {
            "vluchtid": sqlalchemytypes.String,
            "vluchtnr": sqlalchemytypes.String,
            "airlinecode": sqlalchemytypes.String,
            "destcode": sqlalchemytypes.String,
            "vliegtuigcode": sqlalchemytypes.String,
            "datum": sqlalchemytypes.String,
        },
        'weer': {
            "datum": sqlalchemytypes.String,
            "ddvec": sqlalchemytypes.String,
            "fhvec": sqlalchemytypes.String,
            "fg": sqlalchemytypes.String,
            "fhx": sqlalchemytypes.String,
            "fhxh": sqlalchemytypes.String,
            "fhn": sqlalchemytypes.String,
            "fhnh": sqlalchemytypes.String,
            "fxx": sqlalchemytypes.String,
            "fxxh": sqlalchemytypes.String,
            "tg": sqlalchemytypes.String,
            "tn": sqlalchemytypes.String,
            "tnh": sqlalchemytypes.String,
            "tx": sqlalchemytypes.String,
            "txh": sqlalchemytypes.String,
            "t10n": sqlalchemytypes.String,
            "t10nh": sqlalchemytypes.String,
            "sq": sqlalchemytypes.String,
            "sp": sqlalchemytypes.String,
            "q": sqlalchemytypes.String,
            "dr": sqlalchemytypes.String,
            "rh": sqlalchemytypes.String,
            "rhx": sqlalchemytypes.String,
            "rhxh": sqlalchemytypes.String,
            "pg": sqlalchemytypes.String,
            "px": sqlalchemytypes.String,
            "pxh": sqlalchemytypes.String,
            "pn": sqlalchemytypes.String,
            "pnh": sqlalchemytypes.String,
            "vvn": sqlalchemytypes.String,
            "vvnh": sqlalchemytypes.String,
            "vvx": sqlalchemytypes.String,
            "vvxh": sqlalchemytypes.String,
            "ng": sqlalchemytypes.String,
            "ug": sqlalchemytypes.String,
            "ux": sqlalchemytypes.String,
            "uxh": sqlalchemytypes.String,
            "un": sqlalchemytypes.String,
            "unh": sqlalchemytypes.String,
            "ev2": sqlalchemytypes.String,
        }
    }

    engine = create_engine('postgresql://postgres:Newpassword@192.168.56.1:5433/postgres')
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema='raw')

    # Load each table into a DataFrame and assign it to a variable
    for table in tables:
        df = pd.read_sql_table(table, con=engine, schema='raw')
        df.columns = df.columns.str.lower()
        globals()[f'{table}_df'] = df
        tables_raw.append(df)

    special_char_pattern = re.compile(r'[^a-zA-Z0-9\s]')

    for df, table in zip([aankomst_df, banen_df, klant_df, luchthavens_df, maatschappijen_df, planning_df, vertrek_df, vliegtuig_df, vliegtuigtype_df, vlucht_df, weer_df], 
                         ['aankomst', 'banen', 'klant', 'luchthavens', 'maatschappijen', 'planning', 'vertrek', 'vliegtuig', 'vliegtuigtype', 'vlucht', 'weer']):
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

        if table == 'maatschappijen' or table == 'vliegtuig':
            columns_to_check = df.columns[df.columns != 'name']
            df = df[~df[columns_to_check].apply(lambda row: row.astype(str).str.contains(special_char_pattern).any(), axis=1)]

        if 'icao' in df.columns:
            df = df[df['icao'].notnull() & (df['icao'] != '/N')]

        if 'iata' in df.columns:
            df = df[df['iata'].notnull()]

        if 'cat' in df.columns:
            df = df[df['cat'].notnull()]

        if table == 'vliegtuigtype':
            df = df.dropna(thresh=df.shape[1]-1)

        tables_clean.append(df)
        df.to_sql(table, con=engine, schema='cleansed', if_exists='append', index=False, dtype=column_types_cleansed[table])

    for df_raw, df_clean, table in zip(tables_raw, tables_clean, ['aankomst', 'banen', 'klant', 'luchthavens', 'maatschappijen', 'planning', 'vertrek', 'vliegtuig', 'vliegtuigtype', 'vlucht', 'weer']):
        deleted_indices = df_raw.index.difference(df_clean.index)
        deleted_records = df_raw.loc[deleted_indices]
        deleted_records_filtered = deleted_records[[col for col in deleted_records.columns if col in column_types_cleansed[table]]]
        deleted_records_filtered.to_sql(table, con=engine, schema='archived', if_exists='append', index=False, dtype=column_types_cleansed[table])
    
    print("Data cleaning and import complete.")
