import streamlit as st
import pandas as pd
from pathlib import Path

# Import your modules
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import migrate_users_from_file
from app.data.incidents import (
    insert_incident, get_all_incidents, update_incident_status,
    delete_incident, get_incidents_by_type_count, get_severity_count
)

st.set_page_config(page_title='Cyber Incidents',
                   page_icon="img/mdi.jpg"
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
    load_csv_to_table("DATA/cyber_incidents.csv", "cyber_incidents")

    # Step 4: Verify
    st.write("### [4/4] Verifying database setup...")
    conn = connect_database()
    cursor = conn.cursor()

    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    table_summary = []
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        table_summary.append({"Table": table, "Row Count": count})
    conn.close()

    st.table(pd.DataFrame(table_summary))
    st.success("DATABASE SETUP COMPLETE!")

def demo_crud_operations():

    st.write("#### Add New Incident")
    incident_id = st.date_input("Incident ID")
    timestamp = st.date_input("Timestamp")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    category = st.text_input("Category")
    status = st.selectbox("Status", ["Open", "Investigating", "Closed"])
    description = st.text_area("Description")
    reported_by = st.text_input("Reported by")
    created_at = st.date_input("Created at")
    if st.button("Create Incident"):
        incident = insert_incident(incident_id, timestamp, severity, category, status, description, reported_by, created_at)
        st.success(f"Created incident #{incident_id}")

    st.write("#### View All Incidents")
    if st.button("Fetch Incidents"):
        df = get_all_incidents()
        st.dataframe(df)

    st.write("#### Update Incident Status")
    incident_id_update = st.number_input("Incident ID to Update", min_value=1)
    new_status = st.selectbox("New Status", ["Open", "Investigating", "Closed"], key="update_status")
    if st.button("Update Incident"):
        rows = update_incident_status(incident_id_update, new_status)
        st.success(f"Updated {rows} row(s)")

    st.write("#### Delete Incident")
    incident_id_delete = st.number_input("Incident ID to Delete", min_value=1, key="del_incident")
    if st.button("Delete Incident"):
        rows = delete_incident(incident_id_delete)
        st.success(f"Deleted {rows} row(s)")


def demo_analytics():
    st.subheader("Analytics Demo")

    st.write("#### Incidents by ID")
    df_incidents_id = get_incidents_by_type_count()
    st.dataframe(df_incidents_id)

def chart_analysis():
    data = get_severity_count()
    st.bar_chart(data, x="severity", y = "count")


st.title("Cyber Platform Dashboard")

tabs = st.tabs(["Edit Incidents", "Incidents Analysis","Setup Database"])

with tabs[2]:
    st.header("Database Setup")
    if st.button("Run Setup"):
        setup_database()

with tabs[1]:
    st.header("Incidents Dashboard with modification options")
    demo_crud_operations()

with tabs[0]:
    st.header("Chart Analysis")
    st.subheader("Count of each severity")
    chart_analysis()
    st.header("Incidents Analysis")
    demo_analytics()
