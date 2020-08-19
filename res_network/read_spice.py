#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8

import os
import argparse

# parser = argparse.ArgumentParser(description='Read spice into a linklist')
# parser.add_argument('-spi', metavar='DIR', default='a.spi', help='appoint a spice file')
#
# args = parser.parse_args()
#
# for key in args.__dict__:
#     print(f'{key}={args.__dict__[key]}')
# spiFile = args.__dict__['spi']

import re
from collections import defaultdict as ddt
from api.star_linked_list import StarLinkedList

class ReadSpice:
    def __init__(self, spiFile):
        self.linked_dict = {}
        self.h_spiFile = None
        try:
            self.h_spiFile = open(spiFile, 'r')
        except IOError:
            print(f'File "{spiFile}" does not exist!')
            exit('001')

    def read_res(self):
        line = self.h_spiFile.readline()
        inst_net_dict = ddt(list)
        while line != '':
            #print(line)
            if line[0] == 'X':
                l_split = line.split()
                inst_name = l_split[0].split('@')[0]
                l_split.pop(0)
                l_split.pop(-1)
                for m_net_name in l_split:
                    index = f'{inst_name}@{m_net_name.split("#")[0]}'
                    node_num = m_net_name.split('#')[-1]
                    if node_num not in inst_net_dict[index]:
                        inst_net_dict[index].append(node_num)
            elif line[0] == 'R':
                l_split = line.split()
                net_name = l_split[1].split('#')[0]
                if net_name not in self.linked_dict:
                    self.linked_dict[net_name] = StarLinkedList()
                node_num1 = l_split[1].split('#')[-1]
                node_num2 = l_split[2].split('#')[-1]
                value = l_split[3]
                self.linked_dict[net_name].addNode(node_num1, node_num2, value)
            line = self.h_spiFile.readline()
        print(inst_net_dict)
        for m_net_name in inst_net_dict:
            net_name = m_net_name.split('@')[1]
            for i in range(0, len(inst_net_dict[m_net_name])-1):
                node_num1 = inst_net_dict[m_net_name][i]
                node_num2 = inst_net_dict[m_net_name][i+1]
                value = '0'
                self.linked_dict[net_name].addNode(node_num1, node_num2, value)

    def show(self):
        for m_netName in self.linked_dict:
            print(m_netName)
            for m_node_num in self.linked_dict[m_netName].nodeList:
                print(m_node_num)
                print(self.linked_dict[m_netName].nodeList[m_node_num].childNodes)
        #self.linked_dict[m_netName].trace('123', '127')
        self.linked_dict[m_netName].merge_series_res_node()

    def __del__(self):
        self.h_spiFile.close()

if __name__ == '__main__':
    HReadSpaice = ReadSpice('/Users/chenpeijie/Desktop/GitHub/AutoLayout/res_network/a.spi')
    HReadSpaice.read_res()
    HReadSpaice.show()