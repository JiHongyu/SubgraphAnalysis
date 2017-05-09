import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from itertools import product
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['simsun']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


data = [(0.3648, 3.472), (0.4049, 39.93)]

df = pd.DataFrame(data=data, columns=['NMI', '时间'])

