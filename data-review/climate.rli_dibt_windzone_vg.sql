/*
DIBT Windzones per Administrative Area

__copyright__   = "© Reiner Lemoine Institut"
__license__     = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__url__         = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__      = "Ludwig Hülk"

 * This file is part of project open_FRED (https://github.com/open-fred/db).
 * It's copyrighted by the contributors recorded in the version control history:
 * dataprocessing/windpowerlib/bnetza_eeg_anlagenstammdaten_wind_analyse.sql
 * 
 * SPDX-License-Identifier: AGPL-3.0-or-later
*/


WITH    w AS (
        SELECT EXTRACT(YEAR FROM "4.3_tatsächliche_inbetriebnahme") AS start_year
        FROM model_draft.bnetza_eeg_anlagenstammdaten_wind_classification
        WHERE "meldegrund" = 'Inbetriebnahme' AND
              "4.3_tatsächliche_inbetriebnahme" IS NOT NULL)
SELECT  *,
        w.start_year
FROM    w,
        model_draft.bnetza_eeg_anlagenstammdaten_wind_classification;
        
        
SELECT  wind_class_iec, COUNT(*) AS cnt
FROM    model_draft.openfred_windpower_powercurve
GROUP BY wind_class_iec
ORDER BY COUNT(*) DESC;

SELECT  wind_zone_dibt, COUNT(*) AS cnt
FROM    model_draft.openfred_windpower_powercurve
GROUP BY wind_zone_dibt
ORDER BY COUNT(*) DESC;








-- DIBT Windzone VG
DROP TABLE IF EXISTS    model_draft.rli_dibt_windzone_vg;
CREATE TABLE            model_draft.rli_dibt_windzone_vg (
    id              serial,
    gen             character varying(50),
    ags_0           character varying(12),
    nuts            character varying(5),
    dibt_wind_zone  integer,
    geom            geometry(MultiPolygon,31467),
    CONSTRAINT rli_dibt_windzone_vg_pkey PRIMARY KEY (id));
    
-- access rights
ALTER TABLE model_draft.rli_dibt_windzone_vg OWNER TO oeuser;

-- index
CREATE INDEX rli_dibt_windzone_vg_geom_idx
    ON model_draft.rli_dibt_windzone_vg USING gist (geom);


-- insert Gemeinden
INSERT INTO model_draft.rli_dibt_windzone_vg (gen,ags_0,geom)
    SELECT  gen,
            ags_0,
            geom
    FROM    boundaries.bkg_vg250_6_gem
    ORDER BY ags_0;

    
    
-- SH

-- Kreis Schleswig-Flensburg, kreisfreie Stadt Flensburg
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 4
    WHERE   gen IN ('Wohlde', 'Bergenhusen', 'Norderstapel', 
                'Süderstapel', 'Erfde', 'Meggerdorf', 'Tielen') AND 
            dibt_wind_zone IS NULL;
    
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 3
    WHERE   (LEFT(ags_0,5) = '01059' OR 
                ags_0 = '01001000') AND
            dibt_wind_zone IS NULL;

-- Kreise Nordfriesland, Dithmarschen, Helgoland
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 4
    WHERE   (LEFT(ags_0,5) = '01054' OR 
                LEFT(ags_0,5) = '01051' OR
                ags_0 = '01056025') AND 
            dibt_wind_zone IS NULL;

-- Kreise Rendsburg-Eckernförde, Pinneberg, Steinburg 
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 3
    WHERE   (LEFT(ags_0,5) = '01058' OR 
                LEFT(ags_0,5) = '01061' OR
                (LEFT(ags_0,5) = '01056' AND NOT
                ags_0 = '01056025')) AND 
            dibt_wind_zone IS NULL;

-- Kreise Segeberg, Plön, Stormarn, Herzogtum Lauenburg, kreisfreie Städte Kiel, Lübeck, Neumünster
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 2
    WHERE   (LEFT(ags_0,5) = '01060' OR 
                LEFT(ags_0,5) = '01057' OR
                LEFT(ags_0,5) = '01062' OR
                LEFT(ags_0,5) = '01053' OR
                ags_0 = '01002000' OR
                ags_0 = '01003000' OR
                ags_0 = '01004000') AND 
            dibt_wind_zone IS NULL;

-- Kreis Ostholstein
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 4
    WHERE   (ags_0 = '01055046') AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Ostholstein') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Gremersdorf', 'Neukirchen', 'Heringsdorf', 
                    'Göhl', 'Grube', 'Dahme', 'Kellenhusen', 'Riepsdorf', 
                    'Großenbrode', 'Heiligenhafen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 3
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 2
    WHERE   (LEFT(ags_0,5) = '01055') AND 
            dibt_wind_zone IS NULL;


