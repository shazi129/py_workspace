
# -*- coding: utf-8 -*-


#####东方财富api
eastmoney_url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"

eastmoney_get_param = {
    "secid": '122.XAG',
    "end": "20240101",
    "fields1" : 'f1,f2,f3,f4,f5',
    "fields2": 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
    "lmt":58,
    "klt":101,
    "fqt":1,
    "ut": "fa5fd1943c7b386f172d6893dbfba10b"
}

def eastmoney_get_request(code, endtime):
    eastmoney_get_param["secid"] = code
    eastmoney_get_param["end"] = endtime.replace("-", "")

    get_param_str = "";
    for k, v in eastmoney_get_param.items():
        if get_param_str == "":
            get_param_str += "%s=%s" % (k, v)
        else:
            get_param_str += "&%s=%s" % (k, v)
    return "%s?%s" % (eastmoney_url, get_param_str)