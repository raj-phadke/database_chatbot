# 📊 Database Chatbot

A Python-based chatbot that connects to **Snowflake** and allows users to interact with their data warehouse using natural language. It streamlines querying, managing, and writing to Snowflake—making data interaction more accessible to both technical and non-technical users.

---

## 🚀 Features

- 🔗 **Connects to Snowflake** securely via Snowflake Connector.
- 💬 **Natural Language Interface** (future integration) to simplify querying and interacting with Snowflake data.
- 📝 **Write Data** to Snowflake or local filesystem using structured writers.
- ✅ Automatically creates Snowflake tables if they do not exist.
- 📦 Modular design with plug-and-play support for different writers (e.g., Snowflake, Local CSV).
- 🧱 Built with extensibility in mind (easily support more databases).

---

## 🧪 Sample Workflow

### 1. Generate and Write Sample Data to Snowflake

```bash
python src/samples/scripts/write_sample_data_to_snowflake.py
