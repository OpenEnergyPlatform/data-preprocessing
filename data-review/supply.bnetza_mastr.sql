/*
Metadata for Bundesnetzagentur - Marktstammdatenregister
Review: https://github.com/OpenEnergyPlatform/data-preprocessing/issues/

__copyright__   = "none"
__license__     = "CC0 1.0 Universal Public Domain Dedication (CC0-1.0)"
__url__         = "https://creativecommons.org/publicdomain/zero/1.0/"
__author__      = "Ludee"
*/


-- table
DROP TABLE IF EXISTS    supply.bnetza_mastr_wind;
CREATE TABLE            supply.bnetza_mastr_wind (
    id          serial,
    version     text,
    mastr_nr    varchar(5),
    geom        geometry(MultiPolygon,3035),
    CONSTRAINT bnetza_mastr_wind_pkey PRIMARY KEY (id) );

-- access rights
ALTER TABLE supply.bnetza_mastr_wind OWNER to oeuser;

-- index
CREATE INDEX bnetza_mastr_wind_geom_idx
    ON supply.bnetza_mastr_wind USING GIST (geom);

-- metadata
COMMENT ON TABLE supply.bnetza_mastr_wind IS '{
    "title": "Bundesnetzagentur - Marktstammdatenregister - Stromerzeugungseinheiten Wind",
    "description": "Processed MaStR - Stromerzeugungseinheiten Wind",
    "language": [ "eng", "deu" ],
    "spatial": 
        {"location": "none",
        "extent": "Germany",
        "resolution": "vector"},
    "temporal": 
        {"reference_date": "2019-01-31",
        "start": "none",
        "end": "none",
        "resolution": "none"},
    "sources": [
        {"name": "Bundesnetzagentur - Marktstammdatenregister", 
            "description": "Das Marktstammdatenregister ist das Register für den deutschen Strom- und Gasmarkt. Es wird MaStR abgekürzt. Im MaStR sind vor allem die Stammdaten zu Strom- und Gaserzeugungsanlagen zu registrieren. Außerdem sind die Stammdaten von Marktakteuren wie Anlagenbetreibern, Netzbetreibern und Energielieferanten zu registrieren. Das MaStR wird von der Bundesnetzagentur geführt.", 
            "url": "https://www.marktstammdatenregister.de/MaStR/", 
            "license": "Datenlizenz Deutschland – Namensnennung – Version 2.0", 
            "copyright": "© Marktstammdatenregister 2019 | dl-de/by-2-0"},
        {"name": "RLI - open_MaStR", 
            "description": "Scripts to download, process and publish the MaStR data set", 
            "url": "https://github.com/OpenEnergyPlatform/data-preprocessing/", 
            "license": "GNU Affero General Public License Version 3 (AGPL-3.0)", 
            "copyright": "© Reiner Lemoine Institut"} ],
    "license": 
        {"id": "dl-de/by-2-0",
        "name": "Datenlizenz Deutschland – Namensnennung – Version 2.0",
        "version": "2.0",
        "url": "https://www.govdata.de/dl-de/by-2-0",
        "instruction": "Die bereitgestellten Daten und Metadaten dürfen für die kommerzielle und nicht kommerzielle Nutzung verwendet werden. Bei der Nutzung ist sicherzustellen, dass Angaben als Quellenvermerk enthalten sind.",
        "copyright": "© Marktstammdatenregister 2019 | dl-de/by-2-0"},
    "contributors": [
        {"name": "Ludee", "email": "none", "date": "2019-02-07", "comment": "Create metadata"} ],
    "resources": [
        {"name": "supply.bnetza_mastr_wind",
        "format": "PostgreSQL",
        "fields": [
            {"name": "id", "description": "Unique identifier", "unit": "none"},
            {"name": "version", "description": "Version identifier", "unit": "none"},
            {"name": "mastr_nr", "description": "MaStR Nummer", "unit": "none"},
            {"name": "geom", "description": "Generalized geometry", "unit": "none"} ] } ],
    "metadata_version": "1.3"}';

-- scenario log (project,version,io,schema_name,table_name,script_name,comment)
SELECT scenario_log('OEP','data-review','input','supply','bnetza_mastr_wind','supply.ffe_osm_nuts3.sql','Update metadata');


-- import from sandbox
INSERT INTO supply.bnetza_mastr_wind(version,mastr_nr,geom)
    SELECT  'v1.0',
            mastr_nr,
            ST_MULTI(geom)
    FROM    sandbox.osm_nuts3
    ORDER BY id;
