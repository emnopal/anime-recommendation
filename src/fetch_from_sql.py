import os
import mysql.connector as mysql

from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()
pwd = os.environ['MYSQL_DB_PASSWORD']

from utils.profiling import timeit

@timeit
def connections(host='localhost', user='wibu212', password=pwd):
    try:
        print("Success connect to MySQL!")
        return mysql.connect(host=host, user=user, password=password)
    except:
        raise Exception("Error connecting to MySQL", Error)

@timeit
def connect_to_db(conn, db_name):
    try:
        if conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute(f"use {db_name};")
                print(f"You're connected to database: {db_name}")
                return
            except:
                raise Exception(f"Database {db_name} is not found")
    except Error as e:
        print("Error while connecting to MySQL", e)

@timeit
def connect(db_name='animedb'):
    conn = connections()
    connect_to_db(conn, db_name)
    return conn
