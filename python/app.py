import psycopg2

conn = psycopg2.connect(
    database = "Zoo",
    user = "postgres",
    password = "",
    host = "localhost",
    port= '5432' 
)

cursor = conn.cursor()

cursor.execute("select * from employees")

data = cursor.fetchall()
for d in data:
    print(d)

conn.close()