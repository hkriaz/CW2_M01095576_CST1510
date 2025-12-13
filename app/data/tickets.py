import pandas as pd
from app.data.db import connect_database


def insert_ticket(ticket_id, priority, status, category, subject, description,
                  created_date, resolved_date=None, assigned_to=None):
    """
    Insert new IT ticket.

    Args:
        ticket_id: Unique ticket identifier
        priority: Priority level
        status: Current status
        category: Ticket category
        subject: Ticket subject
        description: Ticket description
        created_date: Creation date (YYYY-MM-DD)
        resolved_date: Resolution date (optional)
        assigned_to: Assigned user (optional)

    Returns:
        int: ID of inserted ticket
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets 
        (ticket_id, priority, status, category, subject, description, 
         created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description,
          created_date, resolved_date, assigned_to))
    conn.commit()
    id = cursor.lastrowid
    conn.close()
    return id


def get_all_tickets():
    """
    Get all tickets as DataFrame.

    Returns:
        pandas.DataFrame: All tickets
    """
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def get_ticket_by_id(ticket_id):
    """
    Get a specific ticket by ticket_id.

    Args:
        ticket_id: Unique ticket identifier

    Returns:
        tuple: Ticket record or None
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    ticket = cursor.fetchone()
    conn.close()
    return ticket


def update_ticket_status(ticket_id, new_status, resolved_date=None):
    """
    Update the status of a ticket.

    Args:
        ticket_id: Unique ticket identifier
        new_status: New status value
        resolved_date: Resolution date if status is 'Resolved' or 'Closed'

    Returns:
        int: Number of rows affected
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET status = ?, resolved_date = ? WHERE ticket_id = ?",
        (new_status, resolved_date, ticket_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected


def delete_ticket(ticket_id):
    """
    Delete a ticket from the database.

    Args:
        ticket_id: Unique ticket identifier

    Returns:
        int: Number of rows affected
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def get_priority_count():
    """
    Count priority tickets.

    Returns:
        pandas.DataFrame: priority counts
    """
    conn = connect_database()
    query = """
    SELECT priority, COUNT(*) AS count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return dfimport pandas as pd
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
