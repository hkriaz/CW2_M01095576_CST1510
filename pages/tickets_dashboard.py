import streamlit as st
import pandas as pd
from pathlib import Path

# Import your modules
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import register_user, login_user, migrate_users_from_file
from app.data.tickets import (insert_ticket, get_all_tickets, update_ticket_status, delete_ticket, get_ticket_by_id)

st.set_page_config(page_title='It Tickets'
                    )

def load_csv_to_table(csv_path, table_name):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        st.warning(f"CSV file not found: {csv_path}")
        return 0

    try:
        df = pd.read_csv(csv_path)
        conn = connect_database()
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        st.success(f"Loaded {len(df)} rows into {table_name}")
        return len(df)
    except Exception as e:
        st.error(f"Error loading {csv_path.name}: {e}")
        return 0


def setup_database():
    st.info("STARTING DATABASE SETUP")

    # Step 1: Create tables
    st.write("### [1/4] Creating database tables...")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # Step 2: Migrate users
    st.write("### [2/4] Migrating users from users.txt...")
    migrate_users_from_file()
    st.success("Users migrated successfully!")

    # Step 3: Load CSV data
    st.write("### [3/4] Loading CSV data...")
    load_csv_to_table("DATA/it_tickets.csv", "it_tickets")

    # Step 4: Verify
    st.write("### [4/4] Verifying database setup...")
    conn = connect_database()
    cursor = conn.cursor()

    table_summary = []
    cursor.execute(f"SELECT COUNT(*) FROM it_tickets")
    count = cursor.fetchone()[0]
    table_summary.append({"Table": "it_tickets", "Row Count": count})
    conn.close()

    st.table(pd.DataFrame(table_summary))
    st.success("DATABASE SETUP COMPLETE!")

def demo_crud_operations():
    st.subheader("CRUD Operations Demo")

    st.write("#### Add New Tickets")
    tickets_id = st.date_input("Ticket ID")
    priority = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description")
    status = st.selectbox("Status", ["Open", "In progress", "Resolved", "Waiting"])
    assigned = st.text_input("Assigned to")
    created_at = st.date_input("Created at")
    resolution = st.text_input("Resolution in hours")
    updated_at = st.date_input("Updated at")
    if st.button("Create Ticket"):
        ticket = insert_ticket(tickets_id, priority, description, status, assigned, created_at, resolution, updated_at)
        st.success(f"Created ticket #{ticket}")

    st.write("#### View All Tickets")
    if st.button("Fetch Tickets"):
        df = get_all_tickets()
        st.dataframe(df)

    st.write("#### Update Ticket Status")
    incident_id_update = st.number_input("Incident ID to Update", min_value=1)
    new_status = st.selectbox("New Status", ["Open", "Investigating", "Closed"], key="update_status")
    if st.button("Update Ticket"):
        rows = update_ticket_status(incident_id_update, new_status)
        st.success(f"Updated {rows} row(s)")

    st.write("#### Delete Ticket")
    ticket_id_delete = st.number_input("Ticket ID to Delete", min_value=1, key="del_ticket")
    if st.button("Delete Ticket"):
        rows = delete_ticket(ticket_id_delete)
        st.success(f"Deleted {rows} row(s)")


def demo_analytics():
    st.subheader("Analytics Demo")

    st.write("#### All Tickets")
    df_tickets = get_all_tickets()
    st.dataframe(df_tickets)

    st.write("#### Tickets by ID")
    df_ticket_id = get_ticket_by_id(2008)
    st.dataframe(df_ticket_id)

st.title("It Tickets Dashboard")

tabs = st.tabs(["Setup Database", "CRUD Incidents", "Analytics"])

with tabs[0]:
    st.header("Database Setup")
    if st.button("Run Setup"):
        setup_database()

with tabs[1]:
    st.header("CRUD Operations on Tickets")
    demo_crud_operations()

with tabs[2]:
    st.header("Analytics")
    demo_analytics()
