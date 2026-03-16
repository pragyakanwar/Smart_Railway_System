import sqlite3

conn = sqlite3.connect("railway.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM entry_logs")
cursor.execute("UPDATE tickets SET used = 0")

conn.commit()
conn.close()

print("System reset complete")