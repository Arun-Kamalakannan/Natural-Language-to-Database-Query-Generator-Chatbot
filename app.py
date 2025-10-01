import streamlit as st
import pandas as pd
from schema_discovery import fetch_schema, format_schema_for_groq
from groq_client import generate_sql_from_nl, test_groq_connection
from db import fetch_query, execute_query  # <-- include execute_query for write operations
from logger import log_interaction

# Set Streamlit page configuration
st.set_page_config(page_title="DB Chatbot", layout="wide")

# --- STEP 1: User login ---
# Use Streamlit session_state to maintain login details
if "app_user" not in st.session_state:
    st.title("Welcome to DB Chatbot")

    # Take input details for logs and DB connection
    app_user = st.text_input("Enter your name (for activity logs)")
    db_user = st.text_input("DB username")
    db_password = st.text_input("DB password", type="password")
    db_host = st.text_input("DB host", value="localhost")
    db_name = st.text_input("Database name")

    # Connect button
    if st.button("Connect"):
        if not app_user or not db_user or db_password is None or not db_name:
            st.warning("Please fill in all fields.")
        else:
            # Store user and DB details in session state
            st.session_state.app_user = app_user
            st.session_state.db_user = db_user
            st.session_state.db_password = db_password
            st.session_state.db_host = db_host
            st.session_state.db_name = db_name
            st.success(f"Connected as {app_user}")
            st.experimental_rerun()

    # Stop further execution until user logs in
    st.stop()

# --- STEP 2: Main Chat Interface ---
st.title("DB Chatbot Interface")

# --- Input NLP query ---
user_input = st.text_area("Enter your query (Natural Language)", height=100)

# Submit button for query
if st.button("Submit Query"):
    if not user_input.strip():
        st.warning("Please enter a query.")
    else:
        # STEP 3: Fetch database schema for GPT (helps NL-to-SQL conversion)
        try:
            schema_dict = fetch_schema(
                db_user=st.session_state.db_user,
                db_password=st.session_state.db_password,
                host=st.session_state.db_host,
                database=st.session_state.db_name,
            )
            schema_hint = format_schema_for_groq(schema_dict)
        except Exception:
            schema_hint = ""  # If schema fetch fails, continue without it

        # STEP 4: Generate SQL from natural language using Groq API
        generated_sql = generate_sql_from_nl(user_input, schema_hint)

        if generated_sql:
            st.subheader("Generated SQL")
            st.code(generated_sql)

            # Decide if the query is READ (SELECT) or WRITE (INSERT/UPDATE/DELETE)
            query_lower = generated_sql.strip().lower()
            action_type = "READ" if query_lower.startswith("select") else "WRITE"

            # STEP 5: Execute the generated SQL
            try:
                if action_type == "READ":
                    # For SELECT queries → fetch data
                    cols, rows = fetch_query(
                        generated_sql,
                        db_user=st.session_state.db_user,
                        db_password=st.session_state.db_password,
                        host=st.session_state.db_host,
                        database=st.session_state.db_name,
                    )
                    df = pd.DataFrame(rows, columns=cols)
                    st.subheader("Query Results")
                    st.dataframe(df)
                    details = f"Rows returned: {len(df)}"
                else:
                    # For WRITE queries → run execute_query
                    affected = execute_query(
                        generated_sql,
                        db_user=st.session_state.db_user,
                        db_password=st.session_state.db_password,
                        host=st.session_state.db_host,
                        database=st.session_state.db_name,
                    )
                    st.success(f"Query executed successfully. Rows affected: {affected}")
                    details = f"Rows affected: {affected}"

                # STEP 6: Log interaction in chat_logs table
                log_interaction(
                    user_name=st.session_state.app_user,
                    user_input=user_input,
                    generated_sql=generated_sql,
                    action_type=action_type,
                    status="SUCCESS",
                    details=details,
                    db_user=st.session_state.db_user,
                    db_password=st.session_state.db_password,
                    host=st.session_state.db_host,
                    database=st.session_state.db_name,
                )

            except Exception as e:
                # Handle DB execution errors
                st.error(f"Database Execution Error: {str(e)}")
                log_interaction(
                    user_name=st.session_state.app_user,
                    user_input=user_input,
                    generated_sql=generated_sql,
                    action_type=action_type,
                    status="FAILURE",
                    details=str(e),
                    db_user=st.session_state.db_user,
                    db_password=st.session_state.db_password,
                    host=st.session_state.db_host,
                    database=st.session_state.db_name,
                )

# --- STEP 7: Disconnect Button ---
if st.button("Disconnect"):
    # Clear session state values
    for key in ["app_user", "db_user", "db_password", "db_host", "db_name"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Disconnected.")
    st.experimental_rerun()

# --- STEP 8: Test Groq API Connection ---
if st.button("Test API Connection"):
    success, result = test_groq_connection()
    if success:
        st.success(f"✅ Groq API connected! Response: {result}")
    else:
        st.error(f"❌ API Connection failed: {result}")

# --- STEP 9: View Logs from DB ---
st.subheader("View Chat Logs")

if st.button("Show Logs"):
    try:
        # Fetch last 100 logs from chat_logs table
        cols, rows = fetch_query(
            "SELECT * FROM chat_logs ORDER BY log_time DESC LIMIT 100;",
            db_user=st.session_state.db_user,
            db_password=st.session_state.db_password,
            host=st.session_state.db_host,
            database=st.session_state.db_name,
        )
        if rows:
            df_logs = pd.DataFrame(rows, columns=cols)
            st.dataframe(df_logs)
        else:
            st.info("No logs available.")
    except Exception as e:
        st.error(f"Error fetching logs: {str(e)}")
