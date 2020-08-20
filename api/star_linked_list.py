#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

from collections import defaultdict as ddt

class StarNode:
    def __init__(self, num, child_num):
        self.num = num
        self.childNodes = [child_num]


class StarLinkedList:
    def __init__(self):
        self.nodeDict = {}
        self.valueDict = {}
        self.instNodeDict = ddt(list)

    def addNode(self, num1, num2, value):
        if num1 not in self.nodeDict:
            node1 = StarNode(num1, num2)
            self.nodeDict[num1] = node1
        else:
            if num2 not in self.nodeDict[num1].childNodes:
                self.nodeDict[num1].childNodes.append(num2)

        if num2 not in self.nodeDict:
            node2 = StarNode(num2, num1)
            self.nodeDict[num2] = node2
        else:
            if num1 not in self.nodeDict[num2].childNodes:
                self.nodeDict[num2].childNodes.append(num1)

        value_index = '@'.join(sorted([num1, num2]))
        if value_index not in self.valueDict:
            self.valueDict[value_index] = value
        else:
            self.valueDict[value_index] = \
                self.cal_parallel_res(self.valueDict[value_index], value)

    def delNode(self, node_num):
        for m_node_num in self.nodeDict[node_num].childNodes:
            value_index = '@'.join(sorted([node_num, m_node_num]))
            if value_index in self.valueDict:
                self.valueDict.pop(value_index)
        self.nodeDict.pop(node_num)
        for m_node_num in self.nodeDict:
            if node_num in self.nodeDict[m_node_num].childNodes:
                self.nodeDict[m_node_num].childNodes.remove(node_num)

    def shortAndDeleteNode(self, node_num):
        childNodes = self.nodeDict[node_num].childNodes
        self.delNode(node_num)
        for m_node_num in childNodes:
            tmpNodesList = list(childNodes)
            tmpNodesList.remove(m_node_num)
            self.nodeDict[m_node_num].childNodes.extend(tmpNodesList)
            self.nodeDict[m_node_num].childNodes = list(set(self.nodeDict[m_node_num].childNodes))

    def show_info(self):
        print('************* link node infomation start ***************')
        for m_node_num in self.nodeDict:
            print(f'{m_node_num}:{self.nodeDict[m_node_num].childNodes}')
        print(f'node res info:{self.valueDict}')
        print('*************  link node infomation end  ***************\n')

    def trace(self, node_num1, node_num2):
        if node_num1 not in self.nodeDict:
            return None
        if node_num2 not in self.nodeDict:
            return None
        self.trace_sub(node_num1, node_num2, [node_num1])

    def trace_sub(self, node_num1, node_num2, path):
        for m_node in list(set(self.nodeDict[node_num1].childNodes).difference(set(path))):
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

    # 简单的电阻串联网络，默认每个节点的子节点只有两个，不存在分支
    # 电阻阻值相加，一边累加阻值，一边删除被 merge 的节点，最后只剩下首尾两个节点
    # node1 <--> res1 <--> node2 <--> res2 <--> node3
    # ==>
    # node1 <--> (res1 + res2) <--> node3
    def merge_res_node(self):
        merge_flg = False
        not_to_merge_nodes_list = list(self.instNodeDict.values())
        # 打散
        not_to_merge_nodes_list = list(self.flat_list(not_to_merge_nodes_list))
        # 去重
        not_to_merge_nodes_list = list(set(not_to_merge_nodes_list))

        for m_node_num in list(self.nodeDict.keys()):
            if m_node_num not in not_to_merge_nodes_list:
                childNodes = self.nodeDict[m_node_num].childNodes
                if len(childNodes) == 2:
                    merge_flg = True
                    node_num1 = childNodes[0]
                    node_num2 = childNodes[1]
                    value_index1 = '@'.join(sorted([m_node_num, node_num1]))
                    value_index2 = '@'.join(sorted([m_node_num, node_num2]))
                    r = self.valueDict[value_index1] + self.valueDict[value_index2]
                    self.delNode(m_node_num)
                    self.addNode(node_num1, node_num2, r)
                elif len(childNodes) == 3:
                    merge_flg = True
                    node_num1 = childNodes[0]
                    node_num2 = childNodes[1]
                    node_num3 = childNodes[2]
                    value_index1 = '@'.join(sorted([m_node_num, node_num1]))
                    value_index2 = '@'.join(sorted([m_node_num, node_num2]))
                    value_index3 = '@'.join(sorted([m_node_num, node_num3]))
                    r1 = self.valueDict[value_index1]
                    r2 = self.valueDict[value_index2]
                    r3 = self.valueDict[value_index3]
                    r12 = r1 + r2 + r1*r2/r3
                    r13 = r1 + r3 + r1*r3/r2
                    r23 = r2 + r3 + r2*r3/r1
                    self.delNode(m_node_num)
                    self.addNode(node_num1, node_num2, r12)
                    self.addNode(node_num1, node_num3, r13)
                    self.addNode(node_num2, node_num3, r23)
        if merge_flg:
            self.merge_res_node()
        return(merge_flg)

    def flat_list(self, ori_list: list):
        for m_list in ori_list:
            if isinstance(m_list, list):
                yield from self.flat_list(m_list)
            else:
                yield m_list

    def __del__(self):
        self.show_info()