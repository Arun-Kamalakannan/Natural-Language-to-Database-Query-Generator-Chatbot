import mysql.connector

def get_conn(db_user, db_password, host, database):
    """
    Returns a MySQL connection object using the provided credentials.
    """
    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=host,
        database=database,
        autocommit=True
    )

def fetch_query(sql, db_user, db_password, host, database):
    """
    Executes a SELECT query and returns columns and rows.
    """
    conn = get_conn(db_user, db_password, host, database)
    cursor = conn.cursor()
    cursor.execute(sql)
    cols = [desc[0] for desc in cursor.description] if cursor.description else []
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return cols, rows

def execute_query(sql, db_user, db_password, host, database):
    """
    Executes an INSERT/UPDATE/DELETE/CREATE query and returns affected rows.
    """
    conn = get_conn(db_user, db_password, host, database)
    cursor = conn.cursor()
    cursor.execute(sql)
    affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return affected

