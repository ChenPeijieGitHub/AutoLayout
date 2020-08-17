#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

from collections import namedtuple

class StarNode:
    def __init__(self, num, child_num):
        self.num = num
        self.childNodes = [child_num]


class StarLinkedList:
    def __init__(self):
        self.nodeList = {}
        self.value_list = {}

    def addNode(self, num1, num2, value):
        if num1 not in self.nodeList:
            node1 = StarNode(num1, num2)
            self.nodeList[num1] = node1
            value_index = '@'.join(sorted([num1, num2]))
            if value_index not in self.value_list:
                self.value_list[value_index] = eval(value)
            else:
                self.value_list[value_index] = \
                    self.cal_parallel_res(self.value_list[value_index], eval(value))
        else:
            if num2 not in self.nodeList[num1].childNodes:
                self.nodeList[num1].childNodes.append(num2)

        if num2 not in self.nodeList:
            node2 = StarNode(num2, num1)
            self.nodeList[num2] = node2
        else:
            if num1 not in self.nodeList[num2].childNodes:
                self.nodeList[num2].childNodes.append(num1)

    def delNode(self, node: StarNode):
        self.nodeList.pop(node.num)
        for m_node in self.nodeList:
            for x in self.nodeList[m_node].childNodes:
                if node.num in x:
                    x.pop(node.num)

    def trace(self, node_num1, node_num2):
        if node_num1 not in self.nodeList:
            return None
        if node_num2 not in self.nodeList:
            return None
        self.trace_sub(node_num1, node_num2, [node_num1])

    def trace_sub(self, node_num1, node_num2, path):
        for m_node in list(set(self.nodeList[node_num1].childNodes).difference(set(path))):
            if m_node == node_num2:
                sub_path = list(path)
                sub_path.append(node_num2)
                print('Res Path: %s' % sub_path)
            else:
                sub_path = list(path)
                sub_path.append(m_node)
                self.trace_sub(m_node, node_num2, sub_path)

    def cal_parallel_res(self, res1, res2):
        return res1 * res2 / (res1 + res2)