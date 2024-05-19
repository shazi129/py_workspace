# -*- coding: utf-8 -*-
import requests
import json
import finacial_api
import finacial_db

def get_klines(end_time):
    print("get_klines(122.XAG), end_time:" + end_time)
    get_request = finacial_api.eastmoney_get_request('122.XAG', end_time)
    response = requests.get(get_request).text
    response = json.loads(response)
    if response["data"] != None:
        return response["data"]["klines"]
    else:
        print("response is null!!!!!")
        return []

def save_all_kline():
    file = open("xag.txt", "w")
    end_time = '3000-00-00'
    while True:
        klines = get_klines(end_time)
        if len(klines) == 0:
            break;
        for item in reversed(klines):
            file.write(item + "\n")
            fields = item.split(",")
            if (len(fields) > 0):
                end_time = fields[0]
    file.close()

def parse_kline_to_db():
    file = open("xag.txt", "r")
    klines = reversed(file.readlines())
    file.close()

    connection, cursor = finacial_db.connect_db()
    for item in klines:
        fields = item.split(",")
        finacial_db.stock_table_data["Date"] = fields[0]
        finacial_db.stock_table_data["Open"] = float(fields[1])
        finacial_db.stock_table_data["Close"] = float(fields[2])
        finacial_db.stock_table_data["Hight"] = float(fields[3])
        finacial_db.stock_table_data["Low"] = float(fields[4])
        finacial_db.stock_table_data["CHG"] = round(finacial_db.stock_table_data["Close"] - finacial_db.stock_table_data["Open"], 2)
        finacial_db.stock_table_data["CHG_PCT"] = round(100 * finacial_db.stock_table_data["CHG"] / finacial_db.stock_table_data["Open"], 2)

        finacial_db.write_data(connection, cursor, "XAG", finacial_db.stock_table_data)
        #break


    finacial_db.close_db(connection, cursor)


if __name__ == "__main__":
    finacial_db.update_all_ma("XAG")
    