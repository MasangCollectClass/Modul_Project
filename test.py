import sqlite3

conn = sqlite3.connect("mbti_places.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM places")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()