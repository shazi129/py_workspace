import numpy as np 
from matplotlib import pyplot as plt 

plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

x = np.arange(0,160)

print(x)
y =  -np.power((x - 80), 2) +  100000 


dot_x = [10, 50, 80, 100, 120, 150]
dot_y = [96100, 99100, 100100, 99500, 98840, 95100]

plt.xlabel("平米") 
plt.ylabel("单价") 
plt.plot(x,y) 
plt.scatter(dot_x, dot_y, color='red', marker='+')
plt.show()