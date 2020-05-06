# OEM to ORM

Create database tables (and schema) from oemetadata json file(s)

## Usage:
Keep in mind the current state is not fully tested. The code is
still quit error prone f.e. the postgres types are not fully 
supported by the oedialct - work in progress. 

To use this tool you need to be signed up on the OEP. 

For security reasons, tables can only be created in existing 
schemas and just in the schemas "model_draft" and "sandbox".

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
