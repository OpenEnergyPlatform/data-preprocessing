# OEP Data Review

## Process and Workflow

### An open GitHub Issue
* A contributor has opened a [Metadata Review Issue](https://github.com/OpenEnergyPlatform/data-preprocessing/issues/new/choose) in the data-preprocessing repository using the issue template.

### Metadata string

There are examples and templates for the metadata string in the [oemetadata repository](https://github.com/OpenEnergyPlatform/examples/tree/master/metadata))).

#### Make sure string is in new branch with good name
* If the submitter has not provided a string anywhere you can find it, ask them to provide it to you
* If the string is attached to the issue, download it and push it to a new branch, named according to the name of the dataset "review/*nameofdataset*"
* If the user has already done these things make sure that the naming is appropriate and continue with the next steps

#### Look at the string
* Look at the string from top to bottom, check
1. that the string is valid json
2. that all keys of the string are there
3. The table should be created in the schema **model_draft**. Using oem2orm model_draft will need to be set as a schema in the resources name. (template [here](https://github.com/OpenEnergyPlatform/examples/tree/master/api))
4. Make sure the table name follows the **OEP Naming Conventions**:
* content
  * name starts with the copyright owner, source, project or model name (e.g. zensus, eGo, oemof)
  * main value (e.g. population)
  * Use underscores as separatos
  * separations with "by" (e.g. by_gender)
  * resolution info with "per" (e.g. per_mun)
* format
  * only use lower case
  * use the singular instead of the plural.
  * use ASCII characters only
  * no points, no commas
  * no spaces
  * avoid dates
* Example: zensus_population_by_gender_per_mun
5. Check the dates for compliance with [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
6. Try to interpret the values in the string, referring to the [metadata description](https://github.com/OpenEnergyPlatform/oemetadata/wiki/Metadata-Description)
7. If you find new energy-related abbreviations, if you can, see if you can suggest adding them in the [OEO](https://github.com/OpenEnergyPlatform/ontology/issues/new/choose) or at least to the [openmod glossary](https://wiki.openmod-initiative.org/wiki/Category:Glossary)
8. Check the license. the metadata itself must be licensed as CC0. The data can have different open data licenses.
  * Suitable [open license](http://licenses.opendefinition.org/)
9. Check all links in string
  * All sources included (all attributions can be found and are correct)
  * There are no dead links
10. Add appropriate [OEP tags](http://openenergy-platform.org/dataedit/tags) int he list of keywords
11. Make sure that there is an author with a contact and add yourself as a reviewer in the authors list

10. Add to this list of criteria, if you notice anything that's not described here

### data upload
* Go an check whether the submitter has already
  * created the table (using oem2orm as described in the manual)
  * attached the metadata string to the table
  * uploaded any data
* Check that a primary key is set
* If any errors occur(ed), check that all columns are described in resources and have the right data format


## Collection of additional Criteria

These still need to be sorted into the protocol.

### General
* Data, metadata and additional material (e.g., documentation, article) has been provided

### Geographic Data

* (PostGIS)-Geometry is in column named _geom_ (vector) or _rast_ (raster)
* Data type is geometry (or raster)
  * One of the [Geometric Types](https://www.postgresql.org/docs/current/static/datatype-geometric.html) is defined
* The CRS (SRID) defined is defined as [EPSG](http://spatialreference.org/ref/epsg/)
  * Original data stays with the original CRS
  * Prefered CRS of the oedb are
  1. WGS84 - EPSG: [4326](http://spatialreference.org/ref/epsg/4326/)
  1. ETRS89 / ETRS-LAEA - EPSG: [3035](http://spatialreference.org/ref/epsg/3035/)
  * Spacial Index (GIST) on column _geom_
  * All geometries are valid (ST_IsValid)

To get a basic understanding of CRS, see e.g. [QGIS docs](https://docs.qgis.org/latest/en/docs/gentle_gis_introduction/coordinate_reference_systems.html).

## Data quality

The database set-up of the OEP is designed to support users in achieving good data quality:

* Plausibility and integration tests are applied to identify mistakes in the data.
* When the number of users and reviewers becomes large enough, user evaluations and ratings on data quality will be implemented. 

Further information and guidelines regarding data management and data publication can be found here: [Open Knowledge Foundation](https://okfn.org/opendata/how-to-open-data/), [Open Data Foundation](http://www.odaf.org/?lvl1=resources&lvl2=papers) and [Software Carpentry](https://software-carpentry.org/) (e.g. [here](https://github.com/swcarpentry/good-enough-practices-in-scientific-computing/blob/gh-pages/good-enough-practices-for-scientific-computing.pdf)).

## Badge system

Refer to
https://cos.io/our-services/open-science-badges/

The quality of data is indicated by a badge, e.g.
* Bronze
* Silver
* Gold
* Platin

A certain badge implies that defined criteria are fulfilled, including subordinate ones (e.g. datasets holding a gold badge also fulfill criteria of bronze and silver).

### Badge criteria

1. **Bronze** (must-have)
* Primary key
* Follows naming conventions
* Meta data exist
* ...
2. Silver (should-have)
* Meta data exhaustive
* Spatial index defined
* ...
3. Gold (good-to-have)
* Plausibility and integrity -> a testing script is provided for verification
* ...
4. Platin (best-practice)
* Approved/rated positively by XX users
* ...