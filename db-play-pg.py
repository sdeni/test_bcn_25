# 1. Create DB (PostgreSQL)
# 2. Create table FoodTypes (id, name)
# 3. Create table FoodStuffs (id, name, type_id)
# 4. Insert some data into FoodTypes and FoodStuffs
import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=mysecretpassword")

cursor = conn.cursor()

# cursor.execute("CREATE TABLE FoodTypes (id SERIAL PRIMARY KEY, name TEXT)")
# cursor.execute("CREATE TABLE FoodStuffs (id SERIAL PRIMARY KEY, name TEXT, type_id INTEGER)")
#
# cursor.execute("INSERT INTO FoodTypes (name) VALUES ('Fruit')")
#
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Apple', 1)")
#
# conn.commit()

# show all tables
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

# print it
tables = cursor.fetchall()
for row in tables:
    print(row)

# select top 10 rows from every table
for table in tables:
    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 20")
    print(f"Table: {table[0]}")
    for row in cursor.fetchall():
        print(row)

#
# cursor.execute("SELECT * FROM FoodTypes")
#
# for row in cursor.fetchall():
#     print(row)
#
# cursor.execute("SELECT FoodStuffs.name, FoodTypes.name "
#                 "FROM FoodStuffs "
#                 "INNER JOIN FoodTypes ON FoodStuffs.type_id = FoodTypes.id")
#
# for row in cursor.fetchall():
#     print(row)