import openai
import snowflake.connector
import os

# -------------------------
# 🔐 Configuration
# -------------------------

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-openai-key"

# Snowflake credentials (you can also use environment variables here)
SNOWFLAKE_CONFIG = {
    "user": "your_user",
    "password": "your_password",
    "account": "your_account",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema",
}

# -------------------------
# 🧠 Generate SQL from natural language
# -------------------------


def generate_sql(question, table_metadata):
    prompt = f"""
You are a Snowflake SQL expert.
Generate a Snowflake SQL query based on the question below, using the provided table metadata only.

Table Metadata:
{table_metadata}

Question: "{question}"

SQL:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"-- Error generating SQL: {e}"


# -------------------------
# 🧩 Execute the SQL query on Snowflake
# -------------------------


def run_query(query: str):
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return f"Error executing query: {e}"


# -------------------------
# 📊 Format the result
# -------------------------


def format_result(result):
    if isinstance(result, str):
        return result  # error message
    if not result:
        return "No data found."
    return "\n".join([str(row) for row in result])


# -------------------------
# 💬 Chatbot logic
# -------------------------


def chatbot(question):
    table_metadata = """
    Table: sales_data
    Columns:
        - date (DATE)
        - region (VARCHAR)
        - product (VARCHAR)
        - quantity (INTEGER)
        - revenue (FLOAT)
    """
    sql = generate_sql(question, table_metadata)
    print(f"\n📝 Generated SQL:\n{sql}\n")

    result = run_query(sql)
    return format_result(result)


# -------------------------
# 🚀 Run the chatbot
# -------------------------

if __name__ == "__main__":
    print("🔍 Snowflake Chatbot. Ask me about your data!")
    print("Type 'exit' to quit.\n")
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            break
        answer = chatbot(q)
        print("🤖 Answer:\n", answer)
