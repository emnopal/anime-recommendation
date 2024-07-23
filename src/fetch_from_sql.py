import os
import mysql.connector as mysql

from mysql.connector import Error
from dotenv import load_dotenv

from utils.profiling import timeit

load_dotenv()
pwd = os.environ['MYSQL_DB_PASSWORD']

@timeit
def connections(host='localhost', user='wibu212', password=pwd):
    print("Success connect to MySQL!")
    return mysql.connect(host=host, user=user, password=password)

@timeit
def connect_to_db(conn, db_name):
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"use {db_name};")
            print(f"You're connected to database: {db_name}")
    except Error as e:
        print("Error while connecting to MySQL", e)

@timeit
def connect(db_name='animedb'):
    conn = connections()
    connect_to_db(conn, db_name)
    return conn
