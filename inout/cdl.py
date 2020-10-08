# system import
import os
import re
from collections import defaultdict as ddt
import sqlite3


class SubcktObject:
    def __init__(self):
        self.inst_name = None
        self.ports = []
        self.nets = []
        self.instances = []

    def set_name(self, inst_name):
        self.inst_name = inst_name

    def add_port(self, port):
        if port not in self.ports:
            self.ports.append(port)

    def add_ports(self, ports):
        self.ports.extend(ports)

    def add_net(self, net):
        if net not in self.nets:
            self.nets.append(net)

    def add_nets(self, nets):
        self.nets.extend(nets)
        self.nets = list(set(self.nets))

    def add_instance(self, instance):
        self.instances.append(instance)

    def add_instances(self, instances):
        self.instances.extend(instances)

class NetObject:
    def __init__(self, parent, net_name):
        self.parent = parent
        self.name = net_name
        self.con = []

    def add_connection(self, inst):
        self.con.append(inst)

    def add_connections(self, l_insts):
        self.con.extend(l_insts)

class InstObject:
    def __init__(self, parent, inst_name):
        self.parent = parent
        self.inst_name = inst_name
        self.conn = []
        self.cdf = []

    def add_connection(self, conn):
        self.conn.append(conn)

    def add_connections(self, conn_list):
        self.conn.extend(conn_list)

    def add_cdf(self, cdf):
        self.cdf.append(cdf)

    def add_cdfs(self, cdfs):
        self.cdf.extend(cdfs)

