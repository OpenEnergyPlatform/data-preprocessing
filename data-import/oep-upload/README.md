# OEM to ORM

Create database tables (and schema) from oemetadata json file(s)

## Installation:

This Package is currently in Alpha. We use the Test PyPi instance until 
all Unit-test and UX-test passed. To install Packages listed there 
we recommend using the following command with Pip: 

`
pip install -i https://test.pypi.org/simple/ oem2orm
`


## Usage:

This tool is part of the open-energy-metadata (OEM) integration into the [OEP](https://openenergy-platform.org/).
To use this tool with the OEP API you need to be signed up to the OEP since
you need to provide an API-Token. 

If you want to upload OEM that was officially reviewed you must clone the
OEP data-preprocessing repository on GitHub [here](https://github.com/OpenEnergyPlatform/data-preprocessing).
The data-review folder contains all of the successfully reviewed OEM files.

For security reasons, tables can only be created in existing 
schemas and just in the schemas "model_draft" and "sandbox".

Keep in mind the current state is not fully tested. The code is
still quit error prone f.e. the postgres types (column datatype) are not fully 
supported by the [oedialct](https://pypi.org/project/oedialect/) - work in progress.

### CLI-Application
Step-by-Step: 
1. Create env from requirements.txt, and activate
2. Put the metadata file in the folder metadata or put your own folder in this 
    directory
3. execute the following in a cmd:
```
python oep_oedialect_oem2orm.py
```
4. Provide credentials and folder name in prompt
5. The table will be created 

### Import as Module

You can simply import this module in your Python script.py like this:

```python
from oem2orm import oep_oedialect_oem2orm as oem2orm
```

Now just call the functions provided in oem2orm like this:

Recommended execution order:
1. Setup the logger
```python
oem2orm.setup_logger()
```

2. Setup the Database API connection as Namedtuple storing the SQLAlchemy engine and metadata:
```python
db = oem2orm.setup_db_connection()
```

3. Provide the oem files in a folder (in the current directory).
3.1 Pass the folder name to the function:
```python
metadata_folder = oem2orm.select_oem_dir(oem_folder_name="folder_name")
```

4. Setup a SQLAlchemy ORM including all data-model in the provided oem files:
```python
orm = oem2orm.collect_ordered_tables_from_oem(db, metadata_folder)
```

5. Create the tables on the Database:
```python
oem2orm.create_tables(db, orm)
```

6. Delete all tables that have been created (all tables available in sa.metadata)
```python
oem2orm.delete_tables(db, orm)
```

##Docs:

### oem2orm generator

#### Supported datatypes

## Database support
