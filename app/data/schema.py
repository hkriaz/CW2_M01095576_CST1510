def create_users_table(conn):
    """
    Create the users table if it doesn't exist.

    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("Users table created successfully!")


def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.

    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        severity TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("Cyber incidents table created successfully!")


def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.

    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("Datasets metadata table created successfully!")


def create_it_tickets_table(conn):
    """
    Create the it_tickets table.

    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("IT tickets table created successfully!")


def create_all_tables(conn):
    """
    Create all tables in the database.

    Args:
        conn: Database connection object
    """
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("\n All tables created successfully!")
