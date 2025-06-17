from omi_infer_metadata import frictionless_table_infer, omi_infer_metadata

if __name__ == '__main__':
    # Inspect CSV
    # fn_data = '2025-05-05_Ariadne2_Data_v1.0_data'
    fn_data = '2025-05-05_Ariadne2_Data_v1.0_variables'
    resource = frictionless_table_infer(fn_data)
    metadata = omi_infer_metadata(fn_data)
