import pandas as pd
from sqlalchemy import create_engine, types


file_path = r"C:\Users\david\Documents\job_work\Dropship\new_sql_practice\overstock invoice.xlsx"
file = pd.read_excel(file_path, sheet_name=0, nrows=5)
table_name = pd.ExcelFile(file_path).sheet_names[0].strip().replace(" ", "_").replace("/", "_").replace(".", "")


file.columns = [c.strip().replace(" ", "_").replace("/", "_").replace(".", "").lower() for c in file.columns]
column_types = {c: types.VARCHAR(255) for c in file.columns}

connection_string = "mysql+mysqlconnector://root:malik@localhost/sql_practice?allow_local_infile=1"
# 
engine = create_engine(connection_string)
try:
    file.head(0).to_sql(
        name=table_name,
        con=engine,
        if_exists= 'replace',
        index=False,
        dtype=column_types
    )
    print(f"\nSuccess! Table `{table_name}` has been created in MySQL.")

except Exception as e:
    print("\nError creating table:", e)
    
    
    