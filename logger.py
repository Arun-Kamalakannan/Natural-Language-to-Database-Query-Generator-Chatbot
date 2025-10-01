from db import execute_query, get_conn
from datetime import datetime

def log_interaction(
    user_name,
    user_input,
    generated_sql,
    action_type="READ",
    status="SUCCESS",
    details="",
    db_user=None,
    db_password=None,
    host=None,
    database=None,
):
    """
    Logs user interaction into chat_logs table using the provided DB credentials.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_sql = """
    INSERT INTO chat_logs (user_name, user_input, generated_sql, action_type, status, details, log_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    conn = None
    try:
        conn = get_conn(db_user=db_user, db_password=db_password, host=host, database=database)
        cursor = conn.cursor()
        cursor.execute(
            insert_sql,
            (user_name, user_input, generated_sql, action_type, status, details, timestamp),
        )
        conn.commit()
        cursor.close()
    finally:
        if conn:
            conn.close()

