import pandas as pd
from pathlib import Path

def split_xlsx_to_csvs(xlsx_path, output_dir=None, sep=";"):
    """
    Splits all sheets in an Excel file into separate CSV files.

    Parameters:
        xlsx_path (str or Path): Path to the input .xlsx file.
        output_dir (str or Path, optional): Directory to save CSV files.
                                            Defaults to the same directory as the input file.

    Returns:
        List of output CSV paths.
    """
    xlsx_path = Path(xlsx_path)
    output_dir = Path(output_dir) if output_dir else xlsx_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load all sheets
    xls = pd.read_excel(xlsx_path, sheet_name=None, engine='openpyxl')
    output_paths = []

    for sheet_name, df in xls.items():
        # Clean filename
        safe_sheet_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in sheet_name)
        output_path = output_dir / f"{xlsx_path.stem}_{safe_sheet_name}.csv"
        df.to_csv(output_path, index=False, sep=sep)
        output_paths.append(output_path)

    return output_paths