-- HH (02)
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = 2
    WHERE   (ags_0 = '02000000') AND 
            dibt_wind_zone IS NULL;


-- NI (03)

-- Landkreise Aurich, Wittmund, Friesland, Cuxhaven, kreisfreie Städte Emden, Wilhelmshaven
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Aurich', 'Wittmund', 'Friesland', 'Cuxhaven', 'Emden', 'Wilhelmshaven') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 4
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Wesermarsch
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Wesermarsch') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Butjadingen', 'Stadland', 'Nordenham', 'Jade', 'Ovelgönne', 'Brake (Unterweser)') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 4
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Wesermarsch') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 3
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Stade
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Stade') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Freiburg', 'Balje', 'Krummendeich', 'Oederquart') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 4
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Stade') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 3
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Landkreise Leer, Ammerland, Oldenburg, Osterholz, kreisfreie Städte Oldenburg, Delmenhorst
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Leer', 'Ammerland', 'Oldenburg', 'Osterholz', 'Oldenburg (Oldb)', 'Delmenhorst') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 3
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis  Rotenburg Wümme
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Rotenburg (Wümme)') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Bremervörde', 'Gnarrenburg', 'Alfstedt', 'Ebersdorf', 
                'Oerel', 'Hipstedt', 'Basdahl', 'Rhade', 'Breddorf', 
                'Hepstedt', 'Tarmstedt', 'Wilstedt', 'Vorwerk', 'Zeven', 
                'Heeslingen', 'Anderlingen', 'Selsingen', 'Seedorf', 
                'Ostereistedt', 'Kirchtimke', 'Westertimke', 
                'Sandbostel', 'Seinstedt', 'Farven', 'Bülstedt', 'Deinstedt') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 3
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Rotenburg (Wümme)') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Region Hannover, Landkreise Emsland, Grafschaft Bentheim, Cloppenburg, Vechta, Diepholz, Verden, Harburg, Lüneburg, Soltau-Fallingbostel, Uelzen, Lüchow-Dannenberg, Celle, Nienburg, Gifhorn, Peine, Helmstedt, Wolfenbüttel, Goslar, Osterode am Harz, kreisfreie Städte Hannover, Wolfsburg, Braunschweig, Salzgitter
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Region Hannover', 'Emsland', 'Grafschaft Bentheim', 
    'Cloppenburg', 'Vechta', 'Diepholz', 'Verden', 'Harburg', 'Lüneburg', 
    'Soltau-Fallingbostel', 'Uelzen', 'Lüchow-Dannenberg', 'Celle', 'Nienburg (Weser)', 
    'Gifhorn', 'Peine', 'Helmstedt', 'Wolfenbüttel', 'Goslar', 'Osterode am Harz', 
    'Wolfsburg', 'Braunschweig', 'Salzgitter', 'Heidekreis') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Osnabrück, kreisfreie Stadt Osnabrück
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Osnabrück') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Wallenhorst', 'Belm', 'Bissendorf', 
        'Melle', 'Dissen am Teutoburger Wald', 'Bad Iburg', 
        'Hilter am Teutoburger Wald', 'Georgsmarienhütte', 
        'Hagen am Teutoburger Wald', 'Hasbergen', 'Osnabrück') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Osnabrück') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Schaumburg
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Schaumburg') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Rinteln') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Schaumburg') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Hameln-Pyrmont
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Hameln-Pyrmont') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Bad Münder am Deister') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Hameln-Pyrmont') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Hildesheim
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Hildesheim') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Duingen', 'Alfeld (Leine)', 'Freden (Leine)', 'Coppengrave') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Hildesheim') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Landkreis Holzminden, Northeim, Göttingen
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Holzminden', 'Northeim', 'Göttingen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;


-- HB (04)

-- Stadt Bremen
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Bremen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 3
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Stadt Bremen
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Bremerhaven') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 4
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;


-- NW(05)

