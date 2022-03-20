import mysql
from mysql.connector import Error
import pypyodbc
mySQLServer = 'DESKTOP-3LTHV48\SQLEXPRESS'
myDatabase = 'Data_base_first'
connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server='+mySQLServer+';'
                            'Database='+myDatabase+';')
cursor = connection.cursor()
mySQLQuery = (
"""
    SELECT id, login, password
    FROM dbo.User_login
    WHERE id='1'

"""
)
cursor.execute(mySQLQuery)
result = cursor.fetchall()
print(result)
connection.close()

# def create_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             password=user_password,
#             database=db_name)
#         print('Соединение успешно')
#     except Error as e:
#         print(f"Ошибка'{e}' произошла")
#     return connection
# connection = create_connection("localhost","root","","first")
#
# def create_database(connection, query):
#     cursor=connection.cursor()
#     try:
#         cursor.execute(query)
#         print('База создана успешно')
#     except Error as e:
#         print(f"Ошибка '{e}' произошла")
# create_database_query = "CREATE DATABASE first"
# create_database(connection, create_database_query)