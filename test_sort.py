a = [[3, 1, 4], [8, 5, 7]]
a = [sorted(item) for item in a]


b = [5,6,8]

d = {1:"a", 4:"b", 3:"c"}

print(a)
print(sorted(list(d.keys())) in a)
print([(key, d[key]) for key in sorted(d)])

print(b.index(6))