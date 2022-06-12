# coding=UTF-8
from fractions import Fraction
import re
from graphviz import Digraph


class MdpNode:
    def __init__(self, label, kind):
        self.actions = {}
        self.label = label
        self.kind = kind  # 属于哪种节点


class GraphHelp:
    def __init__(self):
        self.nodes = {}

    def _addEdge(self, x, y):
        if x not in self.nodes.keys():
            self.nodes[x] = set()
        self.nodes[x].add(y)


class Graph:
    def __init__(self):
        self.MdpNodes = set()
        self.reverse_undergraph = GraphHelp()
        self.value = dict()  # 状态自身的价值

    def ReadMdpFromFile(self, filename):
        degreeNotZero = set()
        with open(filename) as file:
            for line in file:
                line = line.split()
                line[3] = float(Fraction(line[3]))
                # 最关键是调用了addEdge函数，那么addEdge函数中到底发生了什么？（注意这里是循环调用）
                self.addEdge(line[0], line[1], line[2], line[3], line[4], degreeNotZero)

    def ReadMdpValueFromFile(self, filename):
        with open(filename) as file:
            for line in file:
                line = line.split()
                self.value[line[0]] = line[1]

    def addEdge(self, labelX, Act, labelY, Pr, Reward, degreeNotZero):
        NodeX = None
        NodeY = None
        # self.MdpNodes中一开始没有节点，节点是随着ReadMdpFromFile函数中那个for循环慢慢出现的
        for node in self.MdpNodes:
            if node.label == labelX:
                NodeX = node
            if node.label == labelY:
                NodeY = node
        if NodeX is None:
            # MdpNode是一个类，描述节点的类，在这里，NodeX是该类创建的实例
            NodeX = MdpNode(labelX, self._KindOfNode(labelX))
            self.MdpNodes.add(NodeX)  # 就是这里，为MdpNodes中添加节点
        if NodeY is None:
            NodeY = MdpNode(labelY, self._KindOfNode(labelY))
            self.MdpNodes.add(NodeY)
        if Act not in NodeX.actions.keys():
            NodeX.actions[Act] = []
        NodeX.actions[Act].append((NodeY, Pr, Reward))
        self.reverse_undergraph._addEdge(NodeY, NodeX)
        degreeNotZero.add(NodeX)

    def _KindOfNode(self, label):
        num = int(re.findall(r'\d+', label)[0])
        if num % 2 == 0:
            return 'env'
        return 'sys'

    # 画图
    def dot(self, B):
        g = Digraph(comment='MDP')
        # print("self.value.items():", self.value.items())
        for node in self.MdpNodes:
            # print("node.label:", node.label)
            # print("self.value.get(node.label):", self.value.get(node.label))
            if node.kind == 'sys':
                g.node(name=node.label, label=node.label, shape="box")
            if node in B:
                g.node(name=node.label, label=node.label, color="green")
            value = self.value.get(node.label)
            if (value != None):
                g.node(name=node.label, label=node.label + "/" + value)

        for node in self.MdpNodes:
            for k in node.actions.keys():
                for out in node.actions[k]:
                    g.edge(node.label, out[0].label, k + '/' + str(out[1]) + '/' + out[2])

        g.view()


if __name__ == "__main__":
    gra = Graph()
    gra.ReadMdpValueFromFile("mdp2_value")
    gra.ReadMdpFromFile("mdp2")
    gra.dot(set())
