#!/bin/env python3
import os
import sys
from collections import defaultdict as ddt
import subprocess


class CalibreHandler:
    gds_in_file = str
    top_cell_name = str
    precision = int
    resolution = int

    layer_map_file = str
    gds_out_file = str
    rule_file = str
    check_item = {}
    layer_operation = ddt(list)
    inner_layers_dict = dict()
    layer_definition_dict = dict()
    run_dir = str
    cmd = str
    gds_out_cmd = []
    rule_check_dict = ddt(str)

    def __init__(self):
        pass

    def set_run_dir(self, run_dir):
        self.run_dir = run_dir

    def set_rule_file_name(self, rule_file_name):
        self.rule_file = os.path.join(self.run_dir, rule_file_name)
        self.check_file_access(self.rule_file)

    def load_layer_map(self, layer_map_file):
        self.check_file_exists(layer_map_file)
        self.layer_map_file = layer_map_file

    def read_gds(self, gds_in_file, top_cell_name):
        self.check_file_exists(gds_in_file)
        self.gds_in_file = os.path.abspath(gds_in_file)
        self.top_cell_name = top_cell_name

    def set_precision(self, precision: int, resolution: int):
        self.precision = precision
        self.resolution = resolution

    def create_rule_file(self):
        with open(self.rule_file, 'w') as file:
            # layout settings
            file.write('//LAYOUT SETTINGS\n')
            file.write(f'PRECISION {self.precision}\n')
            file.write(f'RESOLUTION {self.resolution}\n')

            file.write('LAYOUT SYSTEM GDSII\n')
            file.write(f'LAYOUT PATH "{self.gds_in_file}"\n')
            file.write(f'LAYOUT PRIMARY "{self.top_cell_name}"\n')
            file.write('//END LAYOUT SETTINGS\n\n')

            # report
            file.write('//REPORT SETTINGS\n')
            file.write(f'DRC RESULTS DATABASE "{self.run_dir}/DRC_RES.db"\n')
            file.write(f'DRC SUMMARY REPORT "{self.run_dir}/DRC.rep"\n')
            file.write(f'DRC MAXIMUM RESULTS ALL\n')
            file.write('//END REPORT SETTINGS\n\n')

            # add layer definition
            file.write('//LAYER DEFINITION\n')
            for m_layer_definition in self.layer_definition_dict:
                file.write(f'{self.layer_definition_dict[m_layer_definition]}\n')
            file.write('//END LAYER DEFINITION\n\n')

            # add custom layer operation
            file.write('//CUSTOM LAYER OPERATION\n')
            for m_layer_name in self.inner_layers_dict:
                file.write(f'{m_layer_name} = {self.inner_layers_dict[m_layer_name]}\n')
            file.write('//END CUSTOM LAYER OPERATION\n\n')

            # rule check
            for m_check_name in self.rule_check_dict:
                file.write('%s {%s}\n' % (m_check_name, self.rule_check_dict[m_check_name]))

            file.write(f'{self.gds_out_cmd}\n')
        return self.rule_file

    def add_layer_definition(self, layer_name, layer_num, data_type, map_number):
        self.layer_definition_dict[layer_name] = f'LAYER {layer_name} {map_number}\n'
        self.layer_definition_dict[layer_name] += f'LAYER MAP {layer_num} DATATYPE {data_type} {map_number}\n'

    def layer_and(self, layer1_name, layer2_name, new_layer_name=None):
        if new_layer_name is None:
            new_layer_name = f'{layer1_name}_and_{layer2_name}'
            count = 0
            while new_layer_name in self.inner_layers_dict:
                new_layer_name = f'{layer1_name}_and_{layer2_name}_{count}'

        self.inner_layers_dict[new_layer_name] = f'{layer1_name} AND {layer2_name}'
        return new_layer_name

    def layer_or(self, layer1_name, layer2_name, new_layer_name=None):
        if new_layer_name is None:
            new_layer_name = f'{layer1_name}_or_{layer2_name}'
            count = 0
            while new_layer_name in self.inner_layers_dict:
                new_layer_name = f'{layer1_name}_or_{layer2_name}_{count}'

        self.inner_layers_dict[new_layer_name] = f'{layer1_name} OR {layer2_name}'
        return new_layer_name

    def rule_check(self, check_name, cmd):
        self.rule_check_dict[check_name] = cmd

    def create_gds_by_rule_check(self, rule_name, out_file_name):
        out_file = os.path.join(self.run_dir, out_file_name)
        self.gds_out_cmd = f'DRC CHECK MAP {rule_name} GDSII "{out_file}"'

    def creat_cmd(self):
        self.cmd = ['calibre', '-drc', '-64', f'{self.rule_file}']

    def run(self):
        subprocess.run(self.cmd, cwd=self.run_dir, stdout=sys.stdout, stderr=sys.stdout)

    @staticmethod
    def check_file_exists(file_name):
        if not os.path.exists(file_name):
            raise FileExistsError(f'Can not find the file:{file_name}')

    @staticmethod
    def check_file_access(file_name):
        ret = os.access(os.path.split(file_name)[0], mode=os.W_OK)
        if not ret:
            raise PermissionError(f'Failed to create file:{file_name}')


if __name__ == '__main__':
    h = CalibreHandler()
    h.set_run_dir('/home/chen/verify/rules')
    h.read_gds('/home/chen/cds/test_cell.gds', 'test_cell')
    h.set_precision(1000, 5)
    h.add_layer_definition('M1', 31, 0, 501)
    h.add_layer_definition('M2', 32, 0, 502)
    h.add_layer_definition('M3', 33, 0, 503)
    h.layer_and('M1', 'M2')
    h.load_layer_map("/home/chen/cds/techfile")
    h.rule_check('overlap_m1_m2', 'COPY M1_and_M2')
    h.set_rule_file_name("rule.file")
    h.create_gds_by_rule_check('overlap_m1_m2', '/home/chen/verify/a.gds')
    h.create_rule_file()
    h.creat_cmd()
    # h.run()