class CDL:
    def __init__(self):
        self.cdl_file = ''
        self.ckt_db = None
        self.net_db = None
        self.inst_db = None
        self.top_cell = None
        self.search_result = []
        self.ckts = {}
        self.insts = {}
        self.nets = ddt(list)

    def creat_db(self, db_path):
        ckt_db = f'{db_path}/{self.top_cell}.ckt.db'
        inst_db = f'{db_path}/{self.top_cell}.inst.db'
        net_db = f'{db_path}/{self.top_cell}.net.db'
        if not os.path.exists(ckt_db):
            self.ckt_db = sqlite3.connect(ckt_db)
            cmd = '''
                create table SUBCKT (
                inst_name varchar primary key ,
                ports varchar ,
                instances varchar ,
                nets varchar )
                '''
            self.ckt_db.cursor().execute(cmd)
        else:
            self.ckt_db = sqlite3.connect(ckt_db)

        if not os.path.exists(inst_db):
            self.inst_db = sqlite3.connect(inst_db)
            cmd = '''
                create table INSTANCE (
                cell_name varchar primary key ,
                inst_name varchar ,
                parent varchar ,
                conns varchar ,
                cdf varchar)
                '''
            self.inst_db.cursor().execute(cmd)
        else:
            self.inst_db = sqlite3.connect(inst_db)

        if not os.path.exists(net_db):
            self.net_db = sqlite3.connect(net_db)
            cmd = '''
                create table NET (
                name varchar primary key ,
                parent varchar ,
                conns varchar)
                '''
            self.net_db.cursor().execute(cmd)
        else:
            self.net_db = sqlite3.connect(net_db)

    def read_cdl(self, db_path, cdl_file):
        file_name = os.path.basename(cdl_file)
        self.top_cell = os.path.splitext(file_name)[0]
        self.creat_db(db_path)
        if not os.path.exists(cdl_file):
            print(f'File:{cdl_file} is not exist.')
            return None
        else:
            self.cdl_file = cdl_file
        h_file = open(self.cdl_file, 'r')
        line = h_file.readline()
        flg_start = False
        line_correction = ''
        while line != '':
            if line.upper().find('.SUBCKT') != -1:
                line_correction = ''
                flg_start = True
            if line.upper().find('.END') != -1:
                self.analyse_subckt(line_correction)
                flg_start = False
            if flg_start:
                line_correction = f'{line_correction}{line}'
            line = h_file.readline()

        if self.ckt_db is not None:
            self.ckt_db.cursor().close()
            self.ckt_db.commit()
            self.ckt_db.close()
        if self.inst_db is not None:
            self.inst_db.cursor().close()
            self.inst_db.commit()
            self.inst_db.close()
        if self.net_db is not None:
            self.net_db.cursor().close()
            self.net_db.commit()
            self.net_db.close()

    def analyse_subckt(self, lines):
        l_nets = ddt(list)
        l_line = re.split('\n|\n+', lines.strip())
        ckt_name = l_line[0].split(' ')[1]
        self.ckts[ckt_name] = SubcktObject()
        ckt = self.ckts[ckt_name]
        ckt.set_name(ckt_name)
        ckt.add_ports(l_line[0].split(' ')[2:])
        for m_inst_line in l_line[1:]:
            l_split = m_inst_line.strip().split(' ')
            cell_name = l_split[0]
            m_inst = InstObject(ckt_name, cell_name)
            i = len(l_split)
            for m_index, m_item in enumerate(l_split, 0):
                if m_item.find('=') != -1:
                    i = m_index
                    break
            cell_con = l_split[1:i-1]
            inst_name = l_split[i-1]
            cdf = l_split[i:]
            m_inst.add_connection(cell_con)
            ckt.add_instance(cell_name)
            ckt.add_nets(cell_con)
            for m_net in cell_con:
                net_index = f'{ckt_name}/{m_net}'
                if cell_name not in l_nets[net_index]:
                    l_nets[net_index].append(cell_name)
            parent = ckt.inst_name
            conn = cell_con
            self.insts[inst_name] = InstObject(parent, inst_name)
            self.insts[inst_name].add_connection(conn)
            self.insts[inst_name].add_cdf(cdf)
            if self.inst_db is not None:
                self.inst_db.execute('INSERT INTO INSTANCE VALUES (?, ?, ?, ?, ?)',
                                     (f'{parent}/{cell_name}', inst_name, parent, ' '.join(cell_con), ' '.join(cdf)))

        if self.ckt_db is not None:
            inst_name = ckt.inst_name
            ports = ' '.join(ckt.ports)
            instances = ' '.join(ckt.instances)
            nets = ' '.join(ckt.nets)
            # db
            cur = self.ckt_db.cursor()
            cur.execute('insert into SUBCKT VALUES (?, ?, ?, ?)',
                        (inst_name, ports, instances, nets))

        for m_net in l_nets:
            net_name = m_net.split('/')[1]
            parent = m_net.split('/')[0]
            conn = l_nets[m_net]
            # link
            self.nets[m_net] = NetObject(parent, net_name)
            self.nets[m_net].add_connections(conn)
            # db
            if self.net_db is not None:
                cur = self.net_db.cursor()
                cur.execute('INSERT INTO NET VALUES (?, ?, ?)',
                            (net_name, ckt.inst_name, ' '.join(conn)))

    def read_db(self, db_path, top_cell):
        self.top_cell = top_cell
        ckt_db_file = f'{db_path}/{top_cell}.ckt.db'
        inst_db_file = f'{db_path}/{top_cell}.inst.db'
        net_db_file = f'{db_path}/{top_cell}.net.db'
        self.ckt_db = sqlite3.connect(ckt_db_file)
        self.inst_db = sqlite3.connect(inst_db_file)
        self.net_db = sqlite3.connect(net_db_file)
        # ckt
        self.ckts = {}
        cur = self.ckt_db.cursor()
        cur.execute('SELECT * FROM SUBCKT')
        results = cur.fetchall()
        for m_result in results:
            self.set_ckt(m_result)
        # inst
        cur = self.inst_db.cursor()
        cur.execute('SELECT * FROM INSTANCE')
        results = cur.fetchall()
        for m_result in results:
            self.set_inst(m_result)
        # net
        cur = self.net_db.cursor()
        cur.execute('SELECT * FROM NET')
        results = cur.fetchall()
        for m_result in results:
            self.set_net(m_result)

    def set_ckt(self, m_result):
        ckt_name = m_result[0]
        ports = m_result[1]
        insts = m_result[2]
        nets = m_result[3]
        self.ckts[ckt_name] = SubcktObject()
        m_ckt_obj = self.ckts[ckt_name]
        m_ckt_obj.set_name(ckt_name)
        m_ckt_obj.add_ports(ports.split(' '))
        m_ckt_obj.add_instances(insts.split(' '))
        m_ckt_obj.add_nets(nets.split(' '))

    def set_inst(self, m_result):
        cell_name = m_result[0]
        inst_name = m_result[1]
        parent = m_result[2]
        conns = m_result[3]
        cdf = m_result[4]
        self.insts[f'{parent}/{cell_name}'] = InstObject(parent, inst_name)
        m_inst = self.insts[f'{parent}/{cell_name}']
        m_inst.add_connections(conns.split(' '))
        m_inst.add_cdfs(cdf.split(' '))

    def set_net(self, m_result):
        net_name = m_result[0]
        parent = m_result[1]
        conns = m_result[2]
        self.nets[f'{parent}/{net_name}'] = NetObject(parent, net_name)
        self.nets[f'{parent}/{net_name}'].add_connections(conns.split(' '))

    def search_inst(self, inst_name):
        self.search_result = []
        cur = self.inst_db.cursor()
        cur.execute('SELECT * FROM INSTANCE WHERE inst_name=?', (inst_name,))
        results = cur.fetchall()
        for m_result in results:
            l_result = self.analyse_result(m_result)
            for x in l_result:
                self.search_result.append(x)

    def analyse_result(self, search_result):
        cell_name = search_result[0].split('/')[-1]
        inst_name = search_result[1]
        parent = search_result[2]
        if parent == self.top_cell:
            hier_cell_name = f'({parent})/{cell_name}({inst_name})'
            return [hier_cell_name]
        else:
            hier_cell_name = f'{cell_name}({inst_name})'
            cur = self.inst_db.cursor()
            cur.execute('SELECT * FROM INSTANCE WHERE inst_name=?', (parent,))
            results = cur.fetchall()
            l_new_result = []
            for m_result in results:
                l_results = self.analyse_result(m_result)
                l_new_result.extend([f'{x}/{hier_cell_name}' for x in l_results])
            return l_new_result



    def get_search_result(self):
        for x in self.search_result:
            print(x)
        return self.search_result


if __name__ == '__main__':
    a = CDL()
    # a.read_cdl('.', 'test.cdl')
    a.read_db('.', 'test')
    a.search_inst('nch_18_mac')
    a.get_search_result()