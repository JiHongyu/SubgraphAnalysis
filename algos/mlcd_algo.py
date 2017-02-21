from .algo_base import Algorithm
import mlcd

class Mlcd(Algorithm):

    def __init__(self, networks):
        Algorithm.__init__(self, networks)

    def run_algo(self, *args, **kwargs):
        mlcd_algo = mlcd.MNetworkLCD()

        # 1. ������������
        mlcd_algo.set_networks(self.networks)

        # 2. ���������Լ����㷨
        mlcd_algo.set_linkpair_simi_algo(mlcd.linkpair_simi_2)

        # 3. ��������������
        mlcd_algo.cal_linkpair_similarity()

        # 4. �����������Ż��㷨
        mlcd_algo.set_objectfunc_algo(mlcd.objectfunc_by_mean)

        # 5. Ѱ����������
        result = mlcd_algo.cal_optimization_community()

        self.r = result
        return self.r

