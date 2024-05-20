

-- Maatschappijen
CREATE TABLE Maatschappijen (
    MaatschappijID SERIAL PRIMARY KEY,
    Naam VARCHAR(100) NOT NULL,
    IATA VARCHAR(3),
    ICAO VARCHAR(3)
);

-- Vliegtuigen
CREATE TABLE Vliegtuigen (
    VliegtuigID SERIAL PRIMARY KEY,
    MaatschappijID INT REFERENCES Maatschappijen(MaatschappijID),
    Type VARCHAR(50) NOT NULL,
    Bouwjaar INT
);

-- Planning
CREATE TABLE Planning (
    PlanningID SERIAL PRIMARY KEY,
    Vluchtnummer VARCHAR(10) NOT NULL,
    MaatschappijID INT REFERENCES Maatschappijen(MaatschappijID),
    Bestemming VARCHAR(3) NOT NULL,
    Terminal VARCHAR(5),
    Gate VARCHAR(5),
    Tijd TIMESTAMP
);

-- Vlucht
CREATE TABLE Vlucht (
    VluchtID SERIAL PRIMARY KEY,
    PlanningID INT REFERENCES Planning(PlanningID),
    VliegtuigID INT REFERENCES Vliegtuigen(VliegtuigID),
    Datum DATE
);

-- Weer
CREATE TABLE Weer (
    WeerID SERIAL PRIMARY KEY,
    Datum DATE,
    Windrichting DECIMAL(5,2),
    Windsnelheid DECIMAL(5,2),
    Temperatuur DECIMAL(5,2),
    Neerslag DECIMAL(5,2),
    Luchtdruk DECIMAL(5,2)
);

-- Luchthavens
CREATE TABLE Luchthavens (
    LuchthavenID SERIAL PRIMARY KEY,
    Naam VARCHAR(100) NOT NULL,
    IATA VARCHAR(3),
    ICAO VARCHAR(4),
    Land VARCHAR(50),
    Stad VARCHAR(50),
    Lat DECIMAL(9,6),
    Lon DECIMAL(9,6),
    Alt INT,
    TZ VARCHAR(10),
    DST CHAR(1),
    TZName VARCHAR(50)
);

-- Banen
CREATE TABLE Banen (
    BaanID SERIAL PRIMARY KEY,
    LuchthavenID INT REFERENCES Luchthavens(LuchthavenID),
    Nummer VARCHAR(1) NOT NULL,
    Code VARCHAR(7),
    Naam VARCHAR(100),
    Lengte INT
);

-- Aankomst
CREATE TABLE Aankomst (
    AankomstID SERIAL PRIMARY KEY,
    VluchtID INT REFERENCES Vlucht(VluchtID),
    BaanID INT REFERENCES Banen(BaanID),
    Bezetting INT,
    Vracht INT,
    AankomstTijd TIMESTAMP
);

-- Vertrek
CREATE TABLE Vertrek (
    VertrekID SERIAL PRIMARY KEY,
    VluchtID INT REFERENCES Vlucht(VluchtID),
    BaanID INT REFERENCES Banen(BaanID),
    Bezetting INT,
    Vracht INT,
    VertrekTijd TIMESTAMP
);

-- Klant
CREATE TABLE Klant (
    KlantID SERIAL PRIMARY KEY,
    VluchtID INT REFERENCES Vlucht(VluchtID),
    Operatie DECIMAL(5,2),
    Faciliteiten DECIMAL(5,2),
    Shops DECIMAL(5,2)
);
