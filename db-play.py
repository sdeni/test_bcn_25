# 1. Create DB (SQLite)
# 2. Create table FoodTypes (id, name)
# 3. Create table FoodStuffs (id, name, type_id)
# 4. Insert some data into FoodTypes and FoodStuffs

import sqlite3

conn = sqlite3.connect("food.db")
cursor = conn.cursor()

# cursor.execute("CREATE TABLE FoodTypes (id INTEGER PRIMARY KEY, name TEXT)")
# cursor.execute("CREATE TABLE FoodStuffs (id INTEGER PRIMARY KEY, name TEXT, type_id INTEGER)")
#
# cursor.execute("INSERT INTO FoodTypes (name) VALUES ('Fruit')")
# cursor.execute("INSERT INTO FoodTypes (name) VALUES ('Vegetable')")
# cursor.execute("INSERT INTO FoodTypes (name) VALUES ('Meat')")
# cursor.execute("INSERT INTO FoodTypes (name) VALUES ('Dairy')")
# cursor.execute("INSERT INTO FoodTypes (name) VALUES ('Berry')")
#
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Apple', 1)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Banana', 1)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Orange', 1)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Carrot', 2)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Potato', 2)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Beef', 3)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Pork', 3)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Milk', 4)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Cheese', 4)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Strawberry', 5)")
# cursor.execute("INSERT INTO FoodStuffs (name, type_id) VALUES ('Raspberry', 5)")
#
# conn.commit()

cursor.execute("SELECT * FROM FoodTypes")

for row in cursor.fetchall():
    print(row)

# type_id = "1 UNION SELECT name, 1 FROM FoodStuffs WHERE 1=1"
type_id = "1 UNION SELECT name, 1 FROM FoodStuffs WHERE 1=1"

cursor.execute("SELECT FoodStuffs.name, FoodTypes.name "
               "FROM FoodStuffs "
               "INNER JOIN FoodTypes ON FoodStuffs.type_id = FoodTypes.id"
               f" WHERE FoodStuffs.type_id = ?", (type_id,))
for row in cursor.fetchall():
    print(row)

conn.close()