# 📊 Natural-Language-to-Database-Query-Generator-Chatbot

A **Streamlit-based chatbot** that lets users query a **MySQL database** using **natural language**.  
It automatically generates SQL queries from user input, executes them on the database, and displays results.  
All interactions are logged into a `chat_logs` table for auditing.  

---

## 🚀 Features
- 🔑 User authentication for DB connection  
- 🤖 Natural Language → SQL query generation using the **Groq API**  
- 🗂️ Automatic schema discovery (fetches tables & columns)  
- ⚡ Executes both **read (SELECT)** and **write (INSERT/UPDATE/DELETE)** queries  
- 📊 Displays results as interactive tables in Streamlit  
- 📝 Logs all interactions in MySQL (`chat_logs` table)  
- 🔍 Option to test Groq API connection and view past logs  

> Unlike simple NL chatbots that only generate queries, this project **executes the queries** and returns real results.

---

## 🛠️ Project Structure
```
├── app.py                # Main Streamlit app
├── db.py                 # DB connection + query execution
├── schema_discovery.py   # Schema fetch & format for Groq
├── groq_client.py        # Groq API client for SQL generation
├── logger.py             # Logging interactions into DB
├── requirements.txt      # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/Natural-Language-to-Database-Query-Generator-Chatbot.git
cd Natural-Language-to-Database-Query-Generator-Chatbot
```

### 2️⃣ Create and activate a virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables
Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🗄️ Database Setup
Ensure you have a running **MySQL database**.  

Create a table for logging interactions:
```sql
CREATE TABLE chat_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    user_input TEXT,
    generated_sql TEXT,
    action_type VARCHAR(20),
    status VARCHAR(20),
    details TEXT,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ▶️ Run the App
```bash
streamlit run app.py
```
Open the app in your browser (default: `http://localhost:8501`).

---

## ✅ Usage Flow
1. Enter your **name** and **DB credentials** (username, password, host, database).  
2. Type a natural language query, for example:  
   ```
   Show me all employees in Sales
   ```
3. The app will:  
   - Fetch schema from DB  
   - Generate SQL using Groq API  
   - Execute the query  
   - Display results or number of affected rows  
   - Log the interaction  

4. Optionally test Groq API connection or view past logs.  
5. Disconnect safely when done.  

---

## 📦 Requirements
Dependencies are listed in `requirements.txt`:
```
streamlit==1.26.0
mysql-connector-python==8.1.0
pandas==2.1.1
python-dotenv==1.0.0
groq==0.1.1
```

---

## 🙌 Credits
- [Streamlit](https://streamlit.io/) – UI framework  
- [Groq API](https://groq.com/) – Natural Language → SQL generation  
- [MySQL](https://www.mysql.com/) – Backend database  

---
