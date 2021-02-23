import mysql.connector

connection_obj_db = mysql.connector.connect(host="localhost", user="root", password="", database="rest")

print(connection_obj_db)
cursor_obj = connection_obj_db.cursor()
selection_obj = "SELECT * FROM basic_app_restaurant"
cursor_obj.execute(selection_obj)
fetched_data = cursor_obj.fetchall()
# print(cursor_obj.rowcount)
# print(fetched_data)
# print(cursor_obj.rowcount)
