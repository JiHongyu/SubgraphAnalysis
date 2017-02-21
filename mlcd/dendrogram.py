from .edge import Edge

class TreeNode:
    Cnt = 0

    def __init__(self, info="node", parent=None):
        # 节点信息
        self.info = info
        # 父节点
        self.parent = parent
        # 子节点集
        self.children = []
        # 节点深度
        self.depth = 0
        # 节点关联相似度
        self.simi = 0.0
        # 节点编号
        self.cnt = TreeNode.Cnt
        # 节点计数
        TreeNode.Cnt += 1
        # 子树叶子节点集
        self.leaves = set()

        if isinstance(info, Edge):
            self.leaves.add(info)
            self.simi = 1.0



    def merge_subtree(self, tree):


        self.children.extend(tree.children)

        for child in tree.children:
            child.parent = self

        self.leaves.update(tree.leaves)

        pass

    @classmethod
    def merge_tree(cls, tree1, tree2, simi):

        return cls.merge_trees((tree1,tree2,), simi)

    @classmethod
    def merge_trees(cls, trees, simi):

        new_node = TreeNode(info="inner")

        for tree in trees:
            new_node.children.append(tree)

            tree.parent = new_node

            new_node.leaves.update(tree.leaves)

            new_node.depth = max(tree.depth+1, new_node.depth)
        new_node.simi = simi
        return new_node

    def __hash__(self):
        return self.cnt


class Dendrogram:
    """docstring for DendroGram"""

    def __init__(self, node_pairs_data, node_set):
        """
        系统树构造函数
        :param node_pairs_data: 原始系统树节点关系数据（已排好序）
        :param node_set: 原始系统树节点
        """
        self.__node_pairs_data = node_pairs_data
        self.__node_set = node_set

        self.__pair_used = 0
        self.__pair_redu = 0

        self.__inner = 0
        self.__inner_abd = 0
        # 系统树根节点
        self.__root = self.__generate_tree()




    def __generate_tree(self):
        """
        生成系统树图
        :return: 返回系统树图的根节点
        """

        eps = 0.0001
        # 初始迭代森林 [(TreeNode,(nodes..),...]
        leave2tree = {n:TreeNode(n) for n in self.__node_set}

        forest = [(TreeNode(n, 1.0), {n}) for n in self.__node_set]

        for n1, n2, simi in self.__node_pairs_data:
            if abs(simi) < 0.0001 or len(forest) is 1:
                break

            # 相似对数据使用统计
            self.__pair_used += 1

            # 计算节点 n1和n2 所属的子树
            tree1 = leave2tree[n1]
            tree2 = leave2tree[n2]
            if tree1 is tree2:
                self.__pair_redu += 1
                continue

            if abs(2*simi - tree1.simi - tree2.simi) < 2*eps \
                    and (tree1.info == 'inner' or tree2.info == 'inner'):
                # 两棵树相似性相同，可以直接将两棵子树的孩子合并

                # 确定子树谁去谁留，作为叶节点的平凡子树需要移除的
                if tree1.info == 'inner':
                    remain_tree, left_tree = tree1, tree2
                else:
                    remain_tree, left_tree = tree2, tree1

                remain_tree.merge_subtree(left_tree)

                for leaf in left_tree.leaves:
                    leave2tree[leaf] = remain_tree

            else:
                # 两棵树相似性不同，需要添加新的节点进行融合

                self.__inner += 1
                new_tree = TreeNode.merge_tree(tree1, tree2, simi)

                for leaf in tree1.leaves:
                    leave2tree[leaf] = new_tree

                for leaf in tree2.leaves:
                    leave2tree[leaf] = new_tree

        rest_trees = tuple(set(leave2tree.values()))

        if len(rest_trees) == 1:
            root = rest_trees[0]
        else:
            self.__inner += 1
            root = TreeNode.merge_trees(rest_trees, 0)

        self.__inner_abd  = len(self.__node_set) - self.__inner - 1
        root.info = 'root'
        return root




    def __serialize(self, tree):
        if len(tree.children) is 0:
            return {'name': '%s' % tree.info, 'children': [], 'hight': tree.simi}
        else:
            children = []
            for child in tree.children:
                children.append(self.__serialize(child))
            return {'name': '%s' % tree.info, 'children': children, 'hight': tree.simi}

    def serialize(self, tree=None):
        return self.__serialize(tree=self.__root)

    def generate_community(self, cut_simi, least_com_num):

        # 系统树划分
        subtrees = Dendrogram.__cut_tree(self.__root, cut_simi)
        # 在该划分结果下的边社团
        covers = []
        for tree in subtrees:
            # 每一个社团
            one_com = tree.leaves
            if len(one_com) >= least_com_num:
                covers.append(tuple(one_com))
        return covers


    @classmethod
    def __cut_tree(cls, tree, cut_simi):
        """
        系统树切割算法，按照切分相似度将相似度小于 cut_simi 的分支水平切割。
        算法的目的虽然是切割系统树，但是不会真正地破坏系统树结构，所以可以反复切割。
        :param tree: 系统树
        :param cut_simi: 切割相似度
        :return: 系统树水平切割后的森林
        """

        # 当前待切割的森林
        curr_forest = [tree]
        # 切割好的森林
        cut_well_trees = []

        is_continue_cut = True
        while is_continue_cut:
            is_continue_cut = False
            next_forest = []
            for subtree in curr_forest:
                # 分别处理根节点相似度 大于或小于 cut_simi 的情况
                if subtree.simi < cut_simi:
                    next_forest.extend(subtree.children)
                    is_continue_cut = True
                else:
                    cut_well_trees.append(subtree)

            curr_forest = next_forest

        return cut_well_trees



    @property
    def info(self):
        d = dict()
        d['depth'] = self.__root.depth
        d['root'] = self.__root
        d['leaf_num'] = len(self.__node_set)
        d['pair_num'] = len(self.__node_pairs_data)
        d['pair_used'] = self.__pair_used
        d['pair_redu'] = self.__pair_redu
        d['inner_num'] = self.__inner
        d['inner_abd_num'] = self.__inner_abd
        d['simi_min'] = self.__node_pairs_data[self.__pair_used-1][2]
        d['simi_max'] = self.__node_pairs_data[0][2]
        return d

