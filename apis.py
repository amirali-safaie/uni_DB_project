import mysql.connector
 
# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "mysql_password"
)

cursor = mydb.cursor() # create an instance of cursor class to execute mysql commands
cursor.execute("drop database project");

