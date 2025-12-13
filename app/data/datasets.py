import pandas as pd
from app.data.db import connect_database


def insert_dataset(dataset_id, name, rows, columns, uploaded_by, upload_date, created_at):
    """
    Insert new dataset metadata.

    Args:
        dataset_id: unique identifier
        name: dataset name
        rows: num of rows
        columns: num of columns
        uploaded_by: who uploaded it
        upload_date: date of upload
        created_at: date and time of creation

    Returns:
        int: ID of inserted dataset
        :param at:
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_id, name, rows, columns, uploaded_by, upload_date, created_at))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id


def get_all_datasets():
    """
    Get all datasets as DataFrame.

    Returns:
        pandas.DataFrame: All datasets
    """
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def get_dataset_by_id(dataset_id):
    """
    Get a specific dataset by ID.

    Args:
        dataset_id: ID of the dataset

    Returns:
        tuple: Dataset record or None
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )
    dataset = cursor.fetchone()
    conn.close()
    return dataset


def update_dataset(dataset_id, **kwargs):
    """
    Update dataset metadata fields.

    Args:
        dataset_id: ID of the dataset
        **kwargs: Fields to update (e.g., last_updated='2024-11-05')

    Returns:
        int: Number of rows affected
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Build dynamic UPDATE query
    set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    values = list(kwargs.values()) + [dataset_id]

    cursor.execute(
        f"UPDATE datasets_metadata SET {set_clause} WHERE id = ?",
        values
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected


def delete_dataset(dataset_id):
    """
    Delete a dataset from the database.

    Args:
        dataset_id: ID of the dataset to delete

    Returns:
        int: Number of rows affected
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def get_uploaded_by_count():
    """
    Count uploaded by

    Returns:
        pandas.DataFrame: uploaded by counts
    """
    conn = connect_database()
    query = """
    SELECT uploaded_by, COUNT(*) AS count
    FROM datasets_metadata
    GROUP BY uploaded_by
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
