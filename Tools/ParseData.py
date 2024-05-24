import os

data_file_path = os.path.abspath(__file__)
data_file = "%s/Data.txt" % os.path.dirname(data_file_path)

file = open(data_file, "r")
lines = file.readlines()

summary = [0, 0, 0, 0, 0, 0, 0]
for item in lines:
    summary[int(item.strip()) - 1] += 1

print(summary)