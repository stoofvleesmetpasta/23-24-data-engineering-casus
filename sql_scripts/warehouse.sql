-- Create schema
CREATE SCHEMA IF NOT EXISTS warehouse;

DROP TABLE IF EXISTS warehouse.vliegtuig_dim, warehouse.luchtvaartmaatschappijen_dim, warehouse.luchthavens_dim, warehouse.klanten_dim, warehouse.weer_dim, warehouse.vluchten_feit CASCADE;

-- Create table aircraft_dim (vliegtuig_dim)
CREATE TABLE warehouse.vliegtuig_dim (
    luchtvaartmaatschappij_code CHAR(3),
    vliegtuig_code VARCHAR(12),
    fabrikant VARCHAR(100),
    vliegtuigtype_naam VARCHAR(100),
    wakkerruimte_categorie CHAR(1),
    vliegtuig_nood VARCHAR(50),
    capaciteit INTEGER,
    vrachtcapaciteit INTEGER,
    bouwjaar INTEGER,
    PRIMARY KEY (vliegtuig_code)
);

-- Create table airlines_dim (luchtvaartmaatschappijen_dim)
CREATE TABLE warehouse.luchtvaartmaatschappijen_dim (
    luchtvaartmaatschappij_naam VARCHAR(100),
    iata_code VARCHAR(3),
    icao_code VARCHAR(4),
    luchtvaartmaatschappij_code CHAR(3),
    luchtvaartmaatschappij_id SERIAL PRIMARY KEY
);

-- Create table airports_dim (luchthavens_dim)
CREATE TABLE warehouse.luchthavens_dim (
    luchthaven_naam VARCHAR(100),
    land VARCHAR(60),
    stad VARCHAR(200),
    iata_code VARCHAR(4),
    icao_code VARCHAR(4),
    breedtegraad DOUBLE PRECISION,
    lengtegraad DOUBLE PRECISION,
    hoogte INTEGER,
    tijdzone VARCHAR(30),
    dst CHAR(1),
    luchthaven_id SERIAL PRIMARY KEY
);

-- Create table customer_dim (klanten_dim)
CREATE TABLE warehouse.klanten_dim (
    vlucht_id INTEGER,
    operationele_tevredeheid DOUBLE PRECISION,
    faciliteiten_tevredeheid DOUBLE PRECISION,
    winkels_tevredeheid DOUBLE PRECISION,
    klant_id SERIAL PRIMARY KEY
);

-- Create table weather_dim (weer_dim)
CREATE TABLE warehouse.weer_dim (
    observatie_datum DATE,
    wind_richting_graden INTEGER,
    gemiddelde_uurlijkse_windsnelheid INTEGER,
    gemiddelde_dagelijkse_windsnelheid INTEGER,
    maximale_uurlijkse_windsnelheid INTEGER,
    minimale_uurlijkse_windsnelheid INTEGER,
    maximale_uurlijkse_windsnelheid_tijd INTEGER,
    minimale_uurlijkse_windsnelheid_tijd INTEGER,
    maximale_windsnelheid INTEGER,
    minimale_windsnelheid INTEGER,
    gemiddelde_temperatuur DOUBLE PRECISION,
    maximale_temperatuur DOUBLE PRECISION,
    minimale_temperatuur DOUBLE PRECISION,
    maximale_temperatuur_tijd INTEGER,
    minimale_temperatuur_tijd INTEGER,
    zonneschijnduur_uren INTEGER,
    zonneschijn_percentage INTEGER,
    globale_straling INTEGER,
    neerslagduur_uren INTEGER,
    totale_neerslag INTEGER,
    maximale_uurlijkse_neerslag INTEGER,
    maximale_uurlijkse_neerslag_tijd INTEGER,
    gemiddelde_luchtdruk INTEGER,
    minimale_luchtdruk INTEGER,
    maximale_luchtdruk INTEGER,
    minimale_luchtdruk_tijd INTEGER,
    maximale_luchtdruk_tijd INTEGER,
    minimale_zichtbaarheid INTEGER,
    maximale_zichtbaarheid INTEGER,
    gemiddelde_zichtbaarheid INTEGER,
    gemiddelde_bewolking INTEGER,
    gemiddelde_relatieve_vochtigheid INTEGER,
    maximale_relatieve_vochtigheid INTEGER,
    minimale_relatieve_vochtigheid INTEGER,
    minimale_relatieve_vochtigheid_tijd INTEGER,
    maximale_relatieve_vochtigheid_tijd INTEGER,
    potentiele_verdamping INTEGER,
    weer_id SERIAL PRIMARY KEY
);

-- Create table flights_fact (vluchten_feit)
CREATE TABLE warehouse.vluchten_feit (
    vluchtnummer VARCHAR(20),
    luchtvaartmaatschappij_code CHAR(3),
    luchtvaartmaatschappij_id INTEGER,
    bestemmingscode VARCHAR(4),
    vliegtuig_code VARCHAR(12),
    bezetting INTEGER,
    vrachtcapaciteit INTEGER,
    aankomsttijd TIMESTAMP,
    vertrektijd TIMESTAMP,
    weer_id INTEGER,
    bestemming_luchthaven_id INTEGER,
    vlucht_id INTEGER PRIMARY KEY,
    FOREIGN KEY (vliegtuig_code) REFERENCES warehouse.vliegtuig_dim (vliegtuig_code),
    FOREIGN KEY (luchtvaartmaatschappij_id) REFERENCES warehouse.luchtvaartmaatschappijen_dim (luchtvaartmaatschappij_id),
    FOREIGN KEY (bestemming_luchthaven_id) REFERENCES warehouse.luchthavens_dim (luchthaven_id),
    FOREIGN KEY (weer_id) REFERENCES warehouse.weer_dim (weer_id)
);
