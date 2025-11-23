import pandas as pd
import sqlite3

# This file is responsible for all low-level database interactions
# for the IT Tickets domain.

# --- 1. CREATE: Insert a New Ticket ---
def insert_ticket(conn: sqlite3.Connection, ticket_id: str, priority: str, status: str, category: str, subject: str, description: str, created_date: str, assigned_to: str):
    """
    Insert a new IT ticket into the database. (CREATE)
    """
    cursor = conn.cursor()
    
    insert_sql = """
        INSERT INTO it_tickets 
        (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
    
    cursor.execute(insert_sql, params)
    conn.commit()
    # Return the ID of the new row
    return cursor.lastrowid

# --- 2. READ: Retrieve All Tickets ---
def get_all_tickets(conn: sqlite3.Connection):
    """
    Retrieve all IT tickets from the database, returned as a Pandas DataFrame. (READ)
    """
    query = "SELECT * FROM it_tickets ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    return df

# --- 3. UPDATE: Change Ticket Status and Resolved Date ---
def update_ticket_resolution(conn: sqlite3.Connection, ticket_id: str, new_status: str, resolved_date: str):
    """
    Update the status and resolved date of a specific ticket. (UPDATE)
    """
    cursor = conn.cursor()
    
    update_sql = "UPDATE it_tickets SET status = ?, resolved_date = ? WHERE ticket_id = ?"
    params = (new_status, resolved_date, ticket_id)
    
    cursor.execute(update_sql, params)
    conn.commit()
    # Return the number of rows updated
    return cursor.rowcount

# --- 4. DELETE: Remove a Ticket ---
def delete_ticket(conn: sqlite3.Connection, ticket_id: str):
    """
    Delete an IT ticket from the database using its unique ticket_id. (DELETE)
    """
    cursor = conn.cursor()
    
    delete_sql = "DELETE FROM it_tickets WHERE ticket_id = ?"
    params = (ticket_id,)
    
    cursor.execute(delete_sql, params)
    conn.commit()
    # Return the number of rows deleted
    return cursor.rowcount
