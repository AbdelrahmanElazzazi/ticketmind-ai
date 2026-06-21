import sqlite3

conn = sqlite3.connect("review_queue.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM review_queue")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()