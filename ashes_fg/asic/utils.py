import numpy as np

def update_output_layout(text, file_path):
    '''
    append to the final layout file 
    '''
    with open(file_path, 'a') as outfile:
        outfile.writelines(text)


def calculate_offset(col_widths, curr_col):
    '''
    Calculate the width offset for a given column
    '''
    return sum(list(col_widths.values())[:curr_col])

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
    return neighbors

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