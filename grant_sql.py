import os
import mysql.connector as mysql
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


PWD = os.environ['MYSQL_ROOT']
PW = os.environ['MYSQL_DB_PASSWORD']

host = 'localhost'
user = 'root'
passwd = PWD

mydb = mysql.connect(host=host, user=user, password=passwd)
cursor = mydb.cursor()

try:
    mkuser = 'wibu212'
    mkpass = PW
    create_then_grant = f"""
        CREATE USER '{mkuser}'@'{host}'
        IDENTIFIED BY '{mkpass}';
        GRANT ALL
        ON *.*
        TO '{mkuser}'@'{host}'
        WITH GRANT OPTION;
    """
    results = cursor.execute(create_then_grant)
    print("User creation and granted returned", results)
except Error as e:
    print(e)

