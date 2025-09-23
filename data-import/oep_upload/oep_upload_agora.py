
from split_xlsx_to_csvs import split_xlsx_to_csvs
from omi_infer_metadata import frictionless_table_infer, omi_infer_metadata, get_file_xlsx


if __name__ == '__main__':

    print(f"start")
    import json
    from getpass import getpass
    from os import environ
    import requests as req

    fn_data = 'agora_knde_2024_rounded'
    csv_name_1 = 'agora/agora_knde_2024_jaehrlich'
    csv_name_2 = 'agora/agora_knde_2024_industrie_perioden'
    csv_name_3 = 'agora/agora_knde_2024_industrie_sensitivitaetsanalyse'
    csv_name_4 = 'agora/agora_knde_2024_monatlich'

    # fn_xlsx = get_file_xlsx(fn_data)

    # Excel Split
    # csv_files = split_xlsx_to_csvs(fn_xlsx, output_dir = "data/agora")
    # print("Created CSV files:", csv_files)

    # OMI inspect
    # resource = frictionless_table_infer(csv_name_1)
    # metadata = omi_infer_metadata(csv_name_1)
    #
    # resource = frictionless_table_infer(csv_name_2)
    # metadata = omi_infer_metadata(csv_name_2)
    #
    # resource = frictionless_table_infer(csv_name_3)
    # metadata = omi_infer_metadata(csv_name_3)
    #
    # resource = frictionless_table_infer(csv_name_4)
    # metadata = omi_infer_metadata(csv_name_4)

    # OEP Upload
    #oem2orm

    # Publish to scenario topic
    topic = "model_draft"

    table = f"oemetadata_table_template"
    table_1 = f"agora_knde_2024_jaehrlich"
    table_2 = f"agora_knde_2024_monatlich"
    table_3 = f"agora_knde_2024_industrie_perioden"
    table_4 = f"agora_knde_2024_industrie_sensitivitaetsanalyse"

    print(f"tables")
    publish_in_topic = "scenario"
    token = f""

    table = table_1

    print(table)
    auth_headers = {"Authorization": "Token %s" % token}
    table_publish_api_url = f"https://openenergyplatform.org/api/v0/schema/{topic}/tables/{table}/move_publish/{publish_in_topic}/"
    table_undo_publish_api_url = f"https://openenergyplatform.org/api/v0/schema/{publish_in_topic}/tables/{table}/move_publish/{topic}/"

    print(table_publish_api_url)
    print(table_undo_publish_api_url)

    embargo = {
        # "embargo": {"duration": "6_months"},
        "embargo": None,
    }

    res = req.post(table_publish_api_url, json = {"query": embargo},
                   headers = auth_headers)

    # raise Exception if request fails
    if not res.ok:
        raise Exception(res.reason )

    print(f"done")
