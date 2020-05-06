# OEM to ORM

Create database tables (and schema) from metadata json file(s)

## Usage:
See help: 
1. Create env from requirements.txt, and activate
2. execute the following in a cmd
```
python oep_oedialect_upload_from_gpkg.py
```

Try it with example files in "test_files" folder:
```
python md_to_orm.py --engine=postgresql --host=localhost --port=5432 --log-level=debug --from-folder test_files
```