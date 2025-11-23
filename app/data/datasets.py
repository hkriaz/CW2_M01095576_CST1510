import pandas as pd
from pathlib import Path
import sqlite3

# Define paths relative to the project structure
DATA_DIR = Path("DATA")

def load_csv_to_table(conn: sqlite3.Connection, csv_filename: str, table_name: str, if_exists_policy='replace'):
    """
    Reads a CSV file from the DATA directory and loads it into a specified 
    SQLite database table using Pandas.

    Args:
        conn: The active SQLite connection object.
        csv_filename: The name of the CSV file (e.g., "Datasets_Metadata.csv").
        table_name: The name of the database table (e.g., "datasets_metadata").
        if_exists_policy: What to do if the table already exists. Options:
                          'fail', 'replace', 'append'. Defaults to 'replace'.
    
    Returns:
        The number of rows loaded (int).
    """
    filepath = DATA_DIR / csv_filename
    
    if not filepath.exists():
        print(f"⚠️ CSV file not found: {filepath}")
        return 0
    
    try:
        # 1. Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(filepath)
        
        # 2. Use the to_sql method for efficient insertion
        # This handles column mapping and SQL generation automatically
        rows_loaded = df.to_sql(
            table_name, 
            conn, 
            if_exists=if_exists_policy, 
            index=False # Don't write the DataFrame index as a column
        )
        
        print(f"✅ Successfully loaded {rows_loaded} rows from {csv_filename} into table '{table_name}'.")
        return rows_loaded
    
    except Exception as e:
        print(f"❌ Error loading CSV {csv_filename} into {table_name}: {e}")
        return 0
