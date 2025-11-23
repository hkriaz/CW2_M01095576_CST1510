# main.py

import pandas as pd
from app.data.db import connect_database
from app.data import schema, incidents
from app.data.datasets import load_csv_to_table
from app.services.user_service import migrate_users_from_file

def main():
    print("--- ⚙️  Starting Data Platform Setup ---")
    
    # 1. Connect to the Database
    conn = connect_database()
    print("Database connection established.")
    
    # 2. Initialize the Schema (Create Tables)
    schema.create_all_tables(conn)
    
    # 3. Migrate Users (Service Layer Logic)
    migrate_users_from_file(conn)
    
    # 4. Load Data (Dataset Utility)
    # Load Datasets Metadata
    load_csv_to_table(
        conn, 
        csv_filename="Datasets_Metadata.csv", 
        table_name="datasets_metadata", 
        if_exists_policy='replace'
    )
    
    # Load IT Tickets Data
    load_csv_to_table(
        conn, 
        csv_filename="IT_Tickets.csv", 
        table_name="it_tickets", 
        if_exists_policy='replace'
    )
    
    print("\n--- 🛠️  Testing Incident CRUD Operations ---")
    
    # A. CREATE: Insert a new incident
    incident_id = incidents.insert_incident(
        conn,
        date="2025-10-22",
        incident_type="DDoS Attack",
        severity="High",
        status="Investigating",
        description="External volumetric attack targeting web server.",
        reported_by="SOC Team"
    )
    print(f"✅ New Incident created with ID: {incident_id}")
    
    # B. READ: Retrieve all incidents (as a Pandas DataFrame)
    print("\n**Current Incidents List:**")
    all_incidents_df = incidents.get_all_incidents(conn)
    if not all_incidents_df.empty:
        print(all_incidents_df.head(5).to_markdown(index=False)) # Display first 5 rows
    else:
        print("No incidents found.")
        
    # C. UPDATE: Change the status of the new incident
    rows_updated = incidents.update_incident_status(
        conn, 
        incident_id=incident_id, 
        new_status="Mitigated"
    )
    print(f"\n✅ Updated {rows_updated} row(s) for Incident ID {incident_id}. New Status: Mitigated")
    
    # D. DELETE: Remove the incident
    rows_deleted = incidents.delete_incident(conn, incident_id=incident_id)
    print(f"✅ Deleted {rows_deleted} row(s). Incident ID {incident_id} removed.")
    
    # E. Final Read to confirm deletion
    print("\n**Incidents List after Deletion:**")
    final_incidents_df = incidents.get_all_incidents(conn)
    if not final_incidents_df.empty:
        print(final_incidents_df.head(5).to_markdown(index=False))
    else:
        print("All incidents cleared.")
        
    # 5. Close Connection
    conn.close()
    print("\n--- 🛑 Setup and Testing Complete. Database connection closed. ---")

if __name__ == "__main__":
    main()
