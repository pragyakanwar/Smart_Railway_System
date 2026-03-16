import sqlite3

conn = sqlite3.connect("railway.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(
ticket_id TEXT PRIMARY KEY,
ticket_type TEXT,
station TEXT,
valid_until TEXT,
used INTEGER
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS entry_logs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
ticket_id TEXT,
ticket_type TEXT,
status TEXT,
entry_time TEXT
)
""")

conn.commit()
conn.close()

print("Database created")