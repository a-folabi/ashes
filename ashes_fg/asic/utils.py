import numpy as np
from collections import defaultdict
import bisect

def update_output_layout(text, file_path):
    '''
    append to the final layout file 
    '''
    with open(file_path, 'a') as outfile:
        outfile.writelines(text)


def calculate_offset(col_widths, curr_col, cell_padding):
    '''
    Calculate the width offset for a given column
    '''
    offset = 0
    col_keys = list(col_widths.keys())
    col_keys.sort()
    for key in col_keys:
        if key == curr_col: break
        val = col_widths[key]
        if val[1] == 'matrix':
            offset += val[0]
        elif val[1] == 'cell':
            offset += val[0] + cell_padding
    return offset

def make_pin_list(layer_map, tech_process):
    ''' 
    Return a list of all pin layers in layer map file as a (layer, datatype) tuple
    eg [('131', '0'), ('132', '0'), ('133', '0')]
    '''
    pin_list = []
    for item, value in layer_map.items():
        if value['purpose'] == 'pin':
            layer, datatype = item.split(',')
            pin_list.append((layer, datatype))
    
    if not pin_list: 
        raise PinNotDefined(f'Cannot find any pin mapping in {tech_process}.json')
    
    return pin_list

def assign_pins_to_polygon(pin_names, pin_boxes, layer_map, pin_dt):
    '''
    Given a list of pin centers and pin boxes, match the pin centers to the right boxes
    '''
    assigned_pins = {}
    for pin in pin_names:
        pin_x, pin_y = pin[2], pin[3]
        for box in pin_boxes:
            if box[1] < pin_x < box[3] and box[2] < pin_y < box[4] and box[0] == pin[0]:
                assigned_pins.update({pin[1]: { "Layer": layer_map[f'{pin[0]},{pin_dt}']['pdk_name'], "RECT": (box[1], box[2], box[3], box[4])} })
                break
    return assigned_pins

def reverse_pdk_doc(layer_map):
    '''
    Use pdkname_purpose as key instead
    '''
    ret_doc = {}
    for ld_str, value in layer_map.items():
        key = value['pdk_name'] + '_' + value['purpose']
        ret_doc[key] = value
        ret_doc[key]['layer_type'] = ld_str
    return ret_doc

def count_metal_layers(layer_map, tech_process):
    '''
    Return a list of metal routing layers available in PDK
    '''
    metal_layers = []
    for item, value in layer_map.items():
        if value['layer'][:5] == 'metal':
            metal_layers.append(value['pdk_name'])
    
    if not metal_layers: 
        raise PinNotDefined(f'Cannot find any metal layers in {tech_process}.json')
    
    return metal_layers

def sanitize_island_info(island_info):
    '''
    Return a dictionary of island info with instnce name as key. 
    - collapse deques and merge all islands into one structure
    '''
    ret_doc = {}
    for island in island_info:
        mod_list = island_info[island]['deq']
        for inst in mod_list:
            ret_doc[inst.instance_name] = inst.ports
            ret_doc[inst.instance_name]['module_name'] = inst.module_name
    return ret_doc

def find_via_in_lef(via_name, file_name, dbu):
    '''
    Given a via name and file name, return the via definition from the lef file
    '''
    lef_file = open(f'{file_name}.lef')
    store_via, rect_toggle, leave_file = False, False, False
    temp_via = None
    ret_val = []
    for line in lef_file:
        line = line.split(' ')
        if len(line) > 1 and line[1] == f'{via_name}\n' and line[0] == 'VIA': 
            store_via = True
        elif store_via:
            if line[0] == 'END': 
                store_via = False
                lef_file.close()
                return ret_val
            elif ~rect_toggle: temp_via = line[3]
            elif rect_toggle: ret_val.append((temp_via, float(line[5])*dbu, float(line[6])*dbu, float(line[7])*dbu, float(line[8])*dbu))
            rect_toggle = ~rect_toggle

def get_island_adjacent(island_place, neighbors):
    '''
    Return a dictionary of right adjacent islands for all placed islands.
    i.e. What island is to the right of the current island? This helps determine vertical channels
    '''
    matrix = np.array(island_place)
    bottoms = matrix[:, 1] # get bottom y locations of all placed islands
    for idx, item in enumerate(island_place):
        if idx in neighbors: # skip islands whose adjacent were already assigned
            continue
        else:
            same_row = [i for i,n in enumerate(bottoms) if n == item[1]] # get islands on the same row
            if len(same_row) <= 1: # if only one on the row, then no adjacent islands
                neighbors[idx] = None
            else:
                same_row = list(set(same_row) - set(neighbors.keys())) # for islands on the same row, remove already processed items
                if len(same_row) > 1:
                    neighbors[idx] = same_row[1]
                else:
                    neighbors[idx] = None

