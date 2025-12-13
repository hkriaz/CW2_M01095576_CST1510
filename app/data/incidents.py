import pandas as pd
from app.data.db import connect_database


def insert_incident(incident_id, severity, status, category, description, reported_by=None):
    """
    Insert new incident into the database.

    Args:
        incident_id: id of incident
        severity: Severity level
        status: Current status
        category: type of incident
        description: Incident description
        reported_by: Username of reporter (optional)

    Returns:
        int: ID of inserted incident
        :param by:
        :param at:
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (incident_id, severity, status, category, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (incident_id, severity, status, category, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id


def get_all_incidents():
    """
    Get all incidents as DataFrame.

    Returns:
        pandas.DataFrame: All incidents
    """
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def get_incident_by_id(incident_id):
    """
    Get a specific incident by ID.

    Args:
        incident_id: ID of the incident

    Returns:
        tuple: Incident record or None
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    incident = cursor.fetchone()
    conn.close()
    return incident


def update_incident_status(incident_id, new_status):
    """
    Update the status of an incident.

    Args:
        incident_id: ID of the incident
        new_status: New status value

    Returns:
        int: Number of rows affected
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected


def delete_incident(incident_id):
    """
    Delete an incident from the database.

    Args:
        incident_id: ID of the incident to delete

    Returns:
        int: Number of rows affected
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected


def get_incidents_by_type_count():
    """
    Count incidents by type.

    Returns:
        pandas.DataFrame: Incident counts by type
    """
    conn = connect_database()
    query = """
    SELECT incident_id, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_id
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_severity_count():
    """
    Count severity incidents

    Returns:
        pandas.DataFrame: severity incident counts
    """
    conn = connect_database()
    query = """
    SELECT severity, COUNT(*) AS count
    FROM cyber_incidents
    GROUP BY severity
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
