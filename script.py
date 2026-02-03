import pandas as pd
from sqlalchemy import create_engine, types


file_path = r"C:\Users\david\Documents\job_work\Dropship\new_sql_practice\overstock invoice.xlsx"

file = pd.read_excel(file_path, sheet_name=0, nrows=5)
file_metadata = [c.strip().replace(" ", "_").lower() for c in pd.ExcelFile(file_path).sheet_names]
print(file_metadata)
print(file)
columns = []
table_name = file_metadata[0]
column_names = {}
for c in file.columns:
    column_names[(c.strip().replace(" ", "_").lower())] = types.VARCHAR(255)

print(column_names)


# column_types = {col: types.VarChar(255) }

connection_string = "mysql+mysqlconnecter://root:malik@localhost/sql_practice?allow_local_infile=1"
# 
engine = create_engine(connection_string)

try:
    file.head(0).to_sql(
        name=table_name,
        con=engine,
        if_exists= 'replace',
        index=False,
        dtype=column_names
    )
    print(f"\nSuccess! Table `{table_name}` has been created in MySQL.")

except Exception as e:
    print("\nError creating table:", e)
    
    
    