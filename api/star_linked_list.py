#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

from collections import defaultdict as ddt
import numpy as np

class StarNode:
    def __init__(self, num, child_num):
        self.num = num
        self.childNodes = [child_num]


class StarLinkedList:
    def __init__(self):
        self.nodeDict = {}
        self.valueDict = {}
        self.instNodeDict = ddt(list)
        self.zero = 1e-18

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
        l_path = self.trace_sub(node_num1, node_num2, [node_num1])
        print(l_path)
        return l_path

    def trace_sub(self, node_num1, node_num2, path):
        l_all_path = []
        for m_node in list(set(self.nodeDict[node_num1].childNodes).difference(set(path))):
            if m_node == node_num2:
                sub_path = list(path)
                sub_path.append(node_num2)
                l_all_path.extend(sub_path)
            else:
                sub_path = list(path)
                sub_path.append(m_node)
                tmppath = self.trace_sub(m_node, node_num2, sub_path)
                l_all_path.extend(tmppath)
        l_all_path = list(set(l_all_path))
        return l_all_path

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

    def p2p(self, node_num1, node_num2):
        i = 10
        # r_list = [[0 for x in range(i)] for x in range(i)]
        # print(r_list)
        l_mem_nums = self.trace(node_num1, node_num2)
        max_size = len(l_mem_nums)
        l_mem_nums.pop(l_mem_nums.index(node_num1))
        l_mem_nums.pop(l_mem_nums.index(node_num2))
        tmp = [node_num1]
        tmp.extend(l_mem_nums)
        tmp.append(node_num2)
        l_mem_nums = list(tmp)
        r_list = np.zeros(shape=[max_size, max_size+1])
        print(r_list)
        print(l_mem_nums)
        for m_node_num in l_mem_nums:
            for m_childe_node_num in self.nodeDict[m_node_num].childNodes:
                index_str = '@'.join(sorted([m_node_num, m_childe_node_num]))
                index1 = l_mem_nums.index(m_node_num)
                index2 = l_mem_nums.index(m_childe_node_num)
                value = self.valueDict[index_str]
                r_list[index1][index2] = -1/value
                r_list[index1][index1] += 1/value
        r_list[0][max_size] = 1
        r_list[max_size-1][max_size] = 1
        index_node1 = l_mem_nums.index(node_num1)
        r_list[index_node1][index_node1] = 0
        self.guassi(r_list)
        return r_list

    def guassi(self, r_list):
        print(r_list)
        n = len(r_list)
        print(f'n:{n}')
        # 保证对角线上的值不为0
        for i in range(0, n):
            if abs(r_list[i][i]) < self.zero:
                for j in range(i+1, n):
                    if abs(r_list[j][i]) > self.zero:
                        r_list[[i,j],:] = r_list[[j,i],:]
                        break

        print(r_list)

        for i in range(0, n):
            for j in range(0, i):
                if abs(r_list[i][j]) > self.zero:
                    incr = r_list[i][j]/r_list[j][j]
                    for k in range(0, n+1):
                        r_list[i][k] = r_list[i][k] - incr * r_list[j][k]
        print(r_list)





    def flat_list(self, ori_list: list):
        for m_list in ori_list:
            if isinstance(m_list, list):
                yield from self.flat_list(m_list)
            else:
                yield m_list

    def __del__(self):
        pass
        # self.show_info()
