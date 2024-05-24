
# -*- coding: utf-8 -*-

import requests
import json

#####东方财富api
url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"

get_param = {
    "secid": '122.XAG',
    "end": "20240101",
    "fields1" : 'f1,f2,f3,f4,f5',
    "fields2": 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
    "lmt":58,
    "klt":101,
    "fqt":1,
    "ut": "fa5fd1943c7b386f172d6893dbfba10b"
}

def create_get_request(code, endtime):
    get_param["secid"] = code
    get_param["end"] = endtime.replace("-", "")

    get_param_str = ""
    for k, v in get_param.items():
        if get_param_str == "":
            get_param_str += "%s=%s" % (k, v)
        else:
            get_param_str += "&%s=%s" % (k, v)
    return "%s?%s" % (url, get_param_str)

def get_klines(code, end_time):
    real_code = "122.%s" % code
    print("get_klines(%s), end_time:%s" % (real_code, end_time))
    get_request = create_get_request(real_code, end_time)
    response = requests.get(get_request).text
    response = json.loads(response)
    if response["data"] != None:
        return response["data"]["klines"]
    else:
        print("response is null!!!!!")
        return []
    

def save_all_kline_to_file(code, filename):
    file = open(filename, "w")
    end_time = '3000-00-00'
    while True:
        klines = get_klines(code, end_time)
        if len(klines) == 0:
            break
        new_end_time = ""
        for item in reversed(klines):
            file.write(item + "\n")
            fields = item.split(",")
            if (len(fields) > 0):
                new_end_time = fields[0]

        if new_end_time == end_time:
            break
        else:
            end_time = new_end_time
    file.close()