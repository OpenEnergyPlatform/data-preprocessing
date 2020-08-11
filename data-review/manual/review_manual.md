# OEP Data Review

## Process and Workflow

### An open GitHub Issue
* A contributor has opened a [Metadata Review Issue](https://github.com/OpenEnergyPlatform/data-preprocessing/issues/new/choose) in the data-preprocessing repository using the issue template and assigned you. Try to help them by fixing all mistakes with a straight forward solution and documenting what you did. Ask for the information that might still be missing for you to finish the review. For your reference: There are example and template files for the metadata string in the [oemetadata repository](https://github.com/OpenEnergyPlatform/oemetadata/tree/develop/metadata/latest))).

### Metadata string

* If the submitter has not provided a string anywhere you can find it, kindly ask them to provide it to you
* If the string is attached to the issue, download it and push it to a new branch, named according to the name of the dataset "review/*nameofdataset*"
* If the user has already done these things, make sure that the naming is appropriate and continue with the next steps
* Have a look if the contributor could work off all their checkboxes. If they could not, offer some help. If possible to you, you may also complete a few of their tasks.

#### Check the license first
* Only open data is allowed on the platform. If anything else is uploaded, there might be nasty legal consequences. So before deep-diving, check the string if the data is available under an [open license]([open license](http://licenses.opendefinition.org/). The most common ones should be CC0, dl-de/zero, CC-BY, dl-de/by, PDDL, ODbL-1.0. as described in the [license recommendation](https://github.com/OpenEnergyPlatform/tutorial/blob/master/other/tutorial_open-data-licenses.ipynb). If no open license is available for the dataset, send a friendly reminder to the original contributor that only open data is allowed on the OEP. If there are reasons for a review of metadata on not openly licensed datasets, just establish that the data will not be published on the OEP.

#### Check string validity
1. Check if string is valid json with the tool of your choice. If you don't have one, maybe try [jsonlint](https://jsonlint.com/).
2. Check if [omi](https://github.com/OpenEnergyPlatform/omi) can parse the string by running `omi translate -f oep-v1.4 name_of_string.json`. A valid string will just be returned in the command line.

#### Look at the string
* Look at the string from top to bottom ...
1. Check if all keys of the strings are there and whether there are additional keys. Supplement missing ones and remove additional ones. Let the original contributor know about these.
2. While looking at each item, try to interpret the entered values and make sure they conform to the [metadata key description](https://github.com/OpenEnergyPlatform/oemetadata/blob/develop/metadata/latest/metadata_key_description.md). The following points describe things to check in specific fields, ordered by the sequence of the string.
3. Make sure the table name follows the **OEP Naming Conventions**:
 * content
    * name starts with the copyright owner, source, project or model name (e.g. zensus, eGo, oemof)
    * main value (e.g. population)
    * Use underscores as separatos
    * separations with "by" (e.g. by_gender)
    * resolution info with "per" (e.g. per_mun)
 * format
    * only use lower case
    * use the singular instead of plural.
    * use [ASCII characters](https://en.wikipedia.org/wiki/ASCII) only
    * no points, commas or spaces
    * avoid dates
 * Example: zensus_population_by_gender_per_mun
4. Check all links in string to make sure that
   * there are no dead links
   * links reference the intended location
   * sources and attributions are correct
5. Add appropriate [OEP tags](http://openenergy-platform.org/dataedit/tags) in the list of keywords
6. Check the dates for compliance with [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601). This applies to the keys `publicationDate`, `referenceDate`, `start`, `end` and `date`.
7. Make sure that there is an author with a contact and add yourself as a reviewer in the contributors list.
8. The table should be created in the schema _model_draft_ and then moved to the final schema. Under `resources` the key `name` is the name of the table as it will be stored on the OEDB. The schema is specified by putting the schema name in front and separating it from the table name with a dot. So the name will read something like `model_draft.tablename`. When [uploading the data/metadata via oem2orm](https://github.com/OpenEnergyPlatform/tutorial/blob/master/upload/OEP_Upload_Process_Data_and_Metadata.ipynb), model_draft will need to be set as a schema in the resources name. Once that is done, change the schema to where the final location of the dataset is supposed to go. A [list of schemas](https://openenergy-platform.org/dataedit/schemas) can be observed on the OEP.
9. Check if the resource description reflets the provided data.
10. Only in the case of geographic data, make sure that:
 *  the geometry column is named `geom` (for vector data) or `rast` (for raster data)
 * The data type is `geometry` (or `raster`)
 * One of the [geometric types of PostgreSQL](https://www.postgresql.org/docs/current/static/datatype-geometric.html) is set for each column
 * The CRS (SRID) defined is defined with an [EPSG code](http://spatialreference.org/ref/epsg/). Common codes are WGS84 -  [EPSG:4326](http://spatialreference.org/ref/epsg/4326/) and ETRS89 - [EPSG:3035](http://spatialreference.org/ref/epsg/3035/)
11. Award a badge (see below for criteria)


#### Optional Steps
12. If you find new energy-related abbreviations, if you can, see if you can suggest adding them in the [OEO](https://github.com/OpenEnergyPlatform/ontology) by opening an [issue](https://github.com/OpenEnergyPlatform/ontology/issues/new/choose), or maybe just to the [openmod glossary](https://wiki.openmod-initiative.org/wiki/Category:Glossary)
13. If you notice anything that's not described here or if you have any other suggestions for this document, feel free to create an [issue on review improvement](https://github.com/OpenEnergyPlatform/data-preprocessing/issues/new/choose).

#### Final step: Uploading
* Go an check whether the submitter has already
  * created the table (with the [upload tutorial](https://github.com/OpenEnergyPlatform/tutorial/blob/master/upload/OEP_Upload_Process_Data_and_Metadata.ipynb))
  * attached the metadata string to the table
  * uploaded any data
* Check that a primary key is set
* If any errors occur(ed), check if all columns are described in resources and have the right data format
* Move the data to the final schema
* Merge the related PR
* Tick the last boxes of the issue and close it

## Data quality

The database set-up of the OEP is designed to support users in achieving good data quality:

* Plausibility and integration tests are applied to identify mistakes in the data.
* When the number of users and reviewers becomes large enough, user evaluations and ratings on data quality will be implemented.

Further information and guidelines regarding data management and data publication can be found here: [Open Knowledge Foundation](https://okfn.org/opendata/how-to-open-data/), [Open Data Foundation](http://www.odaf.org/?lvl1=resources&lvl2=papers) and [Software Carpentry](https://software-carpentry.org/) (e.g. [here](https://github.com/swcarpentry/good-enough-practices-in-scientific-computing/blob/gh-pages/good-enough-practices-for-scientific-computing.pdf)).


Refer to
https://cos.io/our-services/open-science-badges/



A certain badge implies that defined criteria are fulfilled, including subordinate ones (e.g. datasets holding a gold badge also fulfill criteria of bronze and silver).

### Badge criteria

The quality of data is indicated by a badge, e.g.
* Bronze
* Silver
* Gold
* Platin

1. **Bronze** (must-have)
* Meta data exist
* Primary key on table
* Has name following conventions
2. **Silver** (should-have)
* Meta data exhaustive
* Spatial index defined
* Data, metadata and additional material (e.g., documentation, article) has been provided
3. **Gold** (good-to-have)
* Plausibility and integrity - for verification
* ...
4. **Platin** (best-practice)
* Approved/rated positively by XX users
* A testing script is provided
