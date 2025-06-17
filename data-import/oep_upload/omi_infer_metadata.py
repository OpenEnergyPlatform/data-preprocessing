import json
from pathlib import Path

from frictionless.resources import TableResource
from frictionless import FrictionlessException, errors
# from frictionless import Schema, fields
from omi.inspection import infer_metadata


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


def get_file_xlsx(fn):
    # Get path
    fn_xlsx = f"data/{fn}.xlsx"
    print(fn_xlsx)

    return fn_xlsx

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
