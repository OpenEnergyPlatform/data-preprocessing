/*
RLI DIBt Windzones Grouping

__copyright__   = "© Reiner Lemoine Institut"
__license__     = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__         = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__      = "Ludwig Hülk"

*/


-- DIBt Windzone
DROP TABLE IF EXISTS    climate.rli_dibt_windzone;
CREATE TABLE            climate.rli_dibt_windzone (
    id              serial,
    version         text,
    vg_version      text,
    dibt_wind_zone  integer,
    v_ref           double precision,
    geom            geometry(MultiPolygon,31467),
    CONSTRAINT rli_dibt_windzone_pkey PRIMARY KEY (id,version));
    
-- access rights
ALTER TABLE climate.rli_dibt_windzone OWNER TO oeuser;

-- index
CREATE INDEX rli_dibt_windzone_geom_idx
    ON climate.rli_dibt_windzone USING gist (geom);

-- merge windzones
INSERT INTO	model_draft.rli_dibt_windzone (version,vg_version,dibt_wind_zone,geom)
	SELECT	'0.1' AS version,
            '2016-01-01' AS vg_version, -- reference_date
            dibt_wind_zone,
            (ST_DUMP(ST_MULTI(ST_BUFFER(ST_UNION(ST_BUFFER(geom, 1)),-1)))).geom ::geometry(Polygon,31467) AS geom
	FROM	model_draft.rli_dibt_windzone_vg
    GROUP BY dibt_wind_zone
    ORDER BY dibt_wind_zone;


-- metadata
COMMENT ON TABLE model_draft.rli_dibt_windzone IS '
{"name": "rli_dibt_windzone",
"title": "Windzone map for Germany",
"id": "model_draft.rli_dibt_windzone",
"description": "",
"language": [ "de-DE; en-GB" ],
"keywords": [ "wind, climate" ],
"publicationDate": "2019-03-21",
"context":
    {"homepage": "https://reiner-lemoine-institut.de/open_fred-open-feed-time-series-based-renewable-energy-database/",
    "documentation": "none",
    "sourceCode": "tba",
    "contact": "none",
    "grantNo": "0324006A"},
"spatial":
    {"location": "none",
    "extent": "Germany",
    "resolution": "vector"},
"temporal":
    {"referenceDate": "2018-09-27",
    "start": "none",
    "end": "none",
    "resolution": "none"},
"sources": [
    {"title": "Zuordnung der Windzonen nach Verwaltungsgrenzen", "description": "Stand: 27. September 2018 ", "path": "https://www.dibt.de/fileadmin/dibt-website/Dokumente/Referat/P5/Technische_Bestimmungen/Windzonen_Formular_nach_Verwaltungsgrenzen.xlsx", "license": "none", "copyright": "none"},
    {"title": "BKG - Verwaltungsgebiete 1:250.000 - Gemeinden (GEM)", "description": "Der Datenbestand umfasst die Verwaltungseinheiten der hierarchischen Verwaltungsebenen vom Staat bis zu den Gemeinden", "path": "boundaries.bkg_vg250_6_gem", "license": "Gesetz über den Zugang zu digitalen Geodaten (Geodatenzugangsgesetz - GeoZG)", "copyright": "© GeoBasis-DE / BKG 2016 (Daten verändert)"},
    {"title": "Windenergie-im-Binnenland", "description": "Online Windzonenrechner für DIBt 2012 und DIN EN 1991-1-4/NA", "path": "http://www.windenergie-im-binnenland.de/windzonenrechner.php", "license": "none", "copyright": "none"} ],
"licenses": [
    {"name": "CC-BY-4.0",
    "title": "Creative Commons Attribution 4.0 International",
    "path": "https://creativecommons.org/licenses/by/4.0/legalcode",
    "instruction": "https://tldrlegal.com/license/creative-commons-attribution-4.0-international-(cc-by-4)",
    "attribution": "© Reiner Lemoine Institut"}],
"contributors": [
    {"title": "Ludee", "email": "none", "date": "2019-03-21", "object": "data", "comment": "Create data"},
    {"title": "Ludee", "email": "none", "date": "2019-03-21", "object": "metadata", "comment": "create metadata"}],
"resources": [
    {"profile": "tabular-data-resource",
    "name": "model_draft.rli_dibt_windzone",
    "path": "http://openenergy-platform.org/dataedit/view/model_draft/rli_dibt_windzone",
    "format": "PostgreSQL",
    "encoding" : "UTF-8",
    "schema": {
        "fields": [
            {"name": "id", "description": "Unique identifier", "type": "serial", "unit": "none"},
            {"name": "version", "description": "Version number", "type": "text", "unit": "none"},
            {"name": "vg_version", "description": "Version from vg250 (reference_date)", "type": "text", "unit": "none"},
            {"name": "rli_dibt_windzone", "description": "Windzone number", "type": "integer", "unit": "none"},
            {"name": "v_ref", "description": "Reference wind speed", "type": "double precision", "unit": "m/s"},
            {"name": "geom", "description": "Geometry", "type": "geometry(MultiPolygon, 31467)", "unit": "none"} ],
        "primaryKey": ["id", "version"]},
    "dialect":
        {"delimiter": "none",
        "decimalSeparator": "."} } ],
"review": {
    "path": "none",
    "badge": "none"},
"metaMetadata":
    {"metadataVersion": "OEP-1.4",
    "metadataLicense":
        {"name": "CC0-1.0",
        "title": "Creative Commons Zero v1.0 Universal",
        "path": "https://creativecommons.org/publicdomain/zero/1.0/"}},
"_comment":
    {"metadata": "Metadata documentation and explanation (https://github.com/OpenEnergyPlatform/organisation/wiki/metadata)",
    "dates": "Dates and time must follow the ISO8601 including time zone (YYYY-MM-DD or YYYY-MM-DDThh:mm:ss±hh)",
    "units": "Use a space between numbers and units (100 m)",
    "languages": "Languages must follow the IETF (BCP47) format (en-GB, en-US, de-DE)",
    "licenses": "License name must follow the SPDX License List (https://spdx.org/licenses/)",
    "review": "Following the OEP Data Review (https://github.com/OpenEnergyPlatform/data-preprocessing/wiki)",
    "none": "If not applicable use (none)"}}';
