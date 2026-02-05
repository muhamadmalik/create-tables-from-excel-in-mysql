from sqlalchemy import create_engine, types
import pandas as pd
import mysql.connector
import json
import os


file_path = r"C:\Users\david\Documents\job_work\Dropship\new_sql_practice\overstock invoice.xlsx"
file = pd.read_excel(file_path, sheet_name=0, nrows=5)
table_name = pd.ExcelFile(file_path).sheet_names[0].strip().replace(" ", "_").replace("/", "_").replace(".", "")


file.columns = [c.strip().replace(" ", "_").replace("/", "_").replace(".", "").lower() for c in file.columns]
column_types = {c: types.VARCHAR(255) for c in file.columns}



# --- 1. YOUR DATABASE CONNECTION ---
db_config = {
    'host': 'localhost',      
    'user': 'root',           
    'password': 'malik', 
    'database': 'sql_practice'
}

def upload_to_staging(file_path, account_code, file_type, doc_ref):
    """
    file_path: Full path to your Excel/CSV
    account_code: e.g., 'OV9004'
    file_type: 'INV' (for Invoices/DB) or 'PAY' (for Credits/Payments)
    doc_ref: e.g., 'IN#909920'
    """
    file_name = os.path.basename(file_path)
    
    # Load File
    print(f"Reading {file_name}...")
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # Clean column names (lowercase and replace spaces with underscores)
    # This makes it easier to write SQL queries later
    df.columns = [str(c).lower().replace(' ', '_') for c in df.columns]

    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    query = """
        INSERT INTO staging_raw (account_code, file_type, doc_ref, source_file, row_data) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    # Convert data into a list of tuples for fast batch upload
    data_to_insert = []
    for _, row in df.iterrows():
        # Drop empty cells and convert the row to a JSON string
        row_dict = row.dropna().to_dict()
        row_json = json.dumps(row_dict, default=str)
        data_to_insert.append((account_code, file_type, doc_ref, file_name, row_json))
    
    # Upload everything in one go
    cursor.executemany(query, data_to_insert)
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully uploaded {len(data_to_insert)} rows to MySQL.")

# --- 3. RUN THE UPLOAD ---
# Example for Invoice Details (The INV file with Cost and Quantity)
upload_to_staging(
    file_path = r"C:\Users\david\Documents\job_work\Dropship\new_sql_practice\overstock invoice.xlsx", 
    account_code = 'OV9004', 
    file_type = 'INV', 
    doc_ref = 'IN#909920'
)