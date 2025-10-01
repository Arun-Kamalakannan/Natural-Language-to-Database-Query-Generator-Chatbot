import os
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

# Load env vars
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    print("Warning: GROQ_API_KEY is not set. Set it in your environment or .env file.")

client = Groq(api_key=groq_api_key)

def test_groq_connection():
    """
    Test Groq API connection by sending a small test prompt.
    Returns tuple (success: bool, message: str)
    """
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
        )
        content = resp.choices[0].message.content.strip() if resp.choices else ""
        return True, content or "ok"
    except Exception as e:
        return False, str(e)

def _strip_code_fence(s: str) -> str:
    """
    Remove surrounding Markdown code fences if present:
    `````` or ``````
    """
    t = s.strip()
    if t.startswith("``````"):
        lines = t.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()
    return t

def generate_sql_from_nl(user_input: str, schema_hint: str) -> Optional[str]:
    """
    Generate ONLY SQL query from natural language using Groq.
    Returns the SQL string or None on error.
    """
    try:
        prompt = f"""You are an SQL generator.
Database schema:
{schema_hint}

Convert the following request into a valid SQL query.
Return ONLY the SQL code without explanation, no markdown, no extra text.

Request: {user_input}"""

        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict SQL generator. Always return only SQL code."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        raw = resp.choices[0].message.content if resp.choices else ""
        sql = _strip_code_fence(raw).strip()

        # Remove stray "sql" language hint if the model included it without fences
        if sql.lower().startswith("sql\n"):
            sql = sql[4:].lstrip()

        return sql
    except Exception as e:
        print(f"Groq Error: {e}")
        return None
