from .algo_base import Algorithm
import mlcd

class Mlcd(Algorithm):

    def __init__(self, networks):
        Algorithm.__init__(self, networks)

    def run_algo(self, *args, **kwargs):
        mlcd_algo = mlcd.MNetworkLCD()

        # 1. 载入网络数据
        mlcd_algo.set_networks(self.networks)

        # 2. 设置相似性计算算法
        mlcd_algo.set_linkpair_simi_algo(mlcd.linkpair_simi_2)

        # 3. 计算连边相似性
        mlcd_algo.cal_linkpair_similarity()

        # 4. 设置最优社团划算法
        mlcd_algo.set_objectfunc_algo(mlcd.objectfunc_by_mean)

        # 5. 寻找最优社团
        result = mlcd_algo.cal_optimization_community()

        self.r = result
        return self.r

