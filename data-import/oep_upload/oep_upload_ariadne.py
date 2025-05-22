import json
from pathlib import Path

from frictionless.resources import TableResource
from frictionless import FrictionlessException, errors
# from frictionless import Schema, fields
from omi.inspection import infer_metadata


# from oem2orm import oep_oedialect_oem2orm as oem2orm


def get_file_path_csv(fn):
    # Get path
    path_fn_csv = Path(__file__).parent / "data" / f"{fn}.csv"
    print(path_fn_csv)

    return path_fn_csv


def get_file_csv(fn):
    # Get path
    fn_csv = f"data/{fn}.csv"
    print(fn_csv)

    return fn_csv


def get_file_path_json(fn):
    # Get path
    path_fn_json = Path(__file__).parent / "data" / f"{fn}.json"
    print(path_fn_json)

    return path_fn_json


def frictionless_table_infer(fn):
    try:
        # Get path
        fn_csv = get_file_csv(fn)

        # Infer metadata
        resource = TableResource(
            path = fn_csv)
        resource.infer(stats = True)

        # Output summary
        print(f"[INFO] Successfully inferred metadata for: {fn_csv}")
        print(resource.to_view())

        return resource

    except Exception as e:
        note = f"Failed to infer metadata for: {fn} — {str(e)}"
        raise FrictionlessException(errors.FormatError(note = note))


def omi_infer_metadata(fn):
    # Get path
    path_fn_csv = get_file_path_csv(fn)
    path_fn_json = get_file_path_json(fn)

    # Infer metadata from CSV file
    with path_fn_csv.open("r") as f:
        metadata = infer_metadata(f, "OEP")

    # Save to a JSON file
    with open(path_fn_json, "w",
              encoding = "utf-8") as json_file:
        json.dump(metadata, json_file, ensure_ascii = False, indent = 4)

    print(metadata)

    return metadata


if __name__ == '__main__':
    # Inspect CSV
    # fn_data = '2025-05-05_Ariadne2_Data_v1.0_data'
    fn_data = '2025-05-05_Ariadne2_Data_v1.0_variables'
    resource = frictionless_table_infer(fn_data)
    metadata = omi_infer_metadata(fn_data)

    # Setup logger
    # oem2orm.setup_logger()

    # Database connection
    # db = oem2orm.setup_db_connection()
    # print(db)

    # Metadata folder
    # metadata_folder = oem2orm.select_oem_dir(oem_folder_name = "data")

    # ORM
    # orm = oem2orm.collect_ordered_tables_from_oem(db, metadata_folder)

    # Create table
    # oem2orm.create_tables(db, orm)
