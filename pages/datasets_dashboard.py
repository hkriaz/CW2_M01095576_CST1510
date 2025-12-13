import streamlit as st
import pandas as pd
from pathlib import Path

# Import your modules
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_services import migrate_users_from_file
from app.data.datasets import (insert_dataset, get_all_datasets, update_dataset, delete_dataset, get_dataset_by_id)

st.set_page_config(page_title='Datasets Metadata'
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
    load_csv_to_table("DATA/datasets_metadata.csv", "datasets_metadata")

    # Step 4: Verify
    st.write("### [4/4] Verifying database setup...")
    conn = connect_database()
    cursor = conn.cursor()

    table_summary = []
    cursor.execute(f"SELECT COUNT(*) FROM datasets_metadata")
    count = cursor.fetchone()[0]
    table_summary.append({"Table": "datasets_metadata", "Row Count": count})
    conn.close()

    st.table(pd.DataFrame(table_summary))
    st.success("DATABASE SETUP COMPLETE!")

def demo_crud_operations():
    st.subheader("CRUD Operations Demo")

    st.write("#### Add New Dataset")
    dataset_id = st.text_input("Dataset ID")
    name = st.text_input("Name")
    rows = st.text_input("Rows")
    columns = st.text_input("Columns")
    uploaded_by = st.text_input("Uploaded by")
    uploaded_at = st.date_input("Upload Date")
    created_at = st.date_input("Created Date")
    if st.button("Create Incident"):
        dataset = insert_dataset(dataset_id, name, rows, columns, uploaded_by, uploaded_at, created_at)
        st.success(f"Created dataset #{dataset}")

    st.write("#### View All tickets")
    if st.button("Fetch Tickets"):
        df = get_all_datasets()
        st.dataframe(df)

    st.write("#### Update Dataset Status")
    dataset_id_update = st.number_input("Incident ID to Update", min_value=1)
    new_status = st.selectbox("New Status", ["Open", "Investigating", "Closed"], key="update_status")
    if st.button("Update Dataset"):
        rows = update_dataset(dataset_id_update, new_status)
        st.success(f"Updated {rows} row(s)")

    st.write("#### Delete Datasets")
    dataset_id_delete = st.number_input("Dataset ID to Delete", min_value=1, key="del_dataset")
    if st.button("Delete Datasets"):
        rows = delete_dataset(dataset_id_delete)
        st.success(f"Deleted {rows} row(s)")


def demo_analytics():
    st.subheader("Analytics Demo")
    st.write("#### All Datasets")
    df_datasets = get_all_datasets()
    st.dataframe(df_datasets)

def chart_analysis():
    data = get_uploaded_by_count()
    st.bar_chart(data, x="uploaded_by", y="count")


st.title("Datasets Metadata Dashboard")

tabs = st.tabs(["Setup Database", "CRUD Incidents", "Analytics"])

with tabs[2]:
    st.header("Database Setup")
    if st.button("Run Setup"):
        setup_database()

with tabs[1]:
    st.header("CRUD Operations on Datasets")
    demo_crud_operations()

with tabs[0]:
    st.header("Chart Analysis")
    st.subheader("Count of each uploader")
    chart_analysis()
    st.header("Analytics")
    demo_analytics()
