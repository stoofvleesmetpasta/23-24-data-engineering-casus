import re
from sqlalchemy import create_engine, inspect
import pandas as pd
import sqlalchemy.types as sqlalchemytypes
from prefect import task, flow
import psycopg2
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, DATE, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Maatschappijen(Base):
    __tablename__ = 'maatschappijen'

    maatschappijid = Column(Integer, primary_key=True)
    naam = Column(String(100), nullable=False)
    iata = Column(String(3))
    icao = Column(String(3))

class Vliegtuigen(Base):
    __tablename__ = 'vliegtuigen'

    vliegtuigid = Column(Integer, primary_key=True)
    maatschappijid = Column(Integer, ForeignKey('maatschappijen.maatschappijid'))
    type = Column(String(50), nullable=False)
    bouwjaar = Column(Integer)

class Planning(Base):
    __tablename__ = 'planning'

    planningid = Column(Integer, primary_key=True)
    vluchtnummer = Column(String(10), nullable=False)
    maatschappijid = Column(Integer, ForeignKey('maatschappijen.maatschappijid'))
    bestemming = Column(String(3), nullable=False)
    terminal = Column(String(5))
    gate = Column(String(5))
    tijd = Column(TIMESTAMP)

class Vlucht(Base):
    __tablename__ = 'vlucht'

    vluchtid = Column(Integer, primary_key=True)
    planningid = Column(Integer, ForeignKey('planning.planningid'))
    vliegtuigid = Column(Integer, ForeignKey('vliegtuigen.vliegtuigid'))
    datum = Column(DATE)

class Weer(Base):
    __tablename__ = 'weer'

    weerid = Column(Integer, primary_key=True)
    datum = Column(DATE)
    windrichting = Column(Float)
    windsnelheid = Column(Float)
    temperatuur = Column(Float)
    neerslag = Column(Float)
    luchtdruk = Column(Float)

class Luchthavens(Base):
    __tablename__ = 'luchthavens'

    luchthavenid = Column(Integer, primary_key=True)
    naam = Column(String(100), nullable=False)
    iata = Column(String(3))
    icao = Column(String(4))
    land = Column(String(50))
    stad = Column(String(50))
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Integer)
    tz = Column(String(10))
    dst = Column(String(1))
    tzname = Column(String(50))

class Banen(Base):
    __tablename__ = 'banen'

    baanid = Column(Integer, primary_key=True)
    luchthavenid = Column(Integer, ForeignKey('luchthavens.luchthavenid'))
    nummer = Column(String(1), nullable=False)
    code = Column(String(7))
    naam = Column(String(100))
    lengte = Column(Integer)

class Aankomst(Base):
    __tablename__ = 'aankomst'

    aankomstid = Column(Integer, primary_key=True)
    vluchtid = Column(Integer, ForeignKey('vlucht.vluchtid'))
    baanid = Column(Integer, ForeignKey('banen.baanid'))
    bezetting = Column(Integer)
    vracht = Column(Integer)
    aankomsttijd = Column(TIMESTAMP)

class Vertrek(Base):
    __tablename__ = 'vertrek'

    vertrekid = Column(Integer, primary_key=True)
    vluchtid = Column(Integer, ForeignKey('vlucht.vluchtid'))
    baanid = Column(Integer, ForeignKey('banen.baanid'))
    bezetting = Column(Integer)
    vracht = Column(Integer)
    vertrektijd = Column(TIMESTAMP)

class Klant(Base):
    __tablename__ = 'klant'

    klantid = Column(Integer, primary_key=True)
    vluchtid = Column(Integer, ForeignKey('vlucht.vluchtid'))
    operatie = Column(Float)
    faciliteiten = Column(Float)
    shops = Column(Float)

engine = create_engine('postgresql://postgres:Newpassword@192.168.56.1:5433/postgres')
inspector = inspect(engine)

