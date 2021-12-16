"""
Here i'm using MySQL to store the data.
"""

import os
import mysql.connector as mysql
import pandas as pd

from mysql.connector import Error
from dotenv import load_dotenv
from utils.profiling import timeit

load_dotenv()

pwd = os.environ['MYSQL_DB_PASSWORD']

class ToSQL:
    def __init__(self, host='localhost', user='wibu212', password=pwd):
        self.conn = mysql.connect(host=host, user=user, password=password)

    @timeit
    def from_csv(self, csv_files, db_name, table_name, query):
        df = pd.read_csv(csv_files)
        try:
            if self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute(f"create database if not exists {db_name};")
                print(f"Database: {db_name} is created")
                cursor.execute(f"use {db_name};")
                print(f"You're connected to database: {db_name}")
                cursor.execute(f'DROP TABLE IF EXISTS {table_name};')
                print('Creating table....')
                cursor.execute(query)
                print("Table is created....")
                for i, row in df.iterrows():
                    if 'auto_increment' in query:
                        sql = f"INSERT INTO {db_name}.{table_name} VALUES {tuple({i+1}) + tuple('%s' for _ in range(len(df.columns)))}"
                    else:
                        sql = f"INSERT INTO {db_name}.{table_name} VALUES {tuple('%s' for _ in range(len(df.columns)))}"
                    cursor.execute(sql, tuple(row))
                    self.conn.commit()
                print(f"Success convert {csv_files} to MySQL db")
                return
        except Error as e:
            print("Error while connecting to MySQL", e)
