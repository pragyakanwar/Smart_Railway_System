import cv2
import sqlite3
import winsound
import time
from datetime import datetime

def main():
 station_name = "Bikaner Junction"
 people_inside = 0
 last_scan_time = 0

 cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
 if not cap.isOpened():
    print("Camera could not be opened")
    return
 detector = cv2.QRCodeDetector()

 while True:
 
    ret, frame = cap.read()

   
    if not ret:
        continue

    data, bbox, _ = detector.detectAndDecode(frame)

    if bbox is not None:
        for i in range(len(bbox)):
            pt1 = tuple(map(int, bbox[i][0]))
            pt2 = tuple(map(int, bbox[(i+1) % len(bbox)][0]))
            cv2.line(frame, pt1, pt2, (255,0,0), 3)

    if data and time.time() - last_scan_time > 3:

        last_scan_time = time.time()

        ticket_id = data
        print("Scanned Ticket:", ticket_id)

        conn = sqlite3.connect("railway.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        ticket = cursor.fetchone()

        ticket_type = "unknown"
        status = "denied"

        if ticket:

            ticket_type = ticket[1]
            valid_until = ticket[3]
            used = ticket[4]

            expiry_time = datetime.strptime(valid_until,"%Y-%m-%d %H:%M:%S")

            if datetime.now() > expiry_time:

                print("Ticket expired")

                winsound.Beep(500,300)

                cv2.putText(frame,"TICKET EXPIRED",(50,60),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

                status = "denied"

            elif used == 1:

                print("Ticket already used")

                winsound.Beep(500,300)

                cv2.putText(frame,"ACCESS DENIED",(50,60),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

                status = "denied"

            else:

                print("Valid Ticket")

                winsound.Beep(1000,200)

                cv2.putText(frame,"GATE OPEN",(50,60),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

                cursor.execute("UPDATE tickets SET used=1 WHERE ticket_id=?", (ticket_id,))
                conn.commit()

                people_inside += 1
                status = "allowed"

        else:

            print("Invalid Ticket")

            winsound.Beep(500,300)

            cv2.putText(frame,"INVALID TICKET",(50,60),
            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

            status = "denied"

        cursor.execute(
            "INSERT INTO entry_logs(ticket_id,ticket_type,status,entry_time) VALUES (?,?,?,?)",
            (ticket_id, ticket_type, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

        conn.commit()
        conn.close()

    cv2.putText(frame,f"Station: {station_name}",(50,200),
    cv2.FONT_HERSHEY_SIMPLEX,0.7,(200,200,200),2)

    cv2.putText(frame,f"Passengers Inside: {people_inside}",(50,230),
    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)

    cv2.imshow("Smart Railway Scanner", frame)

    if cv2.waitKey(1) == 27:
        break

 cap.release()
 cv2.destroyAllWindows()