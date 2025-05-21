
import json
from pathlib import Path

from frictionless.resources import TableResource
from frictionless import Schema, fields
from omi.inspection import infer_metadata

def get_file_path_csv(fn):
    # Get path
    path_fn_csv = Path(__file__).parent / "data" / f"{fn}.csv"
    print(path_fn_csv)

    return path_fn_csv

def get_file_path_json(fn):
    # Get path
    path_fn_json = Path(__file__).parent / "data" / f"{fn}.json"
    print(path_fn_json)

    return path_fn_json

def frictionless_table_infer(fn):
    # Get path
    path_fn_csv = get_file_path_csv(fn)

    # Infer metadata
    resource = TableResource(
        path = path_fn_csv)
    resource.infer(stats=True)

    print(resource)

    return resource

def omi_infer_metadata(fn):

    # Get path
    path_fn_csv = get_file_path_csv(fn)
    print(path_fn_csv)
    path_fn_json = get_file_path_json(fn)
    print(path_fn_json)

    # Infer metadata from CSV file
    with path_fn_csv.open("r") as f:
        metadata = infer_metadata(f, "OEP")

    # Save to a JSON file
    with open(path_fn_json, "w",
              encoding="utf-8") as json_file:
        json.dump(metadata, json_file, ensure_ascii=False, indent=4)

    print(metadata)

    return metadata


if __name__ == '__main__':

    # Inspect CSV
    fn_data = '2025-05-05_Ariadne2_Data_v1.0_data'
    # resource = frictionless_table_infer(fn_data)
    metadata = omi_infer_metadata(fn_data)

    # Convert schema.field to
    #fields =