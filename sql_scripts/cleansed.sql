CREATE SCHEMA IF NOT EXISTS cleansed;

DROP TABLE IF EXISTS cleansed.aankomst, cleansed.banen, cleansed.klant, cleansed.luchthavens, cleansed.maatschappijen, cleansed.planning, cleansed.vertrek, cleansed.vliegtuig, cleansed.vliegtuigtype, cleansed.vlucht, cleansed.weer CASCADE;

CREATE TABLE cleansed.aankomst (
    "vluchtid" VARCHAR(10),
    "vliegtuigcode" VARCHAR(8),
    "terminal" CHAR(1),
    "gate" VARCHAR(2),
    "baan" CHAR(1),
    "bezetting" SMALLINT,
    "vracht" VARCHAR(3),
    "aankomsttijd" TIMESTAMP
);

CREATE TABLE cleansed.banen (
    "baannummer" CHAR(1),
    "code" VARCHAR(7),
    "naam" VARCHAR(30),
    "lengte" SMALLINT
);

CREATE TABLE cleansed.luchthavens (
    "airport" VARCHAR(70),
    "city" VARCHAR(200),
    "country" VARCHAR(60),
    "iata" CHAR(10),
    "icao" CHAR(10),
    "lat" FLOAT,
    "lon" FLOAT,
    "alt" SMALLINT,
    "tz" VARCHAR(10),
    "dst" CHAR(1),
    "tzname" VARCHAR(50)
);

CREATE TABLE cleansed.klant (
    "vluchtid" VARCHAR(7),        -- Behoud van de lengte maar als VARCHAR voor efficiëntie
    "operatie" DECIMAL(2,1),      -- Numeriek datatype voor waarden zoals '7.2' die een decimaal kunnen bevatten
    "faciliteiten" DECIMAL(2,1),  -- Eveneens numeriek datatype voor scores/waarden zoals '8.5'
    "shops" DECIMAL(2,1)          -- Numeriek datatype voor waarden zoals '6.9', mogelijk beoordelingen of scores
);

CREATE TABLE cleansed.maatschappijen (
    "name" VARCHAR(50),     -- Gebruik VARCHAR om ruimte te besparen wanneer namen korter zijn dan 50 karakters
    "iata" VARCHAR(3),      -- VARCHAR is geschikt omdat sommige IATA-codes speciale tekens kunnen bevatten
    "icao" VARCHAR(3)       -- VARCHAR wordt gebruikt omdat er inconsistente waarden zoals 'N/A' of '\N' kunnen voorkomen
);

CREATE TABLE cleansed.planning (
    "vluchtnr" VARCHAR(10),      -- Gebruik VARCHAR voor mogelijke variabiliteit in lengte
    "airlinecode" CHAR(10),      -- Behoud CHAR voor consistente, korte codes zoals '9W'
    "destcode" CHAR(5),         -- Behoud CHAR voor standaard IATA luchthaven codes
    "planterminal" CHAR(1),     -- Behoud CHAR voor enkel karakter waarden
    "plangate" VARCHAR(5),      -- Gebruik VARCHAR, kan efficiënter zijn afhankelijk van variatie
    "plantijd" TIME             -- Gebruik TIME datatype voor tijd, indien de tijd in 24-uurs notatie is
);

CREATE TABLE cleansed.vertrek (
    "vluchtid" VARCHAR(10),       -- VARCHAR wordt gebruikt voor flexibele opslag
    "vliegtuigcode" VARCHAR(8),  -- VARCHAR om ruimte te besparen, gezien lengtes kunnen variëren
    "terminal" CHAR(1),          -- Behoud van CHAR voor een enkel karakter
    "gate" VARCHAR(2),           -- VARCHAR voor mogelijke variatie in lengte
    "baan" CHAR(1),              -- Behoud van CHAR voor consistente, enkele karakteropslag
    "bezetting" SMALLINT,        -- SMALLINT voor numerieke gegevens die niet veel ruimte nodig hebben
    "vracht" VARCHAR(5),         -- Behoud van CHAR, hoewel lijkt dat er vaak geen data is
    "vertrektijd" TIMESTAMP      -- TIMESTAMP voor exacte datum en tijd opslag
);

CREATE TABLE cleansed.vliegtuig (
    "airlinecode" CHAR(3),
    "vliegtuigcode" VARCHAR(8),
    "vliegtuigtype" CHAR(3),
    "bouwjaar" INT       
);

CREATE TABLE cleansed.vliegtuigtype (
    "iata" VARCHAR(10),
    "icao" VARCHAR(10),
    "merk" VARCHAR(40),
    "type" VARCHAR(80),
    "wake" CHAR(1),
    "cat" CHAR(10),
    "capaciteit" INT,
    "vracht" INT    
);

CREATE TABLE cleansed.vlucht (
    "vluchtid" INT,
    "vluchtnr" VARCHAR(10),
    "airlinecode" CHAR(3),
    "destcode" CHAR(3),
    "vliegtuigcode" VARCHAR(10),
    "datum" DATE          
);

CREATE TABLE cleansed.weer (
    "datum" DATE,
    "ddvec" INT,
    "fhvec" INT,
    "fg" INT,
    "fhx" INT,
    "fhxh" INT,
    "fhn" INT,
    "fhnh" INT,
    "fxx" INT,
    "fxxh" INT,
    "tg" INT,
    "tn" INT,
    "tnh" INT,
    "tx" INT,
    "txh" INT,
    "t10n" INT,
    "t10nh" INT,
    "sq" INT,
    "sp" INT,
    "q" INT,
    "dr" INT,
    "rh" INT,
    "rhx" INT,
    "rhxh" INT,
    "pg" INT,
    "px" INT,
    "pxh" INT,
    "pn" INT,
    "pnh" INT,
    "vvn" INT,
    "vvnh" INT,
    "vvx" INT,
    "vvxh" INT,
    "ng" INT,
    "ug" INT,
    "ux" INT,
    "uxh" INT,
    "un" INT,
    "unh" INT,
    "ev2" INT      -- Potentiële verdamping (in 0.1 mm)
);


