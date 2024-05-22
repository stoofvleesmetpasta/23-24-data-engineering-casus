import re
from sqlalchemy import create_engine, inspect
import pandas as pd
import sqlalchemy.types as sqlalchemytypes
from prefect import task, flow
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define connection to the PostgreSQL database
engine = create_engine('postgresql://postgres:Newpassword@192.168.1.18:5433/postgres')
inspector = inspect(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Load data from the `cleansed` schema tables into DataFrames
df_aankomst = pd.read_sql_table('aankomst', con=engine, schema='cleansed')
df_banen = pd.read_sql_table('banen', con=engine, schema='cleansed')
df_luchthavens = pd.read_sql_table('luchthavens', con=engine, schema='cleansed')
df_klant = pd.read_sql_table('klant', con=engine, schema='cleansed')
df_maatschappijen = pd.read_sql_table('maatschappijen', con=engine, schema='cleansed')
df_planning = pd.read_sql_table('planning', con=engine, schema='cleansed')
df_vertrek = pd.read_sql_table('vertrek', con=engine, schema='cleansed')
df_vliegtuig = pd.read_sql_table('vliegtuig', con=engine, schema='cleansed')
df_vlucht = pd.read_sql_table('vlucht', con=engine, schema='cleansed')
df_weer = pd.read_sql_table('weer', con=engine, schema='cleansed')

# Function to insert data into the 'vliegtuig_dim' table
def insert_vliegtuig_dim():
    df_vliegtuig_dim = pd.DataFrame({
        'luchtvaartmaatschappij_code': df_vliegtuig['airlinecode'],
        'vliegtuig_code': df_vliegtuig['vliegtuigcode'],
        'fabrikant': df_vliegtuig['merk'],
        'vliegtuigtype_naam': df_vliegtuig['type'],
        'wakkerruimte_categorie': df_vliegtuig['wake'],
        'vliegtuig_nood': df_vliegtuig['cat'],
        'capaciteit': df_vliegtuig['capaciteit'],
        'vrachtcapaciteit': df_vliegtuig['vracht']
    })
    df_vliegtuig_dim.to_sql('vliegtuig_dim', con=engine, schema='warehouse', if_exists='append', index=False)

# Function to insert data into the 'luchtvaartmaatschappijen_dim' table
def insert_luchtvaartmaatschappijen_dim():
    df_luchtvaartmaatschappijen_dim = pd.DataFrame({
        'luchtvaartmaatschappij_naam': df_maatschappijen['name'],
        'iata_code': df_maatschappijen['iata'],
        'icao_code': df_maatschappijen['icao']
    })
    df_luchtvaartmaatschappijen_dim.to_sql('luchtvaartmaatschappijen_dim', con=engine, schema='warehouse', if_exists='append', index=False, method='multi')

# Function to insert data into the 'luchthavens_dim' table
def insert_luchthavens_dim():
    df_luchthavens_dim = pd.DataFrame({
        'luchthaven_naam': df_luchthavens['airport'],
        'land': df_luchthavens['country'],
        'stad': df_luchthavens['city'],
        'iata_code': df_luchthavens['iata'],
        'icao_code': df_luchthavens['icao'],
        'breedtegraad': df_luchthavens['lat'],
        'lengtegraad': df_luchthavens['lon'],
        'hoogte': df_luchthavens['alt'],
        'tijdzone': df_luchthavens['tz'],
        'dst': df_luchthavens['dst']
    })
    df_luchthavens_dim.to_sql('luchthavens_dim', con=engine, schema='warehouse', if_exists='append', index=False, method='multi')

# Function to insert data into the 'klanten_dim' table
def insert_klanten_dim():
    df_klanten_dim = pd.DataFrame({
        'vlucht_id': df_klant['vluchtid'],
        'operationele_tevredeheid': df_klant['operatie'],
        'faciliteiten_tevredeheid': df_klant['faciliteiten'],
        'winkels_tevredeheid': df_klant['shops']
    })
    df_klanten_dim.to_sql('klanten_dim', con=engine, schema='warehouse', if_exists='append', index=False, method='multi')

# Function to insert data into the 'weer_dim' table
def insert_weer_dim():
    df_weer_dim = pd.DataFrame({
        'observatie_datum': df_weer['datum'],
        'wind_richting_graden': df_weer['ddvec'],
        'gemiddelde_uurlijkse_windsnelheid': df_weer['fhvec'],
        'gemiddelde_dagelijkse_windsnelheid': df_weer['fg'],
        'maximale_uurlijkse_windsnelheid': df_weer['fhx'],
        'minimale_uurlijkse_windsnelheid': df_weer['fhxh'],
        'maximale_uurlijkse_windsnelheid_tijd': df_weer['fhn'],
        'minimale_uurlijkse_windsnelheid_tijd': df_weer['fhnh'],
        'maximale_windsnelheid': df_weer['fxx'],
        'minimale_windsnelheid': df_weer['fxxh'],
        'gemiddelde_temperatuur': df_weer['tg'],
        'maximale_temperatuur': df_weer['tn'],
        'minimale_temperatuur': df_weer['tnh'],
        'maximale_temperatuur_tijd': df_weer['tx'],
        'minimale_temperatuur_tijd': df_weer['txh'],
        'zonneschijnduur_uren': df_weer['t10n'],
        'zonneschijn_percentage': df_weer['t10nh'],
        'globale_straling': df_weer['sq'],
        'neerslagduur_uren': df_weer['rh'],
        'totale_neerslag': df_weer['rh'],
        'maximale_uurlijkse_neerslag': df_weer['rhx'],
        'maximale_uurlijkse_neerslag_tijd': df_weer['rhxh'],
        'gemiddelde_luchtdruk': df_weer['pg'],
        'minimale_luchtdruk': df_weer['px'],
        'maximale_luchtdruk': df_weer['pxh'],
        'minimale_luchtdruk_tijd': df_weer['pn'],
        'maximale_luchtdruk_tijd': df_weer['pnh'],
        'minimale_zichtbaarheid': df_weer['vvnh'],
        'maximale_zichtbaarheid': df_weer['vvx'],
        'gemiddelde_zichtbaarheid': df_weer['vvxh'],
        'gemiddelde_bewolking': df_weer['ng'],
        'gemiddelde_relatieve_vochtigheid': df_weer['ug'],
        'maximale_relatieve_vochtigheid': df_weer['ux'],
        'minimale_relatieve_vochtigheid': df_weer['uxh'],
        'minimale_relatieve_vochtigheid_tijd': df_weer['un'],
        'maximale_relatieve_vochtigheid_tijd': df_weer['unh'],
        'potentiële_verdamping': df_weer['ev2']
    })
    df_weer_dim.to_sql('weer_dim', con=engine, schema='warehouse', if_exists='append', index=False, method='multi')

# Function to insert data into the 'vluchten_feit' table
def insert_vluchten_feit():
    df_vluchten_feit = pd.DataFrame({
        'vluchtnummer': df_vlucht['vluchtnr'],
        'luchtvaartmaatschappij_id': df_vlucht['luchtvaartmaatschappij_id'],  # Assuming this is already in the dataframe
        'bestemmingscode': df_planning['destcode'],
        'vliegtuig_id': df_vlucht['vluchtid'],
        'bezetting': df_vertrek['bezetting'],
        'vrachtcapaciteit': df_vertrek['vracht'],
        'aankomsttijd': df_aankomst['aankomsttijd'],
        'vertrektijd': df_vertrek['vertrektijd'],
        'weer_id': df_vlucht['weer_id'],  # Assuming this is already in the dataframe
        'bestemming_luchthaven_id': df_vlucht['bestemming_luchthaven_id'],  # Assuming this is already in the dataframe
        'vlucht_id': df_vlucht['vluchtid']
    })
    df_vluchten_feit.to_sql('vluchten_feit', con=engine, schema='warehouse', if_exists='append', index=False, method='multi')

# Insert data into the respective tables
insert_vliegtuig_dim()
insert_luchtvaartmaatschappijen_dim()
insert_luchthavens_dim()
insert_klanten_dim()
insert_weer_dim()
insert_vluchten_feit()
