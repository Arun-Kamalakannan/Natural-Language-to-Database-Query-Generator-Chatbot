from db import get_conn

def fetch_schema(db_user=None, db_password=None, host=None, database=None):
    """
    Fetch all table names and their columns from the specified MySQL database.
    Returns a dictionary: { 'table_name': ['col1', 'col2', ...], ... }
    """
    # Create a database connection
    conn = get_conn(db_user=db_user, db_password=db_password, host=host, database=database)
    cursor = conn.cursor()

    # Fetch all table names
    cursor.execute("SHOW TABLES;")
    tables = [t[0] for t in cursor.fetchall()]

    schema = {}
    for table in tables:
        # Fetch column names for each table
        cursor.execute(f"SHOW COLUMNS FROM `{table}`;")
        columns = [col[0] for col in cursor.fetchall()]
        schema[table] = columns

    # Close cursor and connection
    cursor.close()
    conn.close()

    return schema


def format_schema_for_groq(schema_dict):
    """
    Converts schema dictionary into a Groq-readable string format.
    """
    parts = []
    for table, cols in schema_dict.items():
        parts.append(f"{table}({', '.join(cols)})")

    return "Database tables: " + ", ".join(parts)