def add_guide_to_def(file_path, blocks, nets, guide):
    '''
    Append the global router guide polygons to the def file for viewing in klayout
    '''
    with open(file_path, 'a') as def_file:
        def_file.write(blocks)
        def_file.write(f';\n  - LAYER M1\n')
        for idx, box in enumerate(guide):
            if idx < ( len(guide) - 1):  
                def_file.write(f'    RECT ( {box[0]} {box[1]} ) ( {box[2]} {box[3]} ) \n')
            else:
                def_file.write(f'    RECT ( {box[0]} {box[1]} ) ( {box[2]} {box[3]} ) ;\n')
        def_file.write(f'END BLOCKAGES\n\n')
        def_file.write(nets)

def find_metal_in_lef(metal, file_name, dbu):
    lef_file = open(f'{file_name}.lef')
    store_metal = False
    ret_val = None
    for line in lef_file:
        line = line.split(' ')
        if len(line) > 1 and line[1] == f'{metal}\n' and line[0] == 'LAYER': 
            store_metal = True
        elif store_metal:
            if line[2] == 'WIDTH': 
                ret_val = float(line[3])*dbu
                store_metal = False
                lef_file.close()
                return ret_val
    lef_file.close()
    return ret_val


class Rectangle:
    def __init__(self, x1, y1, x2, y2, layer):
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)
        self.layer = layer

class EdgeEvent:
    def __init__(self, coord, start, end, is_start, rect, is_vertical):
        self.coord = coord
        self.start = start
        self.end = end
        self.is_start = is_start
        self.rect = rect
        self.is_vertical = is_vertical

class HoleDetector:
    def __init__(self, metal_width):
        self.metal_width = metal_width
        self.rectangles = []
        self.layers = defaultdict(list)

    def add_rectangle(self, x1, y1, x2, y2, layer):
        rect = Rectangle(x1, y1, x2, y2, layer)
        self.rectangles.append(rect)
        self.layers[layer].append(rect)

    def find_holes(self):
        holes = []
        for layer, rects in self.layers.items():
            vertical_holes = self._find_direction_holes(rects, is_vertical=True)
            horizontal_holes = self._find_direction_holes(rects, is_vertical=False)
            holes.extend([(hole, layer, "vertical") for hole in vertical_holes])
            holes.extend([(hole, layer, "horizontal") for hole in horizontal_holes])
        return holes

    def _find_direction_holes(self, rects, is_vertical):
        events = []
        for rect in rects:
            if is_vertical:
                events.append(EdgeEvent(rect.x1, rect.y1, rect.y2, True, rect, is_vertical))
                events.append(EdgeEvent(rect.x2, rect.y1, rect.y2, False, rect, is_vertical))
            else:
                events.append(EdgeEvent(rect.y1, rect.x1, rect.x2, True, rect, is_vertical))
                events.append(EdgeEvent(rect.y2, rect.x1, rect.x2, False, rect, is_vertical))
        events.sort(key=lambda e: e.coord)

        active_edges = []
        holes = []

        for i, event in enumerate(events):
            if event.is_start:
                self._insert_edge(active_edges, event)
            else:
                self._remove_edge(active_edges, event)

            if i < len(events) - 1 and events[i+1].coord - event.coord <= self.metal_width:
                new_holes = self._check_for_holes(active_edges, event.coord, events[i+1].coord, is_vertical)
                holes.extend(new_holes)

        return holes

    def _insert_edge(self, active_edges, event):
        bisect.insort(active_edges, (event.start, event.end, event.rect), key=lambda e: e[0])

    def _remove_edge(self, active_edges, event):
        active_edges.remove((event.start, event.end, event.rect))

    def _check_for_holes(self, active_edges, coord1, coord2, is_vertical):
        holes = []
        for i in range(len(active_edges) - 1):
            _, end1, _ = active_edges[i]
            start2, _, _ = active_edges[i+1]
            gap = start2 - end1
            if 0 < gap < self.metal_width:
                if is_vertical:
                    hole = ((coord1, end1), (coord2, start2))
                else:
                    hole = ((end1, coord1), (start2, coord2))
                
                # Ensure the hole has non-zero width and height
                if hole[0][0] != hole[1][0] and hole[0][1] != hole[1][1]:
                    holes.append(hole)
        return holes