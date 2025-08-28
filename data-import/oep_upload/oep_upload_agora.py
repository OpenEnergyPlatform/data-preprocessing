
from split_xlsx_to_csvs import split_xlsx_to_csvs
from omi_infer_metadata import frictionless_table_infer, omi_infer_metadata, get_file_xlsx


if __name__ == '__main__':
    fn_data = '2025-08-26_agora_knde_2024'
    csv_name = 'agora/2025-08-26_agora_knde_2024_jaerhlich'
    fn_xlsx = get_file_xlsx(fn_data)

    # Excel Split
    #csv_files = split_xlsx_to_csvs(fn_xlsx, output_dir = "data/agora")
    #print("Created CSV files:", csv_files)

    # OMI inspect
    resource = frictionless_table_infer(csv_name)
    metadata = omi_infer_metadata(csv_name)

    # OEP Upload
    #oem2orm
