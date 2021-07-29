import os

'''
本python文件路径
'''
this_file_path = os.path.abspath(__file__)
print(this_file_path)

'''
路径分割
'''
path_name, file_name = os.path.split(this_file_path)
print(path_name)
print(file_name)

'''
路径拼接
'''
ml_path = os.path.join(path_name, "ML/")
print(ml_path)

'''
遍历
'''
for item in os.walk(ml_path, topdown=True):
    print(item)


'''
列出目录下类容
'''
content = os.listdir(path_name)
print(content)

'''
是目录还是文件
'''
content = [os.path.join(path_name, item) for item in content]
for item in content:
    print("%s is dir: %s, is file:%s" % (item, os.path.isdir(item), os.path.isfile(item)))

print(os.path.isabs(this_file_path))
print(os.path.isabs("./"))