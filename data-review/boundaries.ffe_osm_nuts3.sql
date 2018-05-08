/*
Metadata for OSM NUTS-3 regions 2013

__copyright__   = "none"
__license__     = "CC0 1.0 Universal Public Domain Dedication (CC0-1.0)"
__url__         = "https://creativecommons.org/publicdomain/zero/1.0/"
__author__      = "Claudia Konetschny, Ludee"
*/


-- table
DROP TABLE IF EXISTS    boundaries.ffe_osm_nut3;
CREATE TABLE            boundaries.ffe_osm_nut3 (
    id          serial,
    version     text,
    nuts_code   varchar(5),
    geom        geometry(MultiPolygon,3035),
    CONSTRAINT ffe_osm_nut3_pkey PRIMARY KEY (id) );

-- access rights
ALTER TABLE boundaries.ffe_osm_nut3 OWNER to oeuser;

-- index
CREATE INDEX ffe_osm_nut3_geom_idx
    ON boundaries.ffe_osm_nut3 USING GIST (geom);

-- metadata
COMMENT ON TABLE boundaries.ffe_osm_nut3 IS '{
    "title": "NUTS-3 regions 2013 (generalized)",
    "description": "NUTS (Nomenclature des unités territoriales statistiques) is a uniform hierarchical nomenclature of spatial reference units in Europe used in official statistics. They are often oriented on administration units. This data set shows the NUTS-3 level for the year 2013.",
    "language": [ "eng", "deu" ],
    "spatial": 
        {"location": "none",
        "extent": "Europe",
        "resolution": "vector"},
    "temporal": 
        {"reference_date": "2013-12-31",
        "start": "none",
        "end": "none",
        "resolution": "none"},
    "sources": [
        {"name": "Geofabrik - Download OpenStreetMap Data Extracts (Europe)", 
            "description": "Web page for downloading OpenStreetMap Data", 
            "url": "https://download.geofabrik.de/europe.html", 
            "license": "Open Data Commons Open Database License 1.0 (ODbL-1.0)", 
            "copyright": "© 2016 Geofabrik GmbH and OpenStreetMap Contributors"},
        {"name": "Bundesamt für Kartographie und Geodäsie - Verwaltungsgebiete 1:250.000 - Stand 01.01.2016", 
            "description": "Der Datenbestand umfasst sämtliche Verwaltungseinheiten aller hierarchischen Verwaltungsebenen vom Staat bis zu den Gemeinden mit ihren Verwaltungsgrenzen, statistischen Schlüsselzahlen und dem Namen der Verwaltungseinheit sowie der spezifischen Bezeichnung der Verwaltungsebene des jeweiligen Bundeslandes. Die Geometrie der Grenzen ist hinsichtlich Genauigkeit und Auflösung auf das DLM250 ausgerichtet.", 
            "url": "http://www.geodatenzentrum.de/geodaten/gdz_rahmen.gdz_div?gdz_spr=deu&gdz_akt_zeile=5&gdz_anz_zeile=1&gdz_unt_zeile=13&gdz_user_id=0", 
            "license": "Geodatenzugangsgesetz (GeoZG), GeoNutzV: Verordnung zur Festlegung der Nutzungsbestimmungen für die Bereitstellung von Geodaten des Bundes vom 19. März 2013 (Bundesgesetzblatt Jahrgang 2013 Teil I Nr. 14)", 
            "copyright": "© GeoBasis-DE / BKG 2016"} ],
    "license": 
        {"id": "ODbL-1.0",
        "name": "Open Data Commons Open Database Lizenz 1.0",
        "version": "1.0",
        "url": "https://opendatacommons.org/licenses/odbl/1.0/",
        "instruction": "In addition to the copyright of the Forschungsstelle für Energiewirtschaft e.V. (FfE) (www.ffe.de), the following sources must be cited: © OpenStreetMap-Mitwirkende (https://www.openstreetmap.org/copyright), © GeoBasis-DE / BKG 2016 Daten verändert",
        "copyright": "© FfE"},
    "contributors": [
        {"name": "Claudia Konetschny", "email": "CKonetschny@ffe.de", "date": "2018-05-01", "comment": "Upload data and metadata"},
        {"name": "Michael Ebner", "email": "MEbner@ffe.de", "date": "2018-04-27", "comment": "none"},
        {"name": "Tobias Schmid", "email": "TSchmid@ffe.de", "date": "2018-04-27", "comment": "none"},
        {"name": "Fabian Jetter", "email": "FJetter@ffe.de", "date": "2018-04-27", "comment": "none"},
        {"name": "Ludee", "email": "none", "date": "2018-04-30", "comment": "Review and correct metadata"},
        {"name": "Ludee", "email": "none", "date": "2018-05-08", "comment": "Review and correct table structure"} ],
    "resources": [
        {"name": "boundaries.ffe_osm_nut3",
        "format": "PostgreSQL",
        "fields": [
            {"name": "id", "description": "Unique identifier", "unit": "none"},
            {"name": "version", "description": "Version identifier", "unit": "none"},
            {"name": "nuts_code", "description": "NUTS-3 Code: 5-digits, depending on higher NUTS levels (example: DE212)", "unit": "none"},
            {"name": "geom", "description": "Generalisierte Geometrie", "unit": "none"} ] } ],
    "metadata_version": "1.3"}';

-- scenario log (project,version,io,schema_name,table_name,script_name,comment)
SELECT scenario_log('OEP','data-review','input','boundaries','ffe_osm_nut3','boundaries.ffe_osm_nuts3.sql','Test metadata string');



-- import from sandbox
INSERT INTO boundaries.ffe_osm_nut3(version,nuts_code,geom)
    SELECT  'v1',
            nuts_code,
            ST_MULTI(geom)
    FROM    sandbox.osm_nuts3
    ORDER BY id;
    