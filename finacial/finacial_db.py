# -*- coding: utf-8 -*-

import os
import sqlite3

stock_table_data = {
    "Date": "",
    "Open": 0,
    "Close": 0,
    "Hight": 0,
    "Low": 0,
    "CHG": 0,
    "CHG_PCT": 0,
}

def connect_db():
    current_file_path = os.path.abspath(__file__)
    current_directory_path = os.path.dirname(current_file_path)
    connection = sqlite3.connect('%s/finacial_data.db' % current_directory_path)
    if connection == None:
        print("connect db error")
        return
    cursor = connection.cursor()
    return connection, cursor

def create_stock_table(connection, cursor, table_name):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS XAG(
            Date DATE primary key,
            Open REAL,
            Close REAL,
            Hight REAL,
            Low REAL,
            CHG REAL,
            CHG_PCT REAL,
            MA5 REAL,
            MA10 REAL,
            MA20 REAL,
            MA30 REAL,
            MA60 REAL,
            MA120 REAL,
            MA250 REAL
        )
        """
    )
    connection.commit()

def write_data(connection, cursor, table, data):
    cols = ""
    values = ""
    for k, v in data.items():
        prefix = ""
        if cols != "":
            prefix = ", "
        if isinstance(v, str):
            v = "'%s'" % v
        else:
            v = str(v)
        cols += prefix + k
        values += prefix + v

    sql = 'INSERT INTO %s(%s) VALUES(%s)' % (table, cols, values)
    print(sql)

    try:
        cursor.execute(sql)
        connection.commit()
    except sqlite3.IntegrityError as e:
        print("Insert error: ", e.sqlite_errorname)

def update_all_ma(table):
    connection, cursor = connect_db()
    sql = "select * from %s Order by Date DESC" % table
    cursor.execute(sql)
    results = cursor.fetchall()

    for ma_size in (10, 20, 30, 60, 120, 250):
        ma_cache_list = []
        for i in range(len(results)):
            if i < ma_size:
                ma_cache_list.append(results[i][2])
                continue
            ma = round(sum(ma_cache_list) / ma_size, 2)
            sql = "update %s Set MA%d=%f where Date='%s'" % (table, ma_size, ma, results[i-ma_size][0])
            print(sql)
            cursor.execute(sql)
            connection.commit()
            if (i + 1 < len(results)):
                del ma_cache_list[0]
                ma_cache_list.append(results[i+1][2])
    close_db(connection, cursor)

def close_db(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()