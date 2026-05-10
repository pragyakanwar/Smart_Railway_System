# Smart Railway Entry Control System

A QR-based Smart Railway Entry Control System developed using Python, Flask, OpenCV, and SQLite to automate passenger ticket verification and regulate platform entry.

The system scans QR-based railway tickets in real time, validates ticket authenticity, prevents duplicate entries, and maintains entry records using a database system.

---

## Features

* QR-based ticket verification
* Real-time QR code scanning using OpenCV
* Flask-based web application
* Detection of Valid, Invalid, and Duplicate tickets
* SQLite database integration for ticket records
* Entry logging and scan tracking
* Audio alerts for unauthorized access
* Dashboard displaying scan statistics and system status

---

## Technologies Used

* Python
* Flask
* OpenCV
* SQLite
* HTML/CSS
* QRCode Library

---

## Project Structure

```bash id="v0d6i8"
├── static/
├── templates/
├── app.py
├── database.db
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Clone the Repository

```bash id="5uoq1f"
git clone https://github.com/yourusername/railway-entry-control-system.git
```

### 2. Navigate to the Project Folder

```bash id="e9m9cu"
cd railway-entry-control-system
```

### 3. Install Dependencies

```bash id="z88sm1"
pip install -r requirements.txt
```

### 4. Run the Application

```bash id="5c6x7x"
python app.py
```

---

## Working of the System

1. The system scans QR codes from railway tickets using a camera.
2. Ticket data is verified with stored database records.
3. Tickets are classified as:

   * Valid
   * Invalid
   * Duplicate
4. Entry records are stored automatically in the database.
5. Dashboard analytics display total scans and access status.

---

## Future Improvements

* Face recognition integration
* Cloud database support
* Online ticket API integration
* Admin login authentication
* Real-time analytics dashboard
* Deployment on cloud platforms

---

## Project Screenshots

### QR Ticket Verification

(Add screenshot here)

### Dashboard Interface

(Add screenshot here)

### Entry Log System

(Add screenshot here)

---

## Author

Pragya Kanwar
B.Tech – Artificial Intelligence & Data Science
