import matplotlib.pyplot as plt

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['simsun']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# import numpy as np
# context_data = []
# with open('fanmod_ca.txt.csv','r') as f:
#     for line in f:
#         if line.find('%') != -1:
#             context_data.append(line)
#
# data = []
#
# for each in context_data:
#     data.append(each.split(','))
#
# p = []
# for d in data:
#     x = np.float64(d[2][:-1])/100
#     if np.fabs(x) > 0.0000001:
#         p.append(x)
#
# h = sum((-x*np.log(x) for x in p))
# print(h)
x = [3, 4, 5, 6, 7]

ba = [0.1392,0.9619,1.543,2.479,3.387]

ws = [0.3671,0.9251,1.463,2.215,2.949]

ca = [0.1672, 0.8070, 1.286, 2.000]

plt.figure(1, figsize=(4, 3))
plt.plot(x, ba, ':+', label='BA网络')
plt.plot(x, ws, '--x', label='WS网络')
plt.plot(x[:-1], ca, '-*', label='真实网络')
plt.xticks(x, x, rotation=0)
plt.xlabel('模体阶数')
plt.ylabel('信息熵')
plt.legend()
plt.show()