-- Kreis Recklinghausen
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Recklinghausen', 'Bottrop', 'Gelsenkirchen') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Gladbeck', 'Bottrop', 'Gelsenkirchen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Recklinghausen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Stadt  Kreise Steinfurt, Borken, Coesfeld, Warendorf, kreisfreie Stadt Münster 
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Steinfurt', 'Borken', 'Coesfeld', 'Warendorf', 'Münster') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Kreis Mettmann, kreisfreie Städte Oberhausen, Duisburg, Essen, Mühlheim, Düsseldorf, Solingen, Wuppertal, Remscheid
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Mettmann', 'Oberhausen', 'Duisburg', 
                'Essen', 'Mülheim an der Ruhr', 'Düsseldorf', 
                'Solingen', 'Wuppertal', 'Remscheid') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Kreise Kleve, Wesel, Viersen, Neuss, kreisfreie Städte Krefeld, Mönchengladbach
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Kleve', 'Wesel', 'Viersen', 'Rhein-Kreis Neuss', 
                'Krefeld', 'Mönchengladbach') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Kreise Herford, Lippe, Paderborn, Höxter, kreisfreie Stadt Bielefeld
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Herford', 'Lippe', 'Paderborn', 'Höxter', 'Bielefeld') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Kreis Gütersloh
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Gütersloh') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Versmold', 'Harsewinkel', 'Gütersloh', 
                'Verl', 'Rheda-Wiedenbrück', 'Rietberg', 'Langenberg', 
                'Herzebrock-Clarholz') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Gütersloh') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Kreis Minden-Lübbecke
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Minden-Lübbecke') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- Arnsberg
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_3_rbz
    WHERE   gen IN ('Arnsberg') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Hamm') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,3) = LEFT(w.ags_0,3) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_3_rbz
    WHERE   gen IN ('Arnsberg') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,3) = LEFT(w.ags_0,3) AND 
            dibt_wind_zone IS NULL;

--  Köln
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Köln', 'Leverkusen' ,'Rheinisch-Bergischer Kreis' ,'Oberbergischer Kreis') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5) AND 
            dibt_wind_zone IS NULL;

-- alle rechtsrheinischen Gemeinden sowie die Stadt Köln
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Rhein-Sieg-Kreis', 'Bonn') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Bornheim', 'Alfter', 'Swisttal', 
                'Rheinbach', 'Meckenheim', 'Wachtberg', 'Bonn') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND 
            LEFT(x.ags_0,3) = LEFT(w.ags_0,3) AND 
            dibt_wind_zone IS NULL;

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Rhein-Sieg-Kreis') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,3) = LEFT(w.ags_0,3) AND 
            dibt_wind_zone IS NULL;


-- HE(06)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Hessen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;


-- RP(07)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Rheinland-Pfalz') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;

-- Kreise Ahrweiler, Vulkaneifel, Bitburg-Prüm
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Ahrweiler', 'Vulkaneifel', 'Eifelkreis Bitburg-Prüm') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5);


-- Kreis Mayen-Koblenz, kreisfreie Stadt Koblenz
-- alle Gemeinden und Teile von Gemeinden rechts der Mosel und rechts des Rheins (lol)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Mayen-Koblenz') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5);

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Mayen-Koblenz') ),
        x AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Brodenbach', 'Rhens', 'Spay',
                    'Dieblich', 'Waldesch', 'Nörtershausen',
                    'Niederfell', 'Brey', 'Macken', 'Burgen',
                    'Alken', 'Oberfell') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w,x
    WHERE   a.ags_0 = x.ags_0 AND
            LEFT(x.ags_0,3) = LEFT(w.ags_0,3) AND
            dibt_wind_zone = 2;

-- Kreis Cochem-Zell
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Cochem-Zell'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Cochem-Zell')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '071' AND
             gen IN ('Altlay',
                     'Altstrimmig',
                     'Beilstein',
                     'Blankenrath',
                     'Briedel',
                     'Briedern',
                     'Bruttig-Fankel',
                     'Bullay',
                     'Ellenz-Poltersdorf',
                     'Forst (Hunsrück)',
                     'Grenderich',
                     'Haserich',
                     'Hesweiler',
                     'Lieg',
                     'Liesenich',
                     'Lütz',
                     'Mesenich',
                     'Mittelstrimmig',
                     'Moritzheim',
                     'Moselkern',
                     'Müden (Mosel)',
                     'Neef',
                     'Nehren',
                     'Panzweiler',
                     'Peterswald-Löffelscheid',
                     'Reidenhausen',
                     'Schauren',
                     'Senheim',
                     'Sosberg',
                     'Tellig',
                     'Treis-Karden',
                     'Valwig',
                     'Walhausen',
                     'Zell (Mosel)'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 2;

-- Kreis Bernkastel-Wittlich
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Bernkastel-Wittlich'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Bernkastel-Wittlich')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '072'
         AND gen IN ('Berglicht',
                     'Bernkastel-Kues',
                     'Brauneberg',
                     'Breit',
                     'Büdlich',
                     'Burg (Mosel)',
                     'Burgen',
                     'Burtscheid',
                     'Deuselbach',
                     'Dhronecken',
                     'Enkirch',
                     'Etgert',
                     'Gielert',
                     'Gornhausen',
                     'Graach an der Mosel',
                     'Gräfendhron',
                     'Heidenburg',
                     'Hilscheid',
                     'Hochscheid',
                     'Horath',
                     'Immert',
                     'Irmenach',
                     'Kleinich',
                     'Kommen',
                     'Longkamp',
                     'Lötzbeuren',
                     'Lückenburg',
                     'Malborn',
                     'Merschbach',
                     'Monzelfeld',
                     'Morbach',
                     'Mülheim an der Mosel',
                     'Neumagen-Dhron',
                     'Neunkirchen',
                     'Piesport',
                     'Rorodt',
                     'Schönberg',
                     'Starkenburg',
                     'Talling',
                     'Thalfang',
                     'Traben-Trarbach',
                     'Veldenz',
                     'Wintrich'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 2;

-- Kreis Trier-Saarburg
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Bernkastel-Wittlich')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '072'
         AND gen IN ('Aach',
                     'Bekond',
                     'Föhren',
                     'Igel',
                     'Klüsserath',
                     'Kordel',
                     'Langsur',
                     'Naurath (Eifel)',
                     'Newel',
                     'Ralingen',
                     'Schweich',
                     'Trierweiler',
                     'Welschbillig',
                     'Zemmer'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 1;



-- BW(08)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Baden-Württemberg') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;


-- Regierungsbezirk Freiburg
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Konstanz')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '083'
         AND gen IN ('Reichenau',
                     'Konstanz',
                     'Allensbach'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 1;

-- Alb-Donau-Kreis
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Alb-Donau-Kreis')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '084'
         AND gen IN ('Balzheim',
                     'Dietenheim',
                     'Hüttisheim',
                     'Illerrieden',
                     'Schnürpflingen',
                     'Staig',
                     'Illerkirchberg'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 1;

-- Bodenseekreis; Landkreise Biberach, Ravensburg und Sigmaringen
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Lindau (Bodensee)', 'Bodenseekreis', 'Ravensburg', 'Sigmaringen', 'Biberach'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);


-- BY(09)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Bayern') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;

-- Schwabenländle
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE LEFT(ags_0, 2) = '09'
    AND gen IN
        ('Günzburg', 'Neu-Ulm', 'Augsburg', 'Aichach-Friedberg', 'Unterallgäu', 'Lindau (Bodensee)', 'Memmingen',
         'Kaufbeuren', 'Augsburg'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

-- Kreis Oberallgäu
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Oberallgäu')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '097'
         AND gen IN ('Altusried',
                     'Dietmannsried',
                     'Haldenwang'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 1;

-- Kreis Ostallgäu
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Ostallgäu'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Ostallgäu')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '097'
         AND gen IN ('Pfronten',
                     'Hopferau',
                     'Schwangau',
                     'Füssen',
                     'Rieden am Forggensee',
                     'Seeg',
                     'Roßhaupten',
                     'Görisried',
                     'Wald',
                     'Stötten a. Auerberg',
                     'Lengenwang',
                     'Rückholz',
                     'Nesselwang',
                     'Eisenberg',
                     'Halblech',
                    'Lechbruck am See'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 2;

-- Oberbayern
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE LEFT(ags_0, 3) = '091'
    AND gen IN
        ('Dachau', 'München', 'Fürstenfeldbruck', 'Landsberg am Lech', 'Ebersberg', 'Starnberg', 'München')
  OR (gen = 'Rosenheim' AND bez = 'Kreisfreie Stadt'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

-- Kreis Weilheim-Schongau
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Weilheim-Schongau'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Weilheim-Schongau')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '091'
         AND gen IN ('Bernbeuren',
                     'Prem',
                     'Steingaden',
                     'Wildsteig'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 2;

--  Kreis Bad Tölz-Wolfratshausen
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Bad Tölz-Wolfratshausen')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '091'
         AND gen IN ('Bad Heilbrunn',
'Bad Tölz',
'Dietramszell',
'Egling',
'Eurasburg',
'Geretsried',
'Icking',
'Königsdorf',
'Münsing',
'Pupplinger Au',
'Reichersbeuern',
'Sachsenkam',
'Wolfratshausen',
'Wolfratshauser Forst'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 1;

-- Kreis Miesbach
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Miesbach')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '091'
         AND gen IN ('Gmund a. Tegernsee',
                     'Hausham',
                     'Holzkirchen',
                     'Irschenberg',
                     'Miesbach',
                     'Otterfing',
                     'Valley',
                     'Waakirchen',
                     'Warngau',
                     'Weyarn'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 1;

-- Kreis Traunstein
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Traunstein'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Traunstein')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '091'
         AND gen IN ('Bergen',
                     'Fridolfing',
                     'Grassau',
                     'Inzell',
                     'Kirchanschöring',
                     'Marquartstein',
                     'Palling',
                     'Petting',
                     'Reit im Winkl',
                     'Ruhpolding',
                     'Schleching',
                     'Siegsdorf',
                     'Staudach-Egerndach',
                     'Surberg',
                     'Taching a. See',
                     'Tittmoning',
                     'Unterwössen',
                     'Waging a. See',
                     'Waginger See',
                     'Wonneberg'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 2;

-- Kreis Rosenheim
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Rosenheim') AND bez = 'Landkreis')
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Rosenheim')
    AND bez = 'Landkreis'),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '091'
         AND gen IN ('Aschau i. Chiemgau',
                     'Brannenburg',
                     'Flintsbach a. Inn',
                     'Kiefersfelden',
                     'Nußdorf a. Inn',
                     'Oberaudorf',
                     'Samerberg'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 2;



-- SL(10)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Saarland') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 1
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;


-- BE(11)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Berlin') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;


-- BB(12)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Brandenburg') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;


-- MV(13)





-- SN(14)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Sachsen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;


-- ST(15)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Sachsen-Anhalt') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;


-- TH(16)
WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   gen IN ('Thüringen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = 2
    FROM    w
    WHERE   LEFT(a.ags_0,2) = LEFT(w.ags_0,2) AND 
            dibt_wind_zone IS NULL;

-- Kreise Schmalkalden-Meiningen, Hildburghausen, Sonneberg, kreisfreie Stadt Suhl
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Schmalkalden-Meiningen', 'Hildburghausen', 'Sonneberg', 'Suhl'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);


-- Wartburgkreis
WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Wartburgkreis'))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 1
FROM w
WHERE LEFT(a.ags_0, 5) = LEFT(w.ags_0, 5);

WITH w AS (
  SELECT ags_0, gen
  FROM boundaries.bkg_vg250_4_krs
  WHERE gen IN ('Wartburgkreis')),
     x AS (
       SELECT ags_0, gen
       FROM boundaries.bkg_vg250_6_gem
       WHERE LEFT(ags_0, 3) = '160'
         AND gen IN ('Hallungen',
                     'Hörselberg-Hainich',
                     'Ebenshausen',
                     'Berka v.d. Hainich',
                     'Mihla',
                     'Frankenroda',
                     'Lauterbach',
                     'Nazza',
                     'Ruhla',
                     'Wutha-Farnroda',
                     'Bischofroda',
                     'Seebach',
                     'Krauthausen',
                     'Creuzburg',
                     'Ifta',
                     'Treffurt'
         ))
UPDATE model_draft.rli_dibt_windzone_vg a
SET dibt_wind_zone = 2
FROM w,
     x
WHERE a.ags_0 = x.ags_0
  AND LEFT(x.ags_0, 3) = LEFT(w.ags_0, 3)
  AND dibt_wind_zone = 1;



-- delete Kreis
UPDATE  model_draft.rli_dibt_windzone_vg
    SET     dibt_wind_zone = NULL
    WHERE   LEFT(ags_0,5) = '01055';

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_4_krs
    WHERE   gen IN ('Gütersloh') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = NULL
    FROM    w
    WHERE   LEFT(a.ags_0,5) = LEFT(w.ags_0,5);

WITH    w AS (
    SELECT  ags_0, gen
    FROM    boundaries.bkg_vg250_6_gem
    WHERE   gen IN ('Neukirchen') )
UPDATE  model_draft.rli_dibt_windzone_vg a
    SET     dibt_wind_zone = NULL
    FROM    w
    WHERE   a.ags_0 = w.ags_0;





/*
-- insert LAN
INSERT INTO model_draft.rli_dibt_windzone_vg (ags_0,dibt_wind_zone,geom)
    SELECT  ags_0,
            2,
            geom
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   ags_0 = '02000000' OR
            ags_0 = '11000000' OR
            ags_0 = '12000000' OR
            ags_0 = '14000000' OR
            ags_0 = '15000000';
    
INSERT INTO model_draft.rli_dibt_windzone_vg (ags_0,dibt_wind_zone,geom)
    SELECT  ags_0,
            1,
            geom
    FROM    boundaries.bkg_vg250_2_lan
    WHERE   ags_0 = '06000000';
*/

