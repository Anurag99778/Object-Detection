import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='An@210803',
            database='OBJECT_DETECTION'
        )
        self.cursor = self.conn.cursor()

    def insert_detection(self, detection):
        object_name = detection['object']
        count = detection['count']
        date = detection['date']

        self.cursor.execute("INSERT INTO count_detections (object, count, last_detected) VALUES (%s, %s, %s)",
                            (object_name, count, date))
        print(f"Inserted count in database for {object_name}: {count} at {date}")

        self.conn.commit()

    def __del__(self):
        self.conn.close()
