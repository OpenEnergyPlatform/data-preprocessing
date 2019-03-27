/*
Lattice (regular point grid) with 30m
Lattice on bounding box of Germany.

__copyright__   = "Reiner Lemoine Institut"
__license__     = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__         = "https://github.com/OpenEnergyPlatform/data-preprocessing/blob/master/LICENSE"
__author__      = "Ludee"
*/

-- table for lattice 30m
DROP TABLE IF EXISTS    model_draft.oep_deu_lattice_30m CASCADE;
CREATE TABLE            model_draft.oep_deu_lattice_30m (
    id SERIAL NOT NULL,
    geom_box geometry(Polygon,3035),
    geom geometry(Point,3035),
CONSTRAINT 	oep_deu_lattice_30m_pkey PRIMARY KEY (id));

-- scenario log (project,version,io,schema_name,table_name,script_name,comment)
SELECT scenario_log('OEP', 'v0.1','input','boundaries','bkg_vg250_1_sta_union_mview','oep_deu_lattice_30m.sql',' ');

-- insert lattice
INSERT INTO     model_draft.oep_deu_lattice_30m (geom_box)
    SELECT  ST_SETSRID(ST_CREATEFISHNET(
            ROUND((ST_ymax(box2d(geom)) - ST_ymin(box2d(geom))) /30)::integer,
            ROUND((ST_xmax(box2d(geom)) - ST_xmin(box2d(geom))) /30)::integer,
            30,
            30,
            ST_xmin (box2d(geom)),
            ST_ymin (box2d(geom))
        ),3035)::geometry(POLYGON,3035) AS geom
    FROM boundaries.bkg_vg250_1_sta_union_mview;

-- index gist (geom_box)
CREATE INDEX oep_deu_lattice_30m_geom_box_idx
    ON model_draft.oep_deu_lattice_30m USING gist (geom_box);

-- centroid
UPDATE model_draft.oep_deu_lattice_30m
    SET geom = ST_CENTROID(geom_box);

-- index gist (geom)
CREATE INDEX oep_deu_lattice_30m_geom_idx
    ON model_draft.oep_deu_lattice_30m USING gist (geom);

-- grant (oeuser)
ALTER TABLE model_draft.oep_deu_lattice_30m OWNER TO oeuser;

-- metadata
COMMENT ON TABLE model_draft.oep_deu_lattice_30m IS '{
    "comment": "OEP - Temporary table",
    "version": "v0.1" }';

-- scenario log (project,version,io,schema_name,table_name,script_name,comment)
SELECT scenario_log('OEP', 'v0.1','output','model_draft','oep_deu_lattice_30m','oep_deu_lattice_30m.sql',' ');
