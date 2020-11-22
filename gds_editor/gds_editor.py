import gdspy
import os


class GdsEditor:
    def __init__(self):
        self.lib_dict = {}
        self.dict_layer_name_map_to_num = {}
        self.dict_layer_num_map_to_name = {}

    def load_layer_map(self, map_file):
        if not os.path.exists(map_file):
            print(f'map file:({map_file}) not found.')
            return None
        with open(map_file, 'r') as file:
            for line in file:
                if not line.startswith('#'):
                    l_split = line.split()
                    if len(line) >= 4:
                        layer_name, purpose, layer_num, data_type = l_split
                        layer_num = eval(layer_num)
                        data_type = eval(data_type)
                        self.dict_layer_name_map_to_num[(layer_name, purpose)] = (layer_num, data_type)
                        self.dict_layer_name_map_to_num[(layer_num, data_type)] = (layer_num, data_type)
                        self.dict_layer_num_map_to_name[(layer_name, purpose)] = (layer_name, purpose)
                        self.dict_layer_num_map_to_name[(layer_num, data_type)] = (layer_name, purpose)

    def get_layer_num(self, layer):
        if layer not in self.dict_layer_name_map_to_num:
            return layer
        else:
            return self.dict_layer_name_map_to_num[layer]

    def add_gds_to_lib(self, lib_name: str, gds_file: str):
        if not os.path.exists(gds_file):
            print(f'gds file:({gds_file}) not exists.')
        lib = self.get_lib_by_name(lib_name)
        lib.read_gds(infile=gds_file)
        return lib

    def new_lib(self, lib_name: str):
        if lib_name not in self.lib_dict:
            self.lib_dict[lib_name] = gdspy.GdsLibrary(lib_name)
            print(f'lib({lib_name}) was created successfully.')
            return self.lib_dict[lib_name]
        else:
            print(f'lib named {lib_name} is already exists.')
            return None

    def get_lib_by_name(self, lib_name: str, force_create=False):
        if lib_name not in self.lib_dict:
            if force_create:
                lib = self.new_lib(lib_name)
                return lib
            else:
                return None
        else:
            return self.lib_dict[lib_name]

    def new_cell(self, lib_name: str, cell_name: str, force_create=False):
        lib = self.get_lib_by_name(lib_name, force_create=force_create)
        if lib is not None:
            if cell_name not in lib.cells:
                cell = lib.new_cell(cell_name)
            else:
                cell = lib.cells[cell_name]
                print(f'cell({cell_name}) has already in lib({lib_name})')
            return cell
        else:
            return None

    def get_cell(self, lib_name: str, cell_name: str, force_create=False):
        lib = self.get_lib_by_name(lib_name)
        if cell_name in lib.cells:
            return lib.cells[cell_name]
        else:
            if force_create:
                cell = self.new_cell(lib_name, cell_name)
                return cell
            return None

    def create_gds(self, lib_name: str, outfile :str):
        if lib_name in self.lib_dict:
            lib = self.lib_dict[lib_name]
            lib.write_gds(outfile=outfile)
            return True
        else:
            print(f'lib named {lib_name} not found.')
            return False

    def cell_create_polygon(self, lib_name: str, cell_name: str, pts: list, layer: tuple):
        if len(pts) < 3:
            print('At lease 3 points accepted.')
            return False
        cell = self.get_cell(lib_name, cell_name, force_create=True)
        m_layer = self.get_layer_num(layer)
        polygon = gdspy.Polygon(pts, layer=m_layer[0], datatype=m_layer[1])
        cell.add(polygon)
        return polygon

    def cell_create_label(self, lib_name: str, cell_name: str, label_name: str,
                          pos: list, layer: tuple, rotation: float):
        cell = self.get_cell(lib_name, cell_name, force_create=True)
        m_layer = self.get_layer_num(layer)
        polygon = gdspy.Label(label_name, pos, rotation=rotation, layer=m_layer[0], texttype=m_layer[1])
        cell.add(polygon)
        return polygon

    def cell_create_path(self, lib_name: str, cell_name: str, pts: list, layer: tuple, width: float):
        if len(pts) < 2:
            print('At lease 3 points accepted.')
            return False
        cell = self.get_cell(lib_name, cell_name, force_create=True)
        m_layer = self.get_layer_num(layer)
        path = gdspy.PolyPath(pts, width, layer=m_layer[0], datatype=m_layer[1])
        cell.add(path)
        return path

    def add_gds_cell_to_cell(self, lib_name, cell_name, gds_file,
                             origin, cols=1, rows=1, spacing=None, rotation=0):
        if not os.path.exists(gds_file):
            print(f'gds file:{gds_file} not exists.')
            return False
        else:
            lib = self.get_lib_by_name(lib_name)
            cell = self.get_cell(lib_name, cell_name, force_create=True)
            lib.read_gds(gds_file)
            in_cell = list(lib.cells.values())[-1]
            if spacing is None:
                bbox = in_cell.get_bounding_box()
                width = abs(bbox[1][0]- bbox[0][0])
                height = abs(bbox[1][1]- bbox[0][1])
                spacing = [width, height]
            cell.add(
                gdspy.CellArray(in_cell, columns=cols, rows=rows, spacing=spacing, origin=origin, rotation=rotation)
            )
            return True

    def get_cell_layer(self, lib_name, cell_name, layer):
        dict_shapes = {}
        cell = self.get_cell(lib_name, cell_name)
        layer = self.get_layer_num(layer)
        polygons = cell.get_polygons(by_spec=True)
        dict_shapes['polygons'] = polygons[layer]
        labels = cell.get_labels()
        labels = [x for x in labels if x.layer == layer[0] and x.texttype == layer[1]]
        dict_shapes['labels'] = labels
        return dict_shapes


if __name__ == '__main__':
    # editor = GdsEditor()
    # lib = editor.get_lib_by_name('test', force_create=True)
    # editor.cell_create_polygon('test', 'cell_a', [[0,0], [0,2], [2,2], [2,1], [1,1], [1,0]], (31,0))
    # editor.create_gds('test', 'cell_a.gds')
    # gdspy.LayoutViewer(lib)

    editor = GdsEditor()
    editor.load_layer_map('layer.map')
    lib = editor.get_lib_by_name('test', force_create=True)
    editor.cell_create_polygon('test', 'cell_b', [[0,0], [0,1], [1,1], [1,0]], ('M2', 'drawing'))
    editor.cell_create_path('test', 'cell_b', [[3,0], [3,1], [3,3], [1,3]], ('M2', 'drawing'), 0.5)
    editor.cell_create_label('test', 'cell_b', 'fuck', [5,5], ('M2', 'drawing'), 0.5)
    editor.add_gds_cell_to_cell('test', 'cell_b', 'cell_a.gds', (10,10), 2, 2)
    gdspy.LayoutViewer(lib)
    editor.get_cell_layer('test', 'cell_b', ('M2', 'drawing'))