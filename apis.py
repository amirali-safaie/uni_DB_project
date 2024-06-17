import mysql.connector
import os
from dotenv import load_dotenv


#import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')
print(mysql_password)

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = mysql_password
    # create a database in your local system and create the table 
    # add this field :
    #database = "your database name"
)

print("succesfully conected")

