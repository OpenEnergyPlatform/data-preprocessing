/*
Metadata for TSO Control Area
Review: https://github.com/OpenEnergyPlatform/data-preprocessing/issues/

__copyright__   = "none"
__license__     = "CC0 1.0 Universal Public Domain Dedication (CC0-1.0)"
__url__         = "https://creativecommons.org/publicdomain/zero/1.0/"
__author__      = "Tobias Schmid, Ludee"
*/


-- table
DROP TABLE IF EXISTS    boundaries.ffe_tso_controlarea;
CREATE TABLE            boundaries.ffe_tso_controlarea (
    id          bigint,
    version     text,
    vid         integer,
    plz         varchar(5),
    tso         text,
    geom        geometry(MultiPolygon,3035),
    CONSTRAINT ffe_tso_controlarea_pkey PRIMARY KEY (id) );

-- access rights
ALTER TABLE boundaries.ffe_tso_controlarea OWNER to oeuser;

-- index
CREATE INDEX ffe_tso_controlarea_geom_idx
    ON boundaries.ffe_tso_controlarea USING GIST (geom);

-- metadata
COMMENT ON TABLE boundaries.ffe_tso_controlarea IS '{
    "name": "ffe_tso_controlarea",
    "title": "",
    "id": "",
    "description": "",
    "language": [ "en-GB" ],
    "keywords": [ "" ],
    "publicationDate": "",
    "context":
        {"homepage": "",
        "documentation": "",
        "sourceCode": "",
        "contact": "",
        "grantNo": ""},
    "spatial":
        {"location": "",
        "extent": "",
        "resolution": ""},
    "temporal":
        {"referenceDate": "",
        "start": "",
        "end": "",
        "resolution": ""},
    "sources": [
        {"title": "", "description": "", "path": "https://", "license": "", "copyright": ""},
        {"title": "", "description": "", "path": "https://", "license": "", "copyright": ""} ],
    "licenses": [
        {"name": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0 International",
        "path": "https://creativecommons.org/licenses/by/4.0/legalcode",
        "instruction": "https://tldrlegal.com/license/creative-commons-attribution-4.0-international-(cc-by-4)",
        "attribution": "© CopyrightOwner"}],
    "contributors": [
        {"title": "", "email": "", "date": "", "object": "", "comment": ""},
        {"title": "", "email": "", "date": "", "object": "", "comment": ""} ],
    "resources": [
        {"profile": "tabular-data-resource",
        "name": "model_draft.ffe_tso_controlarea",
        "path": "https://github.com/OpenEnergyPlatform/examples/tree/master/metadata",
        "format": "PostgreSQL",
        "encoding" : "UTF-8",
        "schema": {
            "fields": [
                {"name": "id", "description": "Unique identifier", "type": "serial", "unit": "none"},
                {"name": "year", "description": "Reference year", "type": "integer", "unit": "none"},
                {"name": "value", "description": "Example value", "type": "double precision", "unit": "none"},
                {"name": "geom", "description": "Geometry", "type": "geometry(Point, 4326)", "unit": "none"} ],
            "primaryKey": "id",
            "foreignKeys": {"fields": "year",
                   "reference": {"ressource": "schema.table",
                   "fields": "year"} } },
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

-- scenario log (project,version,io,schema_name,table_name,script_name,comment)
SELECT scenario_log('OEP','data-review','input','boundaries','ffe_tso_controlarea','boundaries.ffe_tso_controlarea.sql','Update metadata');


-- import from model_draft
INSERT INTO boundaries.ffe_tso_controlarea(version,vid,plz,tso,geom)
    SELECT  'v1',
            id,
            plz,
            tso,
            geom
    FROM    model_draft.ffe_tso_controlarea
    ORDER BY id;
