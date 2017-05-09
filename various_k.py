import matplotlib.pyplot as plt
import pandas as pd
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['simsun']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

col_name = ['node', 'edge', 'd', 'q', 'dim', 'ad']
data = [(1000, 2000, 4, 0.596, 8, 4.158),
        (851, 1482, 3.483, 0.581, 10, 4.404),
        (320, 507, 3.169, 0.649, 9, 4.036),
        (66, 106, 3.212, 0.559, 7, 3.027),
        (10, 13, 2.6, 0.311, 4, 2.133)]

x = [0, 1, 2, 3, 4]

df = pd.DataFrame(data=data, columns=col_name)


fig = plt.figure(1, figsize=(4, 3))

ax1 = fig.add_subplot(111)
ax1.plot(x, df['node'], '-*', label='节点数')
ax1.set_ylabel('节点数')

ax2 = ax1.twinx()  # this is the important function
ax2.plot(x, df['edge'], '-*r', label='边数')
ax2.set_ylabel('边数')
ax2.set_xlabel('邻域半径 $k$')

plt.legend()
plt.show()