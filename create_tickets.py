import sqlite3
import qrcode
from datetime import datetime, timedelta

print("Creating demo tickets...")

conn = sqlite3.connect("railway.db")
cursor = conn.cursor()

# Remove old tickets
cursor.execute("DELETE FROM tickets")

tickets = [
("T1001","travel"),
("T1002","travel"),
("T1003","travel"),
("T1004","travel"),
("T1005","travel"),
("T2001","platform"),
("T2002","platform")
]

for ticket_id, ticket_type in tickets:

    expiry = datetime.now() + timedelta(hours=2)

    cursor.execute(
        "INSERT INTO tickets(ticket_id,ticket_type,station,valid_until,used) VALUES (?,?,?,?,?)",
        (ticket_id, ticket_type, "Bikaner Junction", expiry.strftime("%Y-%m-%d %H:%M:%S"), 0)
    )

    # Generate QR code
    img = qrcode.make(ticket_id)
    img.save(f"{ticket_id}.png")

    print("Created ticket:", ticket_id)

conn.commit()
conn.close()

print("All tickets created successfully")