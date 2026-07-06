from services.db import get_connection

conn = get_connection()

print("CONNECTED")

cur = conn.cursor()

cur.execute("SELECT version();")

print(cur.fetchone())

cur.close()
conn.close()