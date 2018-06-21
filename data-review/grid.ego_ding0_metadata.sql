/*
Metadata for eGo DING0 data
Review: https://github.com/OpenEnergyPlatform/data-preprocessing/issues/7

__copyright__   = "none"
__license__     = "CC0 1.0 Universal Public Domain Dedication (CC0-1.0)"
__url__         = "https://creativecommons.org/publicdomain/zero/1.0/"
__author__      = "Ludee, boltbeard, jh-RLI"
*/


-- metadata
COMMENT ON TABLE grid.ego_ding0_hvmv_station IS '
    {"title": "DING0 - HVMV Station",
    "description": "DIstribution Network Generat0r - A tool to generate synthetic medium and low voltage power distribution grids based on open (or at least accessible) data.",
    "language": [ "eng", "ger" ],
    "spatial": 
        {"location": "none",
        "extent": "Germany",
        "resolution": "vector"},
    "temporal": 
        {"reference_date": "none",
        "start": "none",
        "end": "none",
        "resolution": "none"},
    "sources": [
        {"name": "", "description": "", "url": "", "license": "", "copyright": ""},
        {"name": "", "description": "", "url": "", "license": "", "copyright": ""},
        {"name": "", "description": "", "url": "", "license": "", "copyright": ""},
        {"name": "", "description": "", "url": "", "license": "", "copyright": ""},
        {"name": "", "description": "", "url": "", "license": "", "copyright": ""} ],
    "license": 
        {"id": "ODbL-1.0",
        "name": "Open Data Commons Open Database License 1.0",
        "version": "1.0",
        "url": "https://opendatacommons.org/licenses/odbl/1.0/",
        "instruction": "You are free: To Share, To Create, To Adapt; As long as you: Attribute, Share-Alike, Keep open!",
        "copyright": "© Reiner Lemoine Institut"},
    "contributors": [
        {"name": "Ludee", "email": "github.com/Ludee", "date": "2018-06-18", "comment": "Create metadata"},
        {"name": "", "email": "", "date": "", "comment": ""} ],
    "resources": [
        {"name": "grid.ego_ding0_hvmv_station",
        "format": "PostgreSQL",
        "fields": [
            {"name": "id", "description": "tba", "unit": "tba" },
            {"name": "run_id", "description": "tba", "unit": "tba" },
            {"name": "edge_name", "description": "tba", "unit": "tba" },
            {"name": "grid_id_db", "description": "tba", "unit": "tba" } ] } ],
            {"name": "node1", "description": "tba", "unit": "tba" },
            {"name": "node2", "description": "tba", "unit": "tba" },
            {"name": "type_kind", "description": "tba", "unit": "tba" },
            {"name": "type_name", "description": "tba", "unit": "tba" },
            {"name": "length", "description": "tba", "unit": "tba" },
            {"name": "U_n", "description": "tba", "unit": "tba" },
            {"name": "C", "description": "tba", "unit": "tba" },
            {"name": "L", "description": "tba", "unit": "tba" },
            {"name": "R", "description": "tba", "unit": "tba" },
            {"name": "I_max_th", "description": "tba", "unit": "tba" } ] } ],
    "metadata_version": "1.3",
    "_comment": {
        "_metadata_license": "Creative Commons Zero v1.0 Universal (CC0-1.0)",
        "_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "_additional_information": {
            "_dates": "Dates must follow the ISO8601 (JJJJ-MM-TT)",
            "_units": "Use a space between Numbers and units (100 m)",
            "_none": "If not applicable use 'none'"} } }';

-- scenario log (project,version,io,schema_name,table_name,script_name,comment)
SELECT scenario_log('OEP','data-review','setup','grid','ego_ding0_hvmv_station','grid.ego_ding0_metadata.sql','Update metadata');
