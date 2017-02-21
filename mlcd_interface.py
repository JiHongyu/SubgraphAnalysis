import matplotlib.pyplot as plt

import mlcd

simi_func = mlcd.linkpair_simi_2
obj_func = mlcd.objectfunc_by_max

def mlinkcoms_algo(mnetworks, path):

    # 多网络连边社团检测算法对象
    lcd_algo = mlcd.MNetworkLCD()

    # 1. 载入网络数据
    print('1. 载入网络数据')
    lcd_algo.set_networks(mnetworks)

    # 2. 设置相似性计算算法
    print('2. 设置相似性计算算法')
    lcd_algo.set_linkpair_simi_algo(simi_func)

    # 3. 计算连边相似性
    print('3. 计算连边相似性')
    lcd_algo.cal_linkpair_similarity()

    # 4. 设置最优社团划算法
    print('4. 设置最优社团划算法')
    lcd_algo.set_objectfunc_algo(obj_func)

    # 5. 寻找最优社团
    print('5. 寻找最优社团')
    result = lcd_algo.cal_optimization_community()

    # 6. 获取系统树图
    print('6. 获取系统树图')
    lcd_algo.dump_dendrogram(path='.\\result\\')

    # 7. 生成 gml 文件
    print('7. 生成 gml 文件吧')

    return result
