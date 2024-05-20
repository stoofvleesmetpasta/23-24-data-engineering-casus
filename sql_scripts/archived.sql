-- Schema aanmaken indien het nog niet bestaat
CREATE SCHEMA IF NOT EXISTS archived;

-- Tabellen verwijderen indien ze bestaan
DROP TABLE IF EXISTS archived.aankomst, archived.banen, archived.klant, archived.luchthavens, archived.maatschappijen, archived.planning, archived.vertrek, archived.vliegtuig, archived.vliegtuigtype, archived.vlucht, archived.weer CASCADE;


CREATE TABLE archived.aankomst (
    "vluchtid" VARCHAR(10),        -- 6 karakters lang, gebaseerd op de langste waarde 936013
    "vliegtuigcode" VARCHAR(8),    -- 6 karakters lang, zoals VKL859
    "terminal" VARCHAR(1),         -- 1 karakter lang, zoals A, B, C
    "gate" VARCHAR(2),             -- 2 karakters lang, zoals C1, A2
    "baan" VARCHAR(1),             -- 1 karakter lang, voor de baan nummers
    "bezetting" VARCHAR(3),        -- Maximaal 3 karakters, voor getallen zoals 71
    "vracht" VARCHAR(3),           -- Lijkt leeg te zijn in de dataset, maar reserveer 1 karakter voor consistentie
    "aankomsttijd" VARCHAR(19)     -- Datum en tijd in het formaat "YYYY-MM-DD HH:MM:SS"
);

CREATE TABLE archived.banen (
    "baannummer" VARCHAR(1),      -- 1 karakter lang, voor baannummers 1-6
    "code" VARCHAR(7),            -- 7 karakters lang, zoals '18R-36L'
    "naam" VARCHAR(30),           -- Geschatte lengte voor namen zoals 'Stépan Breedveldbaan'
    "lengte" VARCHAR(4)           -- 4 karakters lang, voldoende voor getallen zoals 3600
);

CREATE TABLE archived.klant (
    "vluchtid" VARCHAR(7),      -- 7 karakters lang, gebaseerd op de langste waarde 1317406
    "operatie" VARCHAR(3),      -- 3 karakters lang, bijv. '7.2'
    "faciliteiten" VARCHAR(3),  -- 3 karakters lang, bijv. '8.5'
    "shops" VARCHAR(3)          -- 3 karakters lang, maximaal nodig voor getallen zoals '6.9'
);

CREATE TABLE archived.luchthavens (
    "airport" VARCHAR(70),     -- Geschatte lengte voor namen zoals 'Bamyan Airport'
    "city" VARCHAR(200),        -- Geschatte lengte voor stadsnamen zoals 'Bamyan'
    "country" VARCHAR(60),     -- Geschatte lengte voor landnamen zoals 'Afghanistan'
    "iata" VARCHAR(10),         -- 3 karakters, bijv. 'BIN'
    "icao" VARCHAR(10),         -- 4 karakters, bijv. 'OABN'
    "lat" VARCHAR(20),         -- Lengte voor breedtegraden zoals '34.816667'
    "lon" VARCHAR(20),         -- Lengte voor lengtegraden zoals '67.816667'
    "alt" VARCHAR(10),          -- 4 karakters voor hoogte zoals '2550'
    "tz" VARCHAR(10),           -- 4 karakters voor tijdzone offset zoals '4.5'
    "dst" VARCHAR(5),          -- 1 karakter voor DST, bijv. 'N'
    "tzname" VARCHAR(50)           -- Geschatte lengte voor tijdzone namen zoals 'Asia/Kabul'
);

CREATE TABLE archived.maatschappijen (
    "name" VARCHAR(50),     -- Voldoende lengte om namen zoals "Tom's & co airliners" te bevatten
    "iata" VARCHAR(3),      -- 3 karakters, rekening houdend met bijzondere invoeren zoals '&T'
    "icao" VARCHAR(3)       -- 3 karakters, voor standaard ICAO codes, zelfs met invoeren zoals 'N/A' of '\N'
);

CREATE TABLE archived.planning (
    "vluchtnr" VARCHAR(10),      -- 6 karakters lang, genoeg voor waarden zoals '9W2888'
    "airlinecode" VARCHAR(10),   -- 2 karakters lang, zoals '9W'
    "destcode" VARCHAR(10),      -- 3 karakters, standaard IATA luchthaven codes zoals 'DEL'
    "planterminal" VARCHAR(5),  -- 1 karakter, zoals 'D'
    "plangate" VARCHAR(5),      -- 2 karakters, zoals 'D2'
    "plantijd" VARCHAR(10)       -- 8 karakters, ruimte voor tijden zoals '2:10 PM'
);

CREATE TABLE archived.vertrek (
    "vluchtid" VARCHAR(10),       -- 6 karakters lang, gebaseerd op de langste waarde zoals '935995'
    "vliegtuigcode" VARCHAR(20),  -- 7 karakters lang, zoals 'VEZY741'
    "terminal" VARCHAR(5),       -- 1 karakter lang, zoals 'B'
    "gate" VARCHAR(5),           -- 2 karakters lang, zoals 'B5'
    "baan" VARCHAR(5),           -- 1 karakter lang, voor baan nummers zoals '2'
    "bezetting" VARCHAR(10),      -- Maximaal 3 karakters, voor getallen zoals '85'
    "vracht" VARCHAR(5),         -- 1 karakter lang, lijkt leeg te zijn in de dataset maar voor consistentie
    "vertrektijd" VARCHAR(25)    -- Datum en tijd in het formaat "YYYY-MM-DD HH:MM:SS", zoals '2014-01-01 03:33:00'
);

CREATE TABLE archived.vliegtuig (
    "airlinecode" VARCHAR(10),     -- 2 karakters lang, zoals 'TK'
    "vliegtuigcode" VARCHAR(20),   -- 7 karakters lang, zoals 'VDL5829'
    "vliegtuigtype" VARCHAR(10),   -- 3 karakters lang, voor typeaanduidingen zoals '321'
    "bouwjaar" VARCHAR(10)         -- 4 karakters lang, voor het bouwjaar zoals '1970'
);

CREATE TABLE archived.vliegtuigtype (
    "iata" VARCHAR(10),        -- 3 karakters lang, zoals '100'
    "icao" VARCHAR(10),        -- 4 karakters lang, zoals 'F100'
    "merk" VARCHAR(50),       -- Geschatte lengte voor merknamen zoals 'British Aerospace'
    "type" VARCHAR(100),       -- Geschatte lengte voor types zoals 'BAe 146-200 Pax'
    "wake" VARCHAR(10),        -- 1 karakter, categorie van de wake turbulence, zoals 'M'
    "cat" VARCHAR(10),         -- 3 karakters, categorie van het vliegtuiggebruik, zoals 'Pax'
    "capaciteit" VARCHAR(10),  -- 3 karakters, voor capaciteit zoals '115'
    "vracht" VARCHAR(10)       -- Voldoende voor kleine getallen zoals '5'
);

CREATE TABLE archived.vlucht (
    "vluchtid" VARCHAR(10),        -- 6 karakters lang, zoals '935995'
    "vluchtnr" VARCHAR(10),        -- 6 karakters lang, zoals 'EZY741'
    "airlinecode" VARCHAR(10),     -- 3 karakters lang, zoals 'EZY'
    "destcode" VARCHAR(10),        -- 3 karakters, voor luchthavencodes zoals 'ACE'
    "vliegtuigcode" VARCHAR(20),   -- 7 karakters lang, zoals 'VEZY741'
    "datum" VARCHAR(10)           -- Datum in het formaat "YYYY-MM-DD", zoals '2014-01-01'
);

CREATE TABLE archived.weer (
    "datum" VARCHAR(10),     -- Datum in het formaat "YYYY-MM-DD"
    "ddvec" VARCHAR(3),      -- Windrichting in graden
    "fhvec" VARCHAR(3),      -- Uurgemiddelde windsnelheid (in 0.1 m/s)
    "fg" VARCHAR(3),         -- Daggemiddelde windsnelheid (in 0.1 m/s)
    "fhx" VARCHAR(3),        -- Maximale uurgemiddelde windsnelheid (in 0.1 m/s)
    "fhxh" VARCHAR(2),       -- Uurvak van maximale uurgemiddelde windsnelheid
    "fhn" VARCHAR(3),        -- Minimale uurgemiddelde windsnelheid (in 0.1 m/s)
    "fhnh" VARCHAR(2),       -- Uurvak van minimale uurgemiddelde windsnelheid
    "fxx" VARCHAR(3),        -- Maximale windstoot (in 0.1 m/s)
    "fxxh" VARCHAR(2),       -- Uurvak van maximale windstoot
    "tg" VARCHAR(4),         -- Daggemiddelde temperatuur (in 0.1 graden Celsius)
    "tn" VARCHAR(4),         -- Minimum temperatuur (in 0.1 graden Celsius)
    "tnh" VARCHAR(2),        -- Tijdvak van minimum temperatuur
    "tx" VARCHAR(4),         -- Maximum temperatuur (in 0.1 graden Celsius)
    "txh" VARCHAR(2),        -- Tijdvak van maximum temperatuur
    "t10n" VARCHAR(4),       -- Minimum temperatuur op 10 cm hoogte (in 0.1 graden Celsius)
    "t10nh" VARCHAR(2),      -- Tijdvak van minimum temperatuur op 10 cm hoogte
    "sq" VARCHAR(3),         -- Zonneschijnduur (in 0.1 uur) berekend uit globale straling
    "sp" VARCHAR(3),         -- Percentage van de langst mogelijke zonneschijnduur
    "q" VARCHAR(4),          -- Globale straling (in J/cm2)
    "dr" VARCHAR(3),         -- Duur van de neerslag (in 0.1 uur)
    "rh" VARCHAR(4),         -- Neerslaghoeveelheid (in 0.1 mm)
    "rhx" VARCHAR(4),        -- Maximum uur-neerslaghoeveelheid (in 0.1 mm)
    "rhxh" VARCHAR(2),       -- Uurvak van maximum uur-neerslaghoeveelheid
    "pg" VARCHAR(5),         -- Daggemiddelde luchtdruk (in 0.1 hPa)
    "px" VARCHAR(5),         -- Maximum luchtdruk (in 0.1 hPa)
    "pxh" VARCHAR(2),        -- Uurvak van maximum luchtdruk
    "pn" VARCHAR(5),         -- Minimum luchtdruk (in 0.1 hPa)
    "pnh" VARCHAR(2),        -- Uurvak van minimum luchtdruk
    "vvn" VARCHAR(3),        -- Minimum zicht
    "vvnh" VARCHAR(2),       -- Uurvak van minimum zicht
    "vvx" VARCHAR(3),        -- Maximum zicht
    "vvxh" VARCHAR(2),       -- Uurvak van maximum zicht
    "ng" VARCHAR(2),         -- Gemiddelde bewolking (in achtsten, van 0 tot 9)
    "ug" VARCHAR(3),         -- Gemiddelde relatieve vochtigheid (in procenten)
    "ux" VARCHAR(3),         -- Maximum relatieve vochtigheid (in procenten)
    "uxh" VARCHAR(2),        -- Uurvak van maximum relatieve vochtigheid
    "un" VARCHAR(3),         -- Minimum relatieve vochtigheid (in procenten)
    "unh" VARCHAR(2),        -- Uurvak van minimum relatieve vochtigheid
    "ev2" VARCHAR(4)         -- Potentiële verdamping (in 0.1 mm)
);