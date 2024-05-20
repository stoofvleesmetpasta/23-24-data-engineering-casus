-- Maatschappijen
CREATE TABLE Maatschappijen (
    "maatschappijid" SERIAL PRIMARY KEY,
    "naam" VARCHAR(100) NOT NULL,
    "iata" VARCHAR(3),
    "icao" VARCHAR(3)
);

-- Vliegtuigen
CREATE TABLE Vliegtuigen (
    "vliegtuigid" SERIAL PRIMARY KEY,
    "maatschappijid" INT REFERENCES Maatschappijen("maatschappijid"),
    "type" VARCHAR(50) NOT NULL,
    "bouwjaar" INT
);

-- Planning
CREATE TABLE Planning (
    "planningid" SERIAL PRIMARY KEY,
    "vluchtnummer" VARCHAR(10) NOT NULL,
    "maatschappijid" INT REFERENCES Maatschappijen("maatschappijid"),
    "bestemming" VARCHAR(3) NOT NULL,
    "terminal" VARCHAR(5),
    "gate" VARCHAR(5),
    "tijd" TIMESTAMP
);

-- Vlucht
CREATE TABLE Vlucht (
    "vluchtid" SERIAL PRIMARY KEY,
    "planningid" INT REFERENCES Planning("planningid"),
    "vliegtuigid" INT REFERENCES Vliegtuigen("vliegtuigid"),
    "datum" DATE
);

-- Weer
CREATE TABLE Weer (
    "weerid" SERIAL PRIMARY KEY,
    "datum" DATE,
    "windrichting" DECIMAL(5,2),
    "windsnelheid" DECIMAL(5,2),
    "temperatuur" DECIMAL(5,2),
    "neerslag" DECIMAL(5,2),
    "luchtdruk" DECIMAL(5,2)
);

-- Luchthavens
CREATE TABLE Luchthavens (
    "luchthavenid" SERIAL PRIMARY KEY,
    "naam" VARCHAR(100) NOT NULL,
    "iata" VARCHAR(3),
    "icao" VARCHAR(4),
    "land" VARCHAR(50),
    "stad" VARCHAR(50),
    "lat" DECIMAL(9,6),
    "lon" DECIMAL(9,6),
    "alt" INT,
    "tz" VARCHAR(10),
    "dst" CHAR(1),
    "tzname" VARCHAR(50)
);

-- Banen
CREATE TABLE Banen (
    "baanid" SERIAL PRIMARY KEY,
    "luchthavenid" INT REFERENCES Luchthavens("luchthavenid"),
    "nummer" VARCHAR(1) NOT NULL,
    "code" VARCHAR(7),
    "naam" VARCHAR(100),
    "lengte" INT
);

-- Aankomst
CREATE TABLE Aankomst (
    "aankomstid" SERIAL PRIMARY KEY,
    "vluchtid" INT REFERENCES Vlucht("vluchtid"),
    "baanid" INT REFERENCES Banen("baanid"),
    "bezetting" INT,
    "vracht" INT,
    "aankomsttijd" TIMESTAMP
);

-- Vertrek
CREATE TABLE Vertrek (
    "vertrekid" SERIAL PRIMARY KEY,
    "vluchtid" INT REFERENCES Vlucht("vluchtid"),
    "baanid" INT REFERENCES Banen("baanid"),
    "bezetting" INT,
    "vracht" INT,
    "vertrektijd" TIMESTAMP
);

-- Klant
CREATE TABLE Klant (
    "klantid" SERIAL PRIMARY KEY,
    "vluchtid" INT REFERENCES Vlucht("vluchtid"),
    "operatie" DECIMAL(5,2),
    "faciliteiten" DECIMAL(5,2),
    "shops" DECIMAL(5,2)
);
