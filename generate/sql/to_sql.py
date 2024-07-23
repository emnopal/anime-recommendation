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

USER = 'root'
PWD_USER = os.environ['MYSQL_ROOT']
HOST = 'localhost'

class ToSQL:
    def __init__(self, host=None, user=None, password=None):
        self.conn = mysql.connect(host=host or HOST, user=user or USER, password=password or PWD_USER)

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

                print('Creating table....')
                cursor.execute(query)
                print("Table is created....")

                for i, row in df.iterrows():

                    _db_name = f"{db_name}.{table_name}"

                    columns = ', '.join(df.columns)
                    placeholders = ', '.join(['%s'] * (len(df.columns)))

                    if 'auto_increment' in query:
                        sql = f"INSERT INTO {_db_name} (animeIndex, {columns}) VALUES ({i+1}, {placeholders})"
                    else:
                        sql = f"INSERT INTO {_db_name} ({columns}) VALUES {placeholders}"

                    print(f"Converting row {i+1} ({row[1]}) to MySQL db")
                    cursor.execute(sql, tuple(row))
                    self.conn.commit()

                print(f"Success convert {csv_files} to MySQL db")
        except Error as e:
            print("Error while connecting to MySQL", e)
