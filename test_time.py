import time

'''
时间戳
'''
ts = time.time()
print(ts)


'''
时间结构体
'''
struct_time = time.localtime(ts)
print(struct_time)
print(struct_time.tm_year)

'''
格式化时间
'''
localtime = time.asctime(struct_time)
print(localtime)

time_str = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
print(time_str)

'''
格式化字符串->时间
'''
struct_time = time.strptime(time_str,"%Y-%m-%d %H:%M:%S")
print(time.mktime(struct_time))