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
from api.star_linked_list import StarLinkedList

class ReadSpice:
    def __init__(self, spiFile):
        self.h_spiFile = None
        try:
            self.h_spiFile = open(spiFile, 'r')
        except IOError:
            print(f'File "{spiFile}" does not exist!')
            exit('001')

    def read_res(self):
        link = StarLinkedList()
        line = self.h_spiFile.readline()
        while line != '':
            #print(line)
            l_res = re.split(r'\t| ', line)
            node_num1 = l_res[1].split('#')[1]
            node_num2 = l_res[2].split('#')[1]
            value = l_res[3]
            link.addNode(node_num1, node_num2, value)
            line = self.h_spiFile.readline()
        # for x in link.nodeList:
        #     print(x)
        #     print(link.nodeList[x].childNodes)
        link.trace('123', '127')

    def __del__(self):
        self.h_spiFile.close()

if __name__ == '__main__':
    HReadSpaice = ReadSpice('/Users/chenpeijie/Desktop/GitHub/AutoLayout/res_network/a.spi')
    HReadSpaice.read_res()