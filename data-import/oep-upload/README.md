# OEM to ORM

Create database tables (and schema) from oemetadata json file(s)

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
