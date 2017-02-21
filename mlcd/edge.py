class Edge:
    """
    定义无向边数据结构，具有自反性
    """
    def __init__(self, n1, n2):
        if type(n1) == type(n2):
            if n1 < n2:
                self.__n1 = n1
                self.__n2 = n2
            else:
                self.__n1 = n2
                self.__n2 = n1
        else:
            if hash(n1) < hash(n2):
                self.__n1 = n1
                self.__n2 = n2
            else:
                self.__n1 = n2
                self.__n2 = n1

        self.__name = '%s-%s' % (self.__n1, self.__n2)

    def __eq__(self, edge):
        if not isinstance(edge, Edge):
            return False
        elif self.__n1 == edge.__n1 and self.__n2 == edge.__n2:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__name)

    def __repr__(self):
        return self.__name

    def __str__(self):
        return self.__name

    def name(self):
        return self.__name

    def node(self):
        return self.__n1, self.__n2

    def rnode(self):
        return self.__n2, self.__n1
