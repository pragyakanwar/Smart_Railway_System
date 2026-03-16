from flask import Flask, render_template
import sqlite3
import qrcode
from datetime import datetime, timedelta
from flask import request
import threading
import scanner

app = Flask(__name__)


def get_db():
    return sqlite3.connect("railway.db", timeout=10)



@app.route("/")
def dashboard():

    conn = get_db()
    cursor = conn.cursor()

    # total scans
    cursor.execute("SELECT COUNT(*) FROM entry_logs")
    total = cursor.fetchone()[0]

    # allowed
    cursor.execute("SELECT COUNT(*) FROM entry_logs WHERE status='allowed'")
    allowed = cursor.fetchone()[0]

    # denied
    cursor.execute("SELECT COUNT(*) FROM entry_logs WHERE status='denied'")
    denied = cursor.fetchone()[0]

    # recent entries
    cursor.execute("""
        SELECT ticket_id,ticket_type,status,entry_time
        FROM entry_logs
        ORDER BY id DESC
        LIMIT 10
    """)
    logs = cursor.fetchall()

    # activity feed
    cursor.execute("""
        SELECT ticket_id,ticket_type,status,entry_time
        FROM entry_logs
        ORDER BY id DESC
        LIMIT 15
    """)
    activity = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        allowed=allowed,
        denied=denied,
        logs=logs,
        activity=activity
    )


@app.route("/scanner")
def scanner_page():
    return render_template("scanner.html")


@app.route("/logs")
def logs_page():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ticket_id,ticket_type,status,entry_time
        FROM entry_logs
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()
    conn.close()

    return render_template("logs.html", logs=logs)


@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/generate", methods=["GET","POST"])
def generate_ticket():

    if request.method == "POST":

        ticket_id = request.form["ticket_id"]
        ticket_type = request.form["ticket_type"]

        expiry = datetime.now() + timedelta(hours=2)

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tickets(ticket_id,ticket_type,valid_until,used) VALUES (?,?,?,?)",
            (ticket_id, ticket_type, expiry.strftime("%Y-%m-%d %H:%M:%S"), 0)
        )

        conn.commit()
        conn.close()

        # generate QR
        img = qrcode.make(ticket_id)
        img.save(f"static/{ticket_id}.png")

        return render_template("generate.html",qr=f"static/{ticket_id}.png", ticket_id=ticket_id)

    return render_template("generate.html", qr=None)


if __name__ == "__main__":

    scanner_thread = threading.Thread(target=scanner.main)
    scanner_thread.daemon = True
    scanner_thread.start()

    app.run(debug=True,use_reloader=False)