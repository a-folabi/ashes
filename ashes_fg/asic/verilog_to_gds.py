import os
import pprint
from collections import deque
import json
import shutil
import math
import re
import time
import sys
import tracemalloc
from pathlib import Path

# make sure our local fork of gdsii is added to system path
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

from verilog_parser.parser import parse_verilog 
from gdsii import types, tags 
from gdsii.record import Record 
import numpy as np

from ashes_fg.asic.exceptions import *
from ashes_fg.asic.global_router import global_router
from ashes_fg.asic.utils import *

# TODO: 
# - write output directly as binary
# - Place decoders either on top or to the side depending on die size

# Qs:
# - Why are island numbers zero indexed but row and cols are 1 indexed?

verbose = False
pypath = sys.executable


def gds_synthesis(process_params, design_area, proj_name, routed_def=False, router_tool='qrouter'):
    verilog_file_name = proj_name + '.v'
    file_name_no_ext = proj_name
    file_path = os.path.join('.', file_name_no_ext)
    ver_file = open(os.path.join('.', proj_name, 'verilog_files', verilog_file_name), 'r')
    ver_file_content = ver_file.read()
    ver_file.close()
    tech_process, dbu, track_spacing, x_offset, y_offset, cell_pitch = process_params
    
    ast = parse_verilog(ver_file_content)
    module_list = set()
    cell_info = {}
    first_cell = True
    top_module, frame_module = None, None
    nets_table = {}

    text_layout_path = os.path.join(file_path, f'{file_name_no_ext}_gds.txt')
    gds_path = os.path.join(file_path, f'{file_name_no_ext}_placed.gds')
    lef_file_path = os.path.join(file_path, f'{file_name_no_ext}.lef')
    def_file_path = os.path.join(file_path, f'{file_name_no_ext}.def')
    guide_file_path = os.path.join(file_path, f'{file_name_no_ext}.guide')
    merged_gds_file_path = os.path.join(file_path, f'{file_name_no_ext}_merged.gds')
    text_merged_layout_path = os.path.join(file_path, f'{file_name_no_ext}_merged.txt')

    # Delete previously generated files if not merging routes
    if not routed_def:
        generated_files = [text_layout_path, gds_path, lef_file_path, def_file_path, guide_file_path, merged_gds_file_path, text_merged_layout_path]
        for item in generated_files:
            if os.path.isfile(item):
                os.remove(item)

    
    # Get pin list from technology layer map
    layer_map_path = os.path.join('.', 'ashes_fg', 'asic', 'lib', 'layer_map', tech_process + '.json')
    if not os.path.exists(layer_map_path): 
        raise CellNotFound(f'Could not open layer map {tech_process}.json. Is it in the ./lib/layer_map/ directory?')
    layer_map = json.load(open(layer_map_path))
    pin_list = make_pin_list(layer_map, tech_process)

    # Pick out relevant module and pre fill the module list with unique names of instances used
    # Flow currently handles one module at a time, give 'cells_only' module priority.
    cells_only_module = False
    for item in ast.modules:
        module_name = item.module_name.lower()
        if module_name == 'top' or module_name == 'cells_only':
            cells_only_module = True if module_name == 'cells_only' else False
            top_module = item
            for inst in item.module_instances:
                if inst.module_name not in module_list:
                    module_list.add(inst.module_name)
    
    # replace _num_ with <num> to side step parser for cadence vectorization 
    # Replace _plus_ with + character to side step verilog parser
    # update the port dictionary
    excluded_ports = set(['island_num', 'row', 'col'])
    for inst in top_module.module_instances:
        port_copy = {} 
        for p_key, p_value in inst.ports.items():
            pattern = r'_(\d+)_'
            matches = re.search(pattern, p_key)
            if p_key not in excluded_ports and matches:
                replacement = r'<\1>'
                p_key = re.sub(pattern, replacement, p_key, count=1)
            pattern = r'(?i)_PLUS_'
            matches = re.search(pattern, p_key)
            if p_key not in excluded_ports and matches:
                replacement = "+"
                p_key = re.sub(pattern, replacement, p_key, count=1)
            port_copy[p_key] = p_value
        inst.ports = port_copy

    # Parse cell GDS and instantiate cells in output layout based on modules used in verilog
    for inst in top_module.module_instances:
        if inst.module_name in module_list:
            cell_text = parse_cell_gds(inst.module_name, first_cell, cell_info, module_list, pin_list, layer_map, tech_process)
            if not routed_def: update_output_layout(cell_text, text_layout_path)
            first_cell = False

    if verbose: print('Cell Info:')
    if verbose: pprint.pprint(cell_info)
    if verbose: print(f'Module List:\n{top_module.module_instances}')

    # Separate cells into islands and arrange cell list to start at bottom left
    island_info = {}
    island_place = []
    island_neighbor = {}
    prev_col_idx = 0
    curr_row, max_row = 0, 0
    module_key_names = ['frame', 'decoder', 'switch', 'switch_ind']
    for inst in top_module.module_instances:
        inst_name = inst.instance_name.lower()
        if inst_name not in module_key_names:
            details = inst.ports
            num = int(details['island_num'])
            max_row = max(max_row, int(details['row']))
            if num not in island_info: 
                max_row = int(details['row'])
                prev_col_idx, curr_row = 1, int(details['row'])
                island_info.update({num : { 'deq': deque([inst]), 'max_row': max_row }})
            else:
                # Assumptions about module list:
                # - island descriptions are next to each other, once we see a new island the old one is finished
                # - row cells are next to each other, once we see a new row the old one is finished
                if int(details['row']) > curr_row:
                    island_info[num]['deq'].appendleft(inst)
                    curr_row = int(details['row'])
                    prev_col_idx = 1
                elif int(details['row']) <= curr_row:
                    island_info[num]['deq'].insert(prev_col_idx, inst)
                    prev_col_idx +=1
                island_info[num]['max_row'] = max_row
        elif inst_name == 'frame':
            frame_module = inst
        else:
            details = inst.ports
            num = int(details['island_num'])
            if num not in island_info:
                island_info[num] = {}
            if inst_name not in island_info[num]:
                island_info[num][inst_name] = []
            island_info[num][inst_name].append(inst)

    if verbose: print('Old Island Info:')
    if verbose: pprint.pprint(island_info)
    cell_order_in_island = {}
    island_params = (track_spacing, cell_pitch, cells_only_module)
    parse_cell_params = (module_list, pin_list, layer_map, tech_process, dbu, text_layout_path)
    island_text = generate_islands(island_info, cell_info, island_place, cell_order_in_island, design_area, frame_module, island_params, parse_cell_params)
    if verbose: 
        print(f'Island Placements:\n {island_place}')
        print('Post island gen, island info')
        pprint.pprint(island_info)

    txt2gds_path = os.path.join('.','ashes_fg','asic','txt2gds.py')
    if not routed_def:
        get_island_adjacent(island_place, island_neighbor)
        
        update_output_layout('BGNSTR: 122, 9, 12, 16, 36, 29, 122, 9, 24, 14, 16, 22\n', text_layout_path)
        update_output_layout(f'STRNAME: "{file_name_no_ext}"\n', text_layout_path)
        update_output_layout(island_text, text_layout_path)
        update_output_layout('ENDSTR\n', text_layout_path)
        update_output_layout('ENDLIB\n', text_layout_path)
        os.system(f'{pypath} {txt2gds_path} -o {gds_path} {text_layout_path}')

        generate_lef(module_list, cell_info, tech_process, lef_file_path, dbu, cell_order_in_island)

        metal_layers = count_metal_layers(layer_map, tech_process)
        def_params = (track_spacing, def_file_path, dbu, design_area, file_name_no_ext, frame_module, router_tool)
        def_blocks, def_nets = generate_def(island_info, cell_info, cell_order_in_island, def_params, metal_layers, nets_table)

        #island_info = sanitize_island_info(island_info)
        if verbose:
            #print(f'Cleaned up island info:\n {island_info}\n')
            print(f'Nets Table\n {nets_table}\n')
        
        #def_guide = global_router(island_info, cell_info, nets_table, island_place, metal_layers, track_spacing, guide_file_path, island_neighbor, design_area, frame_module)
        #if verbose: print(f'Post global router nets Table\n {nets_table}\n')

        #add_guide_to_def(def_file_path[:-4] + '_guide.def', def_blocks, def_nets, def_guide)
    else:
        rev_layer_map = reverse_pdk_doc(layer_map)
        if verbose: print(f'Reversed layer map:\n {rev_layer_map}')
        merge_def_with_gds(file_path, file_name_no_ext, rev_layer_map, cell_info, dbu, file_path, router_tool)
        os.system(f'{pypath} {txt2gds_path} -o {merged_gds_file_path} {text_merged_layout_path}')
    

def parse_cell_gds(name, first_cell, cell_info, module_list, pin_list, layer_map, tech_process):
    """
    Convert the cell gds to text
    - Omit header and libary tags for subsequent cells
    - Omit cell definitions for already defined cells
    - Track cell size and update cell info
    - Track cell pin location and update cell info
    - Handle cell rotation, mirroring and translation
    """
    ret_string, cell_pin_names, cell_pin_boxes = [], [], []
    lib_tags = {'HEADER', 'BGNLIB', 'UNITS', 'LIBNAME', 'ENDLIB'}
    max_x, min_x, max_y, min_y, cell_width, cell_height = None, None, None, None, None, None
    omit_record, track_pins, check_pin_text_layer, check_poly_layer, mirror_cell_x, mirror_cell_y = False, False, False, False, False, False
    sub_cell_name, text_layer, text_name, text_loc_X, text_loc_Y, poly_pin_layer = None, None, None, None, None, None
    poly_left, poly_bottom, poly_right, poly_top = None, None, None, None
    sref_name, aref_flag = None, False
    rotated_cell = False

    # add process variable 
    try:
        with open(os.path.join('.','ashes_fg','asic', 'lib', 'gds', tech_process, name + '.gds'),'rb') as bin_file:
            for rec in Record.iterate(bin_file):
                if omit_record:
                    if rec.tag_name == 'ENDSTR':
                        omit_record = False
                elif rec.tag_type == types.NODATA:
                    # Ignore all ENDLIB tags for individual cells
                    if rec.tag_name != 'ENDLIB':
                        ret_string.append(rec.tag_name + '\n')
                    # Add cell to unique list and reset max cell dimensions from subcells
                    if rec.tag_name == 'ENDSTR': 
                        # Update cell info once individual cell parsing is done
                        cell_width = max_x - min_x if max_x is not None and min_x is not None else 0
                        cell_height = max_y - min_y if max_y is not None and min_y is not None else 0
                        if verbose: print((f'Sub cell: {sub_cell_name} Min y: {min_y} Max y: {max_y}'))
                        cell_info.update({sub_cell_name: {'width': cell_width, 'height': cell_height, 'origin': (min_x, min_y)}})
                        max_x, min_x, max_y, min_y = None, None, None, None
                        # Stop tracking pins once end of cell is reached
                        # Add pin list to cell info of cell
                        if track_pins: 
                            track_pins = False
                            cell_pins = assign_pins_to_polygon(cell_pin_names, cell_pin_boxes, layer_map, pin_list[0][1])
                            cell_info[sub_cell_name]['cell_pins'] = cell_pins
                    # Inidicate a text record
                    if rec.tag_name == 'TEXT' and track_pins:
                        check_pin_text_layer = True
                        text_layer, text_name, text_loc_X, text_loc_Y = None, None, None, None
                    # Indicate a boundary record
                    if rec.tag_name == 'BOUNDARY' and track_pins:
                        check_poly_layer = True
                        poly_pin_layer = None
                        poly_left, poly_bottom, poly_right, poly_top = None, None, None, None
                    # Indicate an AREF record. Track this to treat its XY values differently
                    if rec.tag_name == 'AREF':
                        aref_flag = True

                    if rec.tag_name == 'ENDEL' and check_pin_text_layer:
                        check_pin_text_layer = False
                        if text_layer: cell_pin_names.append((text_layer, text_name, text_loc_X, text_loc_Y))
                    
                    if rec.tag_name == 'ENDEL' and check_poly_layer:
                        check_poly_layer = False
                        if poly_pin_layer: cell_pin_boxes.append((poly_pin_layer, poly_left, poly_bottom, poly_right, poly_top))
                    
                    if rec.tag_name == 'ENDEL' and (mirror_cell_x or mirror_cell_y):
                        mirror_cell_x = False
                        mirror_cell_y = False
                    
                    if rec.tag_name == 'ENDEL' and aref_flag:
                        aref_flag = False
                    
                    if rec.tag_name == 'ENDEL' and rotated_cell:
                        rotated_cell = False

                elif rec.tag_type == types.ASCII:
                    # Keep track of current sub cell name that hasnt been defined
                    sub_cell_name = rec.data.decode() if rec.tag_name == 'STRNAME' else sub_cell_name
                    # Only place header/lib tags for the first cell
                    if first_cell:
                        ret_string.append('%s: "%s"\n' % (rec.tag_name, rec.data.decode()))
                    elif rec.tag_name not in lib_tags:
                        # Check that the cell has not been defined previously
                        if rec.tag_name == 'STRNAME' and rec.data.decode() in cell_info:
                                omit_record = True
                                # This deletes the 'BGNSTR' line preceding the duplicate cell to omit
                                ret_string.pop()
                        else:
                            ret_string.append('%s: "%s"\n' % (rec.tag_name, rec.data.decode()))
                    
                    # If cell is already defined and is being called, account for its width
                    if rec.tag_name == 'SNAME':
                        max_x = max(int(cell_info[rec.data.decode()]['width']), max_x) if max_x else int(cell_info[rec.data.decode()]['width'])
                        # needs investigation
                        # However, i havent run into a situation where i need it so it stays commented out
                        #max_y = max(int(cell_info[rec.data.decode()]['height']), max_y)
                        sref_name = rec.data.decode()

                    # Start tracking pins for top level cells
                    if rec.tag_name == 'STRNAME' and sub_cell_name in module_list:
                        track_pins = True
                    
                    # If tracking pins and in a text record, add pin name only if layer was pin layer
                    if rec.tag_name == 'STRING' and check_pin_text_layer and text_layer:
                        text_name = rec.data.decode()

                elif rec.tag_type == types.BITARRAY:
                    ret_string.append('%s: %s \n' % (rec.tag_name, str(rec.data)))
                    if rec.tag_name == 'STRANS' and (rec.data & 0b1000000000000000) and sref_name:
                        mirror_cell_x = True
                else:
                    # Check to ensure record is not a header/lib tag
                    if first_cell:
                        ret_string.append('%s: %s\n' % (rec.tag_name, ', '.join('{0}'.format(i) for i in rec.data)))
                    elif rec.tag_name not in lib_tags:
                        ret_string.append('%s: %s\n' % (rec.tag_name, ', '.join('{0}'.format(i) for i in rec.data)))
                    
                    # If in a text record, check if layer is in pin list
                    if rec.tag_name == 'LAYER' and check_pin_text_layer:
                        text_layer = rec.data[0] if (str(rec.data[0]), pin_list[0][1]) in pin_list else text_layer
                    
                    # If in a boundary record, check if layer is in pin list
                    if rec.tag_name == 'LAYER' and check_poly_layer:
                        poly_pin_layer = rec.data[0] if (str(rec.data[0]), pin_list[0][1]) in pin_list else poly_pin_layer
                    
                    # If the datatype does not match pin list dataype, then reset poly pin layer
                    if rec.tag_name == 'DATATYPE' and poly_pin_layer:
                        poly_pin_layer = None if int(rec.data[0]) != int(pin_list[0][1]) else poly_pin_layer
                    
                    # Mirroring a cell across x axis and rotating 180 deg is same as mirror across y axis
                    if rec.tag_name == 'ANGLE' and mirror_cell_x and rec.data[0] == 180:
                        mirror_cell_y = True
                        mirror_cell_x = False
                    
                    if rec.tag_name == 'ANGLE' and rec.data[0] == 90.0:
                        rotated_cell = True

                    # Check for height and width of the cell
                    # Get location of pin
                    if rec.tag_name == 'XY':
                        for idx, item in enumerate(rec.data):
                            if idx % 2:
                                # keep track of min and max y
                                min_y = item if min_y is None else min(item, min_y)
                                max_y = item if max_y is None else max(item, max_y)
                                if sref_name and not mirror_cell_x and not mirror_cell_y and not rotated_cell and cell_info[sref_name]['width'] != 0 and idx == 1:
                                    temp_max = int(item) + cell_info[sref_name]['height'] + cell_info[sref_name]['origin'][1]
                                    #if (sub_cell_name == 'TSMC350nm_VinjDecode2to4_vtile') and verbose: 
                                    #    print(f'temp max y {temp_max}, item {item} sref_name {sref_name}')
                                    max_y = temp_max if max_y is None else max(temp_max, max_y) 
                            else:
                                # if cell is mirrored, update x pos
                                if mirror_cell_y:
                                    temp_w = cell_info[sref_name]['width'] + cell_info[sref_name]['origin'][0]
                                    #print(f'For a mirrored cell {sref_name}, its x pos is: {item}, cell width is {temp_w}')
                                    item = item - int(temp_w) if not aref_flag else item
                                # keep track of min and max x
                                min_x = item if min_x is None else min(item, min_x)
                                max_x = item if max_x is None else max(item, max_x)
                                # another max case is by adding width to origin of a sub cell. 
                                # Make sure to check if cell is not rotated or mirrored
                                if sref_name and not mirror_cell_x and not mirror_cell_y and not rotated_cell and cell_info[sref_name]['width'] != 0:
                                    temp_max = int(item) + cell_info[sref_name]['width'] + cell_info[sref_name]['origin'][0]
                                    max_x = temp_max if max_x is None else max(temp_max, max_x) 
                        sref_name = None
                        #if (sub_cell_name == 'TSMC350nm_VinjDecode2to4_vtile'):
                        #    print(f'Tracking TSMC350nm_VinjDecode2to4_vtile max y: {max_y}')
                        #    print(f'Rec Data: {rec.data}')        
                        # For a text record on a pin layer, get pin location
                        if check_pin_text_layer and text_layer:
                            text_loc_X, text_loc_Y = rec.data[0], rec.data[1]
                        # For a boundary record on a pin layer, get polygon location
                        if check_poly_layer and poly_pin_layer:
                            poly_left, poly_bottom, poly_right, poly_top = rec.data[0], rec.data[1], rec.data[4], rec.data[5]         
    except:
        raise CellNotFound(f'Problem opening cell {name}.gds file ?')
    return ''.join(ret_string)
    

def generate_islands(island_info, cell_info, island_place, cell_order_in_island, design_area, frame_module, island_params, parse_cell_params):
    ''' 
    Generate gds output for islands 
    - Place all cells and matrices into islands
    - Track cell placement and update island info
    - Track island placement 
    '''
    ret_string = []
    x_loc, y_loc, x_base, y_base = 0, 0, 0, 0
    track_spacing, cell_pitch, cells_only_module = island_params
    module_list, pin_list, layer_map, tech_process, dbu, text_layout_path = parse_cell_params
    rev_layer_map = reverse_pdk_doc(layer_map)

    if design_area:
        x_base, y_base = int(design_area[0] + design_area[4]), int(design_area[1] + design_area[5])
        x_loc, y_loc = x_base, y_base
        design_width = int(design_area[2] - design_area[0])
        design_height = int(design_area[3] - design_area[1])

    # Place pad frame if present
    if frame_module:
        ret_string.append('SREF\n')
        ret_string.append(f'SNAME: "{frame_module.module_name}"\n')
        ret_string.append('XY: 0, 0\n')
        ret_string.append('ENDEL\n')

    for val, island in island_info.items():
        # Determine relative cell orderings within the island
        col_widths = {}
        prev_row, prev_height, prev_col, prev_width = -1, -1, -1, -1
        block_left, block_bot, block_right, block_top = None, None, None, None
        first_cell = True
        cell_order = []
        if not cells_only_module:
            for inst in island['deq']:
                details = inst.ports
                cell_width = int(cell_info[str(inst.module_name)]['width'])
                cell_height = int(cell_info[str(inst.module_name)]['height'])
                curr_row = int(details['row'])
                curr_col = int(details['col'])

                # Track column widths for cells that need to skip
                # TODO: Add a feature to find col widths when bottom row needs offset
                if curr_col not in col_widths:
                    if 'matrix_row' in details:
                        col_widths[curr_col] = cell_width
                        for idx in range(curr_col + 1, int(details['matrix_col']) + 1):
                            col_widths[idx] = cell_width
                    else:
                        col_widths[curr_col] = cell_width
                
                # Reset x and update y for each row
                # Y location is estimated assuming that rows are defined in the ascending order in the verilog file
                if not first_cell and prev_row != curr_row:
                    x_loc = x_base
                    if curr_col != 1:
                        x_loc += calculate_offset(col_widths, curr_col-1)
                    y_loc = y_base + (island['max_row'] - curr_row)*cell_pitch if not block_top else block_top
                elif first_cell: 
                    first_cell = False
                    x_loc = x_base
                    y_loc = y_base
                
                prev_row = curr_row
                prev_height = cell_height
                prev_col = curr_col
                
                if 'matrix_row' in details:
                    mat_col, mat_row = int(details['matrix_col']), int(details['matrix_row'])
                    ref_str = 'AREF\n'
                    ret_string.append(ref_str)
                    ret_string.append(f'SNAME: "{inst.module_name}"\n')
                    col_row = f'COLROW: {mat_col}, {mat_row}\n'
                    ret_string.append(col_row)
                    if (x_loc == 0 and curr_col != 1) or (curr_col - prev_col > 1 and x_loc != 0):
                        x_loc += calculate_offset(col_widths, curr_col-1)
                    xy_tag = f'XY: {x_loc}, {y_loc}, {x_loc + mat_col*cell_width}, {y_loc}, {x_loc}, {y_loc + mat_row*cell_height}\n'
                    ret_string.append(xy_tag)
                    details['placement'] = (x_loc, y_loc, x_loc + mat_col*cell_width, y_loc + mat_row*cell_height )
                    block_left = x_loc if block_left is None else min(block_left, x_loc)
                    block_bot = y_loc if block_bot is None else min(block_bot, y_loc)
                    block_right = x_loc + mat_col*cell_width if block_right is None else max(block_right, x_loc + mat_col*cell_width)
                    block_top = y_loc + mat_row*cell_height if block_top is None else max(block_top, y_loc + mat_row*cell_height)
                    x_loc += mat_col*cell_width
                else:
                    ref_str = 'SREF\n'
                    ret_string.append(ref_str)
                    ret_string.append(f'SNAME: "{inst.module_name}"\n')
                    # TODO: Possibly Remove. Isn't this calculating offset twice?
                    if (x_loc == 0 and curr_col != 1) or (curr_col - prev_col > 1 and x_loc != 0):
                        x_loc += calculate_offset(col_widths, curr_col-1)
                    xy_tag = f'XY: {x_loc}, {y_loc}\n'
                    ret_string.append(xy_tag)
                    details['placement'] = (x_loc, y_loc, x_loc + cell_width, y_loc + cell_height )
                    block_left = x_loc if block_left is None else min(block_left, x_loc)
                    block_bot = y_loc if block_bot is None else min(block_bot, y_loc)
                    block_right = x_loc + cell_width if block_right is None else max(block_right, x_loc + cell_width)
                    block_top = y_loc + cell_height if block_top is None else max(block_top, y_loc + cell_height)
                    x_loc += cell_width
                
                ret_string.append('ENDEL\n')
            island_place.append((block_left, block_bot, block_right, block_top))
        else:
            for inst in island['deq']:
                details = inst.ports
                cell_width = int(cell_info[str(inst.module_name)]['width'])
                curr_col = int(details['col'])
                temp_order = [str(inst.module_name), curr_col, cell_width]
                key_except = ['island_num', 'row', 'col']
                temp_nets = {}
                for pin_key, pin_val in details.items():
                    if pin_key not in key_except:
                        temp_nets[pin_key] = pin_val
                if temp_nets: temp_order.append(temp_nets)
                cell_order.append(temp_order)
            cell_order.sort(key=lambda x: x[1])
            prev_x = 0
            intra_cell_padding = int(5*dbu)
            for idx in range(len(cell_order)):
                rel_x = prev_x
                rel_y = 0 if idx % 2 == 0 else cell_pitch
                cell_order[idx] = cell_order[idx][0:3] + [rel_x, rel_y] + cell_order[idx][3:]
                cell_width = cell_order[idx][2]
                prev_x += cell_width + intra_cell_padding
        if verbose: print(f'Cell order in island {cell_order}')
        
        # If required, perform mux generation. 
        # Create decoder tree
        mux_needed = 'decoder' in island and 'switch' in island
        if mux_needed:
            # Outline decoder cells 
            decoder_helper_suffix = ['_A_bridge', '_B_bridge', '_C_bridge', '_D_bridge', '_spacing', '_bridge_spacing']
            horz_decoder_array, vert_decoder_array = [], []
            horz_switch_array, vert_switch_array = [], []
            for inst in island['decoder']:
                decoder_array = []
                details = inst.ports
                bit_width = int(details['bits'])
                direction = details['direction']
                decoder_helper_prefix = str(inst.module_name)
                decoder_helper_cell_names = [decoder_helper_prefix+x for x in decoder_helper_suffix]
                for name in decoder_helper_cell_names:
                    cell_text = parse_cell_gds(name, False, cell_info, module_list, pin_list, layer_map, tech_process)
                    update_output_layout(cell_text, text_layout_path)
                    if verbose: pprint.pprint(cell_info[name])   
                total_outputs = 2**bit_width
                decoder_cols = int(math.ceil(math.log2(bit_width))+ math.ceil(math.log2(bit_width))-1)
                decoder_rows = int(math.ceil(total_outputs/4))
                # Compute as though vertical, transpose at the end if horizontal 
                bridge_cnt = 0
                for row in range(decoder_rows):
                    temp_row = []
                    for col in range(decoder_cols):
                        alpha = 4**(math.floor((decoder_cols-col-1)/2))
                        if col == decoder_cols -1:
                            temp_row.append(decoder_helper_prefix)
                        elif col == decoder_cols - 2:
                            names_idx = row % 4
                            temp_row.append(decoder_helper_cell_names[names_idx])
                        elif col % 2 == 1:
                            if row % alpha == 0:
                                temp_row.append(decoder_helper_cell_names[bridge_cnt])
                                bridge_cnt+= 1
                                bridge_cnt = 0 if bridge_cnt == 4 else bridge_cnt
                            else:
                                temp_row.append(decoder_helper_cell_names[5])
                        elif col % 2 == 0:
                            if row % alpha == 0:
                                temp_row.append(decoder_helper_prefix)
                            else:
                                temp_row.append(decoder_helper_cell_names[4])
                    decoder_array.append(temp_row)
                if direction == 'horizontal': 
                    decoder_array = list(zip(*decoder_array))
                    horz_decoder_array = decoder_array
                else:
                    vert_decoder_array = decoder_array
                if verbose: 
                    print(f'{direction} decoder {bit_width} bits')
                    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in decoder_array]))
            # Create switch vector for horz and vert
            # assume all directs first, then replace any specified columns with indirect swcs
            key_except = ['island_num', 'direction','num', 'type']
            for inst in island['switch']:
                details = inst.ports
                direction = details['direction']
                swc_cols = int(details['num'])
                swc_name = inst.module_name
                if direction == 'horizontal':
                    temp_row = [{'name':swc_name, 'nets':{}, 'pin_blockage':True} for x in range(swc_cols)]
                    for pin_key, pin_val in details.items():
                            if pin_key not in key_except:
                                swc_id = pin_key.split("_")[1]
                                swc_id = int(swc_id[1:])
                                swc_pin_key = pin_key.split("_")[2]
                                temp_row[swc_id]['nets'][swc_pin_key] = pin_val
                    horz_switch_array.append(temp_row)
                elif direction == 'vertical':
                    swc_type = details['type']
                    if swc_type == 'prog_switch': 
                        temp_row = [{'name':swc_name, 'nets':{}, 'pin_blockage':True} for x in range(swc_cols)]
                        for pin_key, pin_val in details.items():
                            if pin_key not in key_except:
                                # Pull out the number and pin name from the naming format switch_n#_<pin name>
                                # then associate the pin + net with the right cell
                                swc_id = pin_key.split("_")[1]
                                swc_id = int(swc_id[1:])
                                swc_pin_key = pin_key.split("_")[2]
                                temp_row[swc_id]['nets'][swc_pin_key] = pin_val
                        vert_switch_array.append(temp_row)
                    elif swc_type == 'drain_select': vert_switch_array.insert(0, [{'name':swc_name, 'nets':{}, 'pin_blockage':False} for x in range(swc_cols)])
                    
            vert_switch_array = list(zip(*vert_switch_array))
            if 'switch_ind' in island:
                for inst in island['switch_ind']:
                    details = inst.ports
                    direction = details['direction']
                    col_id = int(details['col']) - 1
                    swc_name = inst.module_name
                    horz_switch_array[0][col_id] = swc_name 
            if verbose: 
                print(f'horz switch')
                print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in horz_switch_array]))
                print(f'vert switch')
                print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in vert_switch_array]))
            # Align decoder and switches around the core cell island then update cell order.
            # Deal with vertical mux then calculate x-axis offset.
            if val not in cell_order_in_island:
                cell_order_in_island[val] = {'items': {}, 'coords': []}
            # First is decoders in vertical mux
            height_accum, coords_id = 0, 0
            for row in reversed(vert_decoder_array):
                width_accum = 0
                for col in row:
                    cell_width = cell_info[col]['width']
                    cell_height = cell_info[col]['height']
                    cell_order_in_island[val]['items'][coords_id] = {}
                    cell_order_in_island[val]['items'][coords_id]['type'] = 'cell'
                    cell_order_in_island[val]['items'][coords_id]['name'] = col
                    temp_coord = [width_accum, height_accum, width_accum + cell_width, height_accum + cell_height]
                    cell_order_in_island[val]['coords'].append(temp_coord)
                    coords_id += 1
                    width_accum += cell_width
                height_accum += int(cell_info[row[0]]['height'])
            # next update switches positioning
            height_accum = 0
            x_drainmux_offset = 0
            for item in vert_decoder_array[0]:
                x_drainmux_offset += cell_info[item]['width']
            for row in reversed(vert_switch_array):
                width_accum = x_drainmux_offset
                for col in row:
                    cell_width = cell_info[col['name']]['width']
                    cell_height = cell_info[col['name']]['height']
                    cell_order_in_island[val]['items'][coords_id] = {}
                    cell_order_in_island[val]['items'][coords_id]['type'] = 'cell'
                    cell_order_in_island[val]['items'][coords_id]['name'] = col['name']
                    temp_coord = [width_accum, height_accum, width_accum + cell_width, height_accum + cell_height]
                    cell_order_in_island[val]['coords'].append(temp_coord)
                    cell_order_in_island[val]['items'][coords_id]['nets'] = col['nets']
                    cell_order_in_island[val]['items'][coords_id]['pin_blockage'] = col['pin_blockage']
                    coords_id += 1
                    width_accum += cell_width
                height_accum += int(cell_info[row[0]['name']]['height'])
            drain_select_width = cell_info[str(vert_switch_array[0][0]['name'])]['width']
            prog_switch_width = cell_info[str(vert_switch_array[0][1]['name'])]['width']
            drainmux_spacing = 8*dbu
            x_drainmux_offset += drain_select_width + prog_switch_width + drainmux_spacing
            # Deal with core cells inside island
            for cell in cell_order:
                cell_width = cell[2]
                cell_height = cell_info[cell[0]]['height']
                cell_order_in_island[val]['items'][coords_id] = {}
                cell_order_in_island[val]['items'][coords_id]['type'] = 'cell'
                cell_order_in_island[val]['items'][coords_id]['pin_blockage'] = True
                cell_order_in_island[val]['items'][coords_id]['name'] = cell[0]
                temp_coord = [x_drainmux_offset + cell[3], cell[4], x_drainmux_offset + cell[3] + cell_width, cell[4] + cell_height]
                cell_order_in_island[val]['coords'].append(temp_coord)
                # Forward along the nets
                if len(cell) > 5: cell_order_in_island[val]['items'][coords_id]['nets'] = cell[5]
                cell[3] = x_drainmux_offset + cell[3]
                coords_id += 1
            # Deal with horizontal switches
            gatemux_spacing = 15*dbu
            height_accum += gatemux_spacing
            for idx, switch in enumerate(horz_switch_array[0]):
                if idx % 2 == 0:
                    x_loc = cell_order[idx][3]
                    y_loc = height_accum
                    cell_width = cell_info[switch['name']]['width']
                    cell_height = cell_info[switch['name']]['height']
                    cell_order_in_island[val]['items'][coords_id] = {}
                    cell_order_in_island[val]['items'][coords_id]['type'] = 'cell'
                    cell_order_in_island[val]['items'][coords_id]['name'] = switch['name']
                    temp_coord = [x_loc, y_loc, x_loc + cell_width, y_loc + cell_height]
                    cell_order_in_island[val]['items'][coords_id]['nets'] = switch['nets']
                    cell_order_in_island[val]['items'][coords_id]['pin_blockage'] = switch['pin_blockage']
                    cell_order_in_island[val]['coords'].append(temp_coord)
                    coords_id += 1
                    if (idx+1) < len(horz_switch_array[0]):
                        switch = horz_switch_array[0][idx+1]
                        x2_loc = x_loc + cell_width
                        cell_width = cell_info[switch['name']]['width']
                        cell_height = cell_info[switch['name']]['height']
                        cell_order_in_island[val]['items'][coords_id] = {}
                        cell_order_in_island[val]['items'][coords_id]['type'] = 'cell'
                        cell_order_in_island[val]['items'][coords_id]['name'] = switch['name']
                        temp_coord = [x2_loc, y_loc, x2_loc + cell_width, y_loc + cell_height]
                        cell_order_in_island[val]['items'][coords_id]['nets'] = switch['nets']
                        cell_order_in_island[val]['items'][coords_id]['pin_blockage'] = switch['pin_blockage']
                        cell_order_in_island[val]['coords'].append(temp_coord)
                        coords_id += 1
            # Place polygons to hook up nets that should have been connected via abutting. Mainly for gate side.
            # for switch: get x,y starting point. get all y offsets for nets. Find total width.
            # TODO: convert the hardcoded y offsets for 350 into a dynamic look up based on net names
            abut_net_x1 = x_drainmux_offset
            abut_net_y1 = height_accum
            switch_net_y_offsets = [3950, 5100, 6050, 12480, 19090, 20250]
            abut_net_last_swc_x_loc = cell_order_in_island[val]['coords'][coords_id-1][0]
            if verbose: print(f'Last switch placed should be {coords_id -1}')
            for yval in switch_net_y_offsets:
                cell_order_in_island[val]['items'][coords_id] = {}
                cell_order_in_island[val]['items'][coords_id]['type'] = 'polygon'
                cell_order_in_island[val]['items'][coords_id]['layer'] = 'METAL1'
                temp_coord = [abut_net_x1, abut_net_y1 + yval, abut_net_last_swc_x_loc, abut_net_y1 + yval + 500]
                cell_order_in_island[val]['coords'].append(temp_coord)
                coords_id += 1
            # deal with horizontal decoders and place polygons
            height_accum += cell_height
            for row_idx, row in enumerate(reversed(horz_decoder_array)):
                for idx, col in enumerate(row):
                    if (idx*2) < len(cell_order):
                        x_loc = cell_order[idx*2][3]
                        y_loc = height_accum
                        cell_width = cell_info[col]['width']
                        cell_height = cell_info[col]['height']
                        cell_order_in_island[val]['items'][coords_id] = {}
                        cell_order_in_island[val]['items'][coords_id]['type'] = 'cell'
                        cell_order_in_island[val]['items'][coords_id]['name'] = col
                        temp_coord = [x_loc, y_loc, x_loc + cell_width, y_loc + cell_height]
                        cell_order_in_island[val]['coords'].append(temp_coord)
                        coords_id += 1
                decoder_cell_row_y_offsets = [1990, 6990, 10600, 11850]
                decoder_bridge_row_y_offsets = [3500, 7500, 11500, 15500]
                abut_net_y1 = height_accum
                abut_net_last_swc_x_loc = cell_order_in_island[val]['coords'][coords_id-1][0]
                if row_idx % 2 == 0:
                    for yval in decoder_cell_row_y_offsets:
                        cell_order_in_island[val]['items'][coords_id] = {}
                        cell_order_in_island[val]['items'][coords_id]['type'] = 'polygon'
                        cell_order_in_island[val]['items'][coords_id]['layer'] = 'METAL1'
                        temp_coord = [abut_net_x1, abut_net_y1 + yval, abut_net_last_swc_x_loc, abut_net_y1 + yval + 500]
                        cell_order_in_island[val]['coords'].append(temp_coord)
                        coords_id += 1
                elif row_idx % 2 == 1:
                    for yval in decoder_bridge_row_y_offsets:
                        cell_order_in_island[val]['items'][coords_id] = {}
                        cell_order_in_island[val]['items'][coords_id]['type'] = 'polygon'
                        cell_order_in_island[val]['items'][coords_id]['layer'] = 'METAL1'
                        temp_coord = [abut_net_x1, abut_net_y1 + yval, abut_net_last_swc_x_loc, abut_net_y1 + yval + 500]
                        cell_order_in_island[val]['coords'].append(temp_coord)
                        coords_id += 1
                height_accum += cell_height
        else:
            coords_id = 0
            if val not in cell_order_in_island:
                cell_order_in_island[val] = {'items': {}, 'coords': []}
            for cell in cell_order:
                cell_width = cell[2]
                cell_height = cell_info[cell[0]]['height']
                cell_order_in_island[val]['items'][coords_id] = {}
                cell_order_in_island[val]['items'][coords_id]['type'] = 'cell'
                cell_order_in_island[val]['items'][coords_id]['name'] = cell[0]
                temp_coord = [cell[3], cell[4], cell[3] + cell_width, cell[4] + cell_height]
                cell_order_in_island[val]['coords'].append(temp_coord)
                # Forward along the nets
                if len(cell) > 5: cell_order_in_island[val]['items'][coords_id]['nets'] = cell[5]
                coords_id+=1
    if verbose: 
        print('Relative ordering within islands')
        pprint.pprint(cell_order_in_island) 
    # Fit islands into design area
    island_dims = []
    for val, island in cell_order_in_island.items():
        array = np.array(island['coords'])
        island_width = np.max(array[:, 2])
        island_height = np.max(array[:, 3])
        if island_width > design_width:
            raise ParsingError(f"Island num {val} is too wide ({island_width}nm) to fit in the design space ({design_width}nm)")
        elif island_height > design_height:
            raise ParsingError(f"Island num {val} is too tall ({island_height}nm) to fit in the design space ({design_height}nm)")
        island_dims.append([island_width, island_height, val])
        if verbose: print(f'island dims {island_width} x {island_height}')
    
    if cells_only_module:
        # find center left design area. starting with island 0, place them all in a row and update cell order doc
        x_loc = int(design_area[0])
        y_loc = int(design_height/2) + int(design_area[1])
        total_islands_width = sum(row[0] for row in island_dims)
        island_row_spacing = int(round((design_width - total_islands_width)/(len(island_dims) + 1), -3))
        if verbose: print(f'dynamic spacing {island_row_spacing}')
        for dim in island_dims:
            array = np.array(cell_order_in_island[dim[2]]['coords'])
            x_loc += island_row_spacing
            array[:, 0] += x_loc
            array[:, 2] += x_loc
            array[:, 1] += y_loc
            array[:, 3] += y_loc
            island_place.append([x_loc, y_loc])
            x_loc += dim[0] 
            cell_order_in_island[dim[2]]['coords'] = array.tolist()

    # gds write out
    for val, island in cell_order_in_island.items():
        for idx, item in island['items'].items():
            if item['type'] == 'cell':
                ret_string.append('SREF\n')
                c_name = item['name']
                ret_string.append(f'SNAME: "{c_name}"\n')
                array = island['coords']
                x_loc = array[idx][0]
                y_loc = array[idx][1]
                ret_string.append(f'XY: {x_loc}, {y_loc}\n')
                ret_string.append(f'ENDEL\n')
            elif item['type'] == 'polygon':
                layer_type = rev_layer_map[item['layer']+'_drawing']['layer_type']
                layer_type = layer_type.split(',')
                array = island['coords']
                left, bottom, right, top = array[idx][0], array[idx][1], array[idx][2], array[idx][3]
                ret_string.append('BOUNDARY\n')
                ret_string.append(f'LAYER: {layer_type[0]}\n')
                ret_string.append(f'DATATYPE: {layer_type[1]}\n')
                ret_string.append(f'XY: {left}, {bottom}, {right}, {bottom}, {right}, {top}, {left}, {top}, {left}, {bottom}\n')
                ret_string.append('ENDEL\n')

    return ''.join(ret_string)


def generate_lef(module_list, cell_info, tech_process, file_path, dbu, cell_order_in_island):
    '''
    Create a lef file for the design
    - Start with a copy of the technology lef
    - Use the module list to define any pins found
    '''

    # Copy the technology lef for the design
    tech_lef_path = os.path.join('.', 'ashes_fg', 'asic', 'lib', 'tech_lef', tech_process + '.lef')
    if os.path.exists(tech_lef_path): shutil.copy(tech_lef_path, file_path)
    else: raise CellNotFound(f'Could not find the technology lef file {tech_process}.lef. Is it in the ./lib/tech_lef/ directory?')

    lef_file = open(file_path, 'a')
    lef_file.write('\n\n') 
    seen = set()
    # Run through cell order dict
    for val, island in cell_order_in_island.items():
        for idx, item in island['items'].items():
            processed = 'name' in item and item['name'] in seen
            if item['type'] == 'cell' and not processed:
                module = item['name']
                lef_file.write(f'MACRO {module}\n')
                try:
                    pins = cell_info[module]['cell_pins']
                except:
                    if verbose:
                        print(f'Warning: module {module} has no pins defined on the cell.')
                    pins = {}
                for pin, value in pins.items():
                    lef_file.write(f'  PIN {pin}\n')
                    lef_file.write(f'    DIRECTION INOUT ;\n')
                    lef_file.write(f'    USE SIGNAL ;\n')
                    lef_file.write(f'    PORT\n')
                    layer = value['Layer']
                    lef_file.write(f'      LAYER {layer} ;\n')
                    rect = value['RECT']
                    lef_file.write(f'        RECT {rect[0]/dbu} {rect[1]/dbu} {rect[2]/dbu} {rect[3]/dbu} ;\n')
                    lef_file.write(f'    END\n')
                    lef_file.write(f'  END {pin}\n')
                lef_file.write(f'END {module}\n\n')
                seen.add(item['name'])
    
    # Double check the module list for things like frame 
    for module in module_list:
        processed = module in seen
        if not processed:
            lef_file.write(f'MACRO {module}\n')
            try:
                pins = cell_info[module]['cell_pins']
            except:
                if verbose:
                    print(f'Warning: module {module} has no pins defined on the cell.')
                pins = {}
            for pin, value in pins.items():
                lef_file.write(f'  PIN {pin}\n')
                lef_file.write(f'    DIRECTION INOUT ;\n')
                lef_file.write(f'    USE SIGNAL ;\n')
                lef_file.write(f'    PORT\n')
                layer = value['Layer']
                lef_file.write(f'      LAYER {layer} ;\n')
                rect = value['RECT']
                lef_file.write(f'        RECT {rect[0]/dbu} {rect[1]/dbu} {rect[2]/dbu} {rect[3]/dbu} ;\n')
                lef_file.write(f'    END\n')
                lef_file.write(f'  END {pin}\n')
            lef_file.write(f'END {module}\n\n')
            seen.add(module)

    lef_file.write('END LIBRARY')
    lef_file.close()

def generate_def(island_info, cell_info, cell_order_in_island, def_params, metal_layers, nets_table):
    '''
    Create a def file for the design
    - Place def instances around the edge for matrices
    - Route correct nets to correct instances
    - Create correct obstructions for routing
    '''
    track_spacing, file_path, dbu, design_area, file_name, frame_module, router_tool = def_params

    # Calculate num of tracks based on die area 
    num_tracks = (round(design_area[2]/track_spacing), round(design_area[3]/track_spacing))
    track_corner = (0,0)
    stop_layer = 3 # Metal layers to cover cells with (indicate which cells are Mx dense)
   
    header_str = 'VERSION 5.5 ;\nNAMESCASESENSITIVE ON ;\nDIVIDERCHAR "/" ;\nBUSBITCHARS "[]" ;\n\n'
    def_file = open(file_path, 'w')
    def_file.write(header_str) 

    def_file.write(f'DESIGN {file_name} ;\n\n')
    def_file.write(f'UNITS DISTANCE MICRONS {dbu} ;\n\n')
    def_file.write(f'DIEAREA ( {design_area[0]} {design_area[1]} ) ( {design_area[2]} {design_area[3]} ) ;\n\n')
    # Generate Tracks
    track_string = []
    for val in range(len(metal_layers), 0, -1):
        track_def = f'TRACKS X {track_corner[0]} DO {num_tracks[0]} STEP {track_spacing} LAYER {metal_layers[val-1]} ;\n'
        track_def += f'TRACKS Y {track_corner[1]} DO {num_tracks[1]} STEP {track_spacing} LAYER {metal_layers[val-1]} ;\n'
        track_string.append(track_def)
    def_file.write(''.join(track_string))
    comp_string = []
    rect_string = []
    
    def_blocks, def_nets = None, None
    nets_cnt, comp_cnt = 0, 0
    # Place components in def file
    if frame_module:
            comp_string.append(f'- {frame_module.instance_name} {frame_module.module_name} + PLACED ( 0 0 ) N ;\n')
            comp_cnt += 1
    # TODO: handle vectorized items when placing components
    for val, island in cell_order_in_island.items():
        for idx, item in island['items'].items():
            if item['type'] == 'cell':
                c_name = item['name']
                array = island['coords']
                x_loc = array[idx][0]
                y_loc = array[idx][1]
                comp_string.append(f'- I_{val}_{idx} {c_name} + PLACED ( {x_loc} {y_loc} ) N ;\n')
                comp_cnt += 1
    def_file.write(f'\nCOMPONENTS {comp_cnt} ;\n')
    def_file.write(''.join(comp_string))
    def_file.write('END COMPONENTS\n\n')
    def_file.close()
    shutil.copy(file_path, file_path[:-4] + '_guide.def')
    def_file = open(file_path, 'a')
    #rect_string[-1] = rect_string[-1][:-1] + ' ;\n'

    # Place blockages in def file
    pin_const = 1 # this is for amount of distance between blockage edge and true cell edge
    pin_spacing = 1*dbu # this is for space from pin block to pin
    pin_threshold = 1.5*dbu # this is the minimum distance between pins for a blockage to be inserted
    block_ext_len = 1*dbu # this is how far the block should extend from the internal blockage
    for val, island in cell_order_in_island.items():
        for idx, item in island['items'].items():
            if item['type'] == 'cell':
                array = island['coords']
                loc = array[idx]
                block_x1 = loc[0] + pin_const*dbu
                block_y1 = loc[1] + pin_const*dbu
                block_x2 = loc[2] - pin_const*dbu
                block_y2 = loc[3] - pin_const*dbu
                rect_string.append(f'    RECT ( {block_x1} {block_y1} ) ( {block_x2} {block_y2} )\n')
            # Insert blockages between pins around the edges
            if 'pin_blockage' in item and item['pin_blockage']:
                # Split ports into sides
                left_side, top_side, right_side, bot_side = [], [], [], []
                cell_pins = cell_info[item['name']]['cell_pins']
                for pin_item in cell_pins.values():
                    pin_left, pin_bot, pin_right, pin_top = loc[0] + int(pin_item['RECT'][0]), loc[1] + int(pin_item['RECT'][1]), loc[0] + int(pin_item['RECT'][2]), loc[1] + int(pin_item['RECT'][3])
                    extension_dirs = [abs(loc[0] - pin_left), abs(loc[1] - pin_bot), abs(loc[2] - pin_right), abs(loc[3] - pin_top)]
                    index_min = min(range(len(extension_dirs)), key=extension_dirs.__getitem__)
                    if index_min == 0:
                        left_side.append([pin_left, pin_bot, pin_right,pin_top])
                    elif index_min == 1:
                        bot_side.append([pin_left, pin_bot, pin_right,pin_top])
                    elif index_min == 2:
                        right_side.append([pin_left, pin_bot, pin_right,pin_top])
                    elif index_min == 3:
                        top_side.append([pin_left, pin_bot, pin_right,pin_top])
                # For each side, insert a new rect blockage if theres space around the pins
                left_side.sort(key=lambda x:x[1])
                prev_coord, pin_dist = None, None
                temp_y = None
                num_pins = len(left_side) - 1
                for ind, pin_coord in enumerate(left_side):
                    if prev_coord == None:
                        pin_dist = abs(pin_coord[1] - block_y1)
                        temp_y = block_y1
                    else:
                        pin_dist = abs(pin_coord[1] - prev_coord[3])
                        temp_y = prev_coord[3] + pin_spacing
                    prev_coord = pin_coord
                    if pin_dist > pin_threshold:
                        rect_string.append(f'    RECT ( {loc[0] - block_ext_len} {temp_y} ) ( {block_x1} {pin_coord[1] - pin_spacing} )\n')
                    # check how much space there was from last pin to edge of the side
                    if ind == num_pins:
                        pin_dist = abs(pin_coord[3] - block_y2)
                        if pin_dist > pin_threshold:
                            rect_string.append(f'    RECT ( {loc[0] - block_ext_len} {pin_coord[3] + pin_spacing} ) ( {block_x1} {block_y2} )\n')
                # check if there were no pins on left side
                if prev_coord == None:
                    rect_string.append(f'    RECT ( {loc[0] - block_ext_len} {block_y1} ) ( {block_x1} {block_y2} )\n')
                
                top_side.sort(key=lambda x:x[0])
                prev_coord, pin_dist = None, None
                temp_x = None
                num_pins = len(top_side) - 1
                for ind, pin_coord in enumerate(top_side):
                    if prev_coord == None:
                        pin_dist = abs(pin_coord[0] - block_x1)
                        temp_x = block_x1
                    else:
                        pin_dist = abs(pin_coord[0] - prev_coord[2])
                        temp_x = prev_coord[2] + pin_spacing
                    prev_coord = pin_coord
                    if pin_dist > pin_threshold:
                        rect_string.append(f'    RECT ( {temp_x} {block_y2} ) ( {pin_coord[0] - pin_spacing} {loc[3] + block_ext_len} )\n')
                    # check how much space there was from last pin to edge of the side
                    if ind == num_pins:
                        pin_dist = abs(pin_coord[2] - block_x2)
                        if pin_dist > pin_threshold:
                            rect_string.append(f'    RECT ( {pin_coord[2] + pin_spacing} {block_y2} ) ( {block_x2} {loc[3] + block_ext_len} )\n')
                # check if there were no pins on top side
                if prev_coord == None:
                    rect_string.append( f'    RECT ( {block_x1} {block_y2} ) ( {block_x2} {loc[3] + block_ext_len} )\n')
                
                right_side.sort(key=lambda x:x[1], reverse=True)
                prev_coord, pin_dist = None, None
                temp_y = None
                num_pins = len(right_side) - 1
                for ind, pin_coord in enumerate(right_side):
                    if prev_coord == None:
                        pin_dist = abs(pin_coord[3] - block_y2)
                        temp_y = block_y2
                    else:
                        pin_dist = abs(pin_coord[3] - prev_coord[1])
                        temp_y = prev_coord[1] - pin_spacing
                    prev_coord = pin_coord
                    if pin_dist > pin_threshold:
                        rect_string.append(f'    RECT ( {block_x2} {pin_coord[3] + pin_spacing} ) ( {loc[2] + block_ext_len} {temp_y} )\n')
                    # check how much space there was from last pin to edge of the side
                    if ind == num_pins:
                        pin_dist = abs(pin_coord[1] - block_y1)
                        if pin_dist > pin_threshold:
                            rect_string.append(f'    RECT ( {block_x2} {block_y1} ) ( {loc[2] + block_ext_len} {pin_coord[1] - pin_spacing} )\n')
                # check if there were no pins on right side
                if prev_coord == None:
                    rect_string.append(f'    RECT ( {block_x2} {block_y1} ) ( {loc[2] + block_ext_len} {block_y2} )\n')

                bot_side.sort(key=lambda x:x[0], reverse=True)
                prev_coord, pin_dist = None, None
                temp_x = None
                num_pins = len(bot_side) - 1
                for ind, pin_coord in enumerate(bot_side):
                    if prev_coord == None:
                        pin_dist = abs(pin_coord[2] - block_x2)
                        temp_x = block_x2
                    else:
                        pin_dist = abs(pin_coord[2] - prev_coord[0])
                        temp_x = prev_coord[0] - pin_spacing
                    prev_coord = pin_coord
                    if pin_dist > pin_threshold:
                        rect_string.append(f'    RECT ( {pin_coord[2] + pin_spacing} {loc[1] - block_ext_len} ) ( {temp_x} {block_y1} )\n')
                    # check how much space there was from last pin to edge of the side
                    if ind == num_pins:
                        pin_dist = abs(pin_coord[0] - block_x1)
                        if pin_dist > pin_threshold:
                            rect_string.append(f'    RECT ( {block_x1} {loc[1] - block_ext_len} ) ( {pin_coord[0] - pin_spacing} {block_y1} )\n')
                # check if there were no pins on bot side
                if prev_coord == None:
                    rect_string.append(f'    RECT ( {block_x1} {loc[1] - block_ext_len} ) ( {block_x2} {block_y1} )\n')
    
    # Change blockages syntax based on router. Qrouter accepts an older DEF syntax i believe.
    if router_tool != 'qrouter':
        def_file.write(f'BLOCKAGES {stop_layer} ;\n')
        for num in range(stop_layer):
            def_file.write(f'  - LAYER {metal_layers[num]}\n')
            def_file.write(''.join(rect_string))
        def_file.write(f'END BLOCKAGES\n\n')
    else:
        blocks_total = len(rect_string)*stop_layer
        def_file.write(f'BLOCKAGES {blocks_total} ;\n')
        for num in range(stop_layer):
            for single_rect in rect_string:
                def_file.write(f'  - {metal_layers[num]}\n')
                def_file.write(f'    LAYER {metal_layers[num]} ;\n')
                if single_rect[-2] != ';':
                    single_rect = single_rect[:-1] + ' ;\n'
                def_file.write(single_rect)
                def_file.write(f'  END\n\n')
        def_file.write(f'END BLOCKAGES\n\n')
    def_blocks = f'BLOCKAGES {stop_layer} ;\n'
    def_blocks += f'  - LAYER {metal_layers[0]}\n'
    if rect_string: rect_string[-1] = rect_string[-1][:-2] # These are for regenerating a def file with visible guide nets
    def_blocks += ''.join(rect_string)                

    # old code for def file generation. remove once function transition is complete.
    for island in island_info:
        inst_list = island_info[island]['deq']
        for inst in inst_list:
            pass
            #loc = inst.ports['placement']
            # If module is a matrix, place all cells around the edges
            #if 'matrix_row' in inst.ports:
            #    total_row = int(inst.ports['matrix_row'])
            #    total_col = int(inst.ports['matrix_col'])
            #    cell_height = cell_info[inst.module_name]['height']
            #    cell_width = cell_info[inst.module_name]['width']
            #    for i in range(total_row):
            #        for j in range(total_col):
            #            if i == 0 or i == total_row - 1 or j == 0 or j == total_col - 1: 
            #                comp_string.append(f'- {inst.instance_name}_{i*total_col + j} {inst.module_name} + PLACED ( {loc[0] + ((j)*cell_width) } {loc[1] + ((total_row - i - 1)*cell_height)} ) N ;\n')
            #                comp_cnt += 1
            #else:
            #    comp_string.append(f'- {inst.instance_name} {inst.module_name} + PLACED ( {loc[0]} {loc[1]} ) N ;\n')
            #    comp_cnt += 1
            
    # TODO: Handle vectorized cells for net connections
    for val, island in cell_order_in_island.items():
        for idx, item in island['items'].items():
            if item['type'] == 'cell' and 'nets' in item:
                for pin_name, pin_val in item['nets'].items():
                    # Remove brackets if present and append index to net name
                    net_name = pin_val if '[' not in pin_val else pin_val.split('[')[0] + '_' + pin_val.split('[')[1][:-1]
                    if net_name in nets_table:
                        nets_table[net_name].append((f'I_{val}_{idx}', pin_name))
                    else:
                        nets_table.update({net_name: [(f'I_{val}_{idx}', pin_name)]})
                        nets_cnt += 1
            '''
            # Convert all port values to string for substring search,
            vals = [str(i) for i in vals]
            # Check if instance has a net in the port list
            if next((s for s in vals if 'net' in s), None):
                # if the net is in a matrix, handle bus routing
                if 'matrix_row' in inst.ports:
                    for pin_name, pin_val in inst.ports.items():
                        pin_val = str(pin_val)
                        if 'net' in pin_val:
                            # To align instance number with net number for bus notation eg net[8:16], reset the instance number to zero because we assume groups of instances are always routed together. This should be a hard external requirement. 
                            # That is, if you have a matrix/vectorized block, you can only route all of them together.  
                            pattern = r'\[(\d+):(\d+)\]'
                            matches = re.findall(pattern, pin_val)
                            net_range_start = 0
                            net_range_stop = int(matches[0][1]) - int(matches[0][0])
                            for inst_num in range(net_range_start, net_range_stop):
                                # net name should be based on raw net number
                                net_number = int(matches[0][0]) + inst_num
                                net_name = pin_val.split('[')[0] + f'_{net_number}'
                                if net_name in nets_table:
                                    nets_table[net_name].append((inst.instance_name + f'_{inst_num}', pin_name))
                                else:
                                    nets_table.update({net_name: [(inst.instance_name + f'_{inst_num}', pin_name)]})
                                    nets_cnt += 1
                else:
                    for pin_name, pin_val in inst.ports.items():
                        pin_val = str(pin_val)
                        if 'net' in pin_val:
                            # Remove brackets if present and append index to net name
                            net_name = pin_val if '[' not in pin_val else pin_val.split('[')[0] + '_' + pin_val.split('[')[1][:-1]
                            if net_name in nets_table:
                                    nets_table[net_name].append((inst.instance_name, pin_name))
                            else:
                                nets_table.update({net_name: [(inst.instance_name, pin_name)]})
                                nets_cnt += 1  
            '''
    
    # Add frame pins to nets table
    if frame_module:
        frame_pins = frame_module.ports
        for pin_name, net_val in frame_pins.items():
            net_val = str(net_val)
            if net_val in nets_table:
                nets_table[net_val].append((frame_module.instance_name, pin_name))
            else:
                nets_table.update({net_val: [(frame_module.instance_name, pin_name)]})
                nets_cnt += 1
    
    def_file.write(f'NETS {nets_cnt} ;\n')
    def_nets = f'NETS {nets_cnt} ;\n'
    for n_name, n_list in nets_table.items():
        if len(n_list) > 1:
            def_file.write(f'- {n_name}\n  ')
            def_nets += f'- {n_name}\n  '
            for pin in n_list:
                def_file.write(f'( {pin[0]} {pin[1]} ) ')
                def_nets += f'( {pin[0]} {pin[1]} ) '
            def_file.write(f'\n;\n')
            def_nets += f'\n;\n'
    def_file.write('END NETS\n\n')
    def_nets += 'END NETS\n\n' # These are for regenerating a def file with visible guide nets
    
    def_file.write('END DESIGN')
    def_file.close()
    return def_blocks, def_nets
 

def merge_def_with_gds(file_path, file_name, layer_map, cell_info, dbu, pwd, router_tool):
    '''
    Convert routed def into polygons for gds
    '''
    def_file_name = f'{file_name}_routed.def' if router_tool != 'qrouter' else f'{file_name}_qroute.def'
    def_file_name = os.path.join(file_path, def_file_name)
    if not os.path.exists(def_file_name): 
        raise CellNotFound(f'Routed def file cannot be found.')
    
    routed_str = []
    def_file = open(def_file_name)
    parse_nets, parse_vias, update_via_doc = False, False, False
    single_net, special_net = False, False
    via_doc, metal_widths = {}, {}
    detector = HoleDetector(metal_width=int(0.5*dbu))
    prev_coords = None

    # Only chose this pattern because I was learning and testing out nested python functions
    def update_routed_str(left, bottom, right, top, routing_layer, layer_type, parse_vias=False, route_edge=False):
        left, bottom, right, top = int(left), int(bottom), int(right), int(top)
        if not parse_vias:
            coord_start = (int(left), int(bottom))
            coord_end = (int(right), int(top))
            # First check if metal layer exists in cache, if yes apply if not look it up and append to doc
            if routing_layer in metal_widths:
                net_width = int(metal_widths[routing_layer]/2)
            else:
                m_width = find_metal_in_lef(routing_layer, os.path.join(pwd, file_name), dbu)
                metal_widths[routing_layer] = m_width
                net_width = int(m_width/2)
            if special_net:
                width_ind = line.index("(") - 1
                net_width = int(int(line[width_ind])/2)
                route_edge = False
            if left == right:
                # Before expanding the vertical route, check if we're connecting an exisiting path or at a route edge
                if (int(left), int(bottom)) in prev_coords or route_edge:
                    bottom = int(bottom) - net_width
                if (int(right), int(top)) in prev_coords or route_edge:
                    top = int(top) + net_width
                # Expand the path as normal
                left = int(left) - net_width
                right = int(right) + net_width
            elif top == bottom:
                # Before expanding the horizontal route, check if we're connecting an exisiting path or at a route edge
                if (int(left), int(bottom)) in prev_coords or route_edge:
                    left = int(left) - net_width
                if (int(right), int(top)) in prev_coords or route_edge:
                    right = int(right) + net_width
                # Expand the path as normal
                bottom = int(bottom) - net_width 
                top = int(top) + net_width
            prev_coords.add(coord_start)
            prev_coords.add(coord_end)
        routed_str.append('BOUNDARY\n')
        routed_str.append(f'LAYER: {layer_type[0]}\n')
        routed_str.append(f'DATATYPE: {layer_type[1]}\n')
        routed_str.append(f'XY: {left}, {bottom}, {right}, {bottom}, {right}, {top}, {left}, {top}, {left}, {bottom}\n')
        routed_str.append('ENDEL\n')
        detector.add_rectangle(left, bottom, right, top, routing_layer)

    def merge_nonqrouter_def():
        if len(line) > 11 and line[3] == 'ROUTED':
            layer_type = layer_map[line[4]+'_drawing']['layer_type']
            layer_type = layer_type.split(',')
            left, bottom = line[6], line[7]
            right = line[10] if line[8] != '0' else line[11]
            top = line[11] if line[8] != '0' else line[12]
            update_routed_str(left, bottom, right, top, line[4])
        
        elif len(line) > 11 and len(line) < 17 and line[4] == 'NEW':
            layer_type = layer_map[line[5]+'_drawing']['layer_type']
            layer_type = layer_type.split(',')
            left, bottom = line[7], line[8]
            right = line[11] if line[9] != '0' else line[12]
            top = line[12] if line[9] != '0' else line[13]
            update_routed_str(left, bottom, right, top, line[5])
        
        elif len(line) > 5 and len(line) < 12 and line[4] == 'NEW':
            if line[10][:-1] in via_doc:
                via_list = via_doc[line[10][:-1]]
                for item in via_list:
                    layer_type = layer_map[item[0]+'_drawing']['layer_type']
                    layer_type = layer_type.split(',')
                    left, bottom = int(line[7]) + int(item[1]), int(line[8]) + int(item[2])
                    right, top = int(line[7]) + int(item[3]), int(line[8]) + int(item[4])
                    update_routed_str(left, bottom, right, top, None, parse_vias=True)
            else:
                via_ref = line[10][:-1]
                via_def = find_via_in_lef(via_ref, os.path.join(pwd, file_name), dbu)
                via_doc[via_ref] = via_def
                if verbose: print(f'VIA DOC {via_doc}')
                for item in via_def:
                    layer_type = layer_map[item[0]+'_drawing']['layer_type']
                    layer_type = layer_type.split(',')
                    left, bottom = int(line[7]) + int(item[1]), int(line[8]) + int(item[2])
                    right, top = int(line[7]) + int(item[3]), int(line[8]) + int(item[4])
                    update_routed_str(left, bottom, right, top, None, parse_vias=True)
                    
        elif len(line) >= 17 and line[4] == 'NEW':
            # This case handles when routes are described with single coordinate + rectangle offsets
            layer_type = layer_map[line[5]+'_drawing']['layer_type']
            layer_type = layer_type.split(',')
            left, bottom, right, top = int(line[7]) + int(line[12]), int(line[8]) + int(line[13]), int(line[7]) + int(line[14]), int(line[8]) + int(line[15])
            update_routed_str(left, bottom, right, top, line[5])

    def merge_qrouter_def():
        key_def1 = line[0] == '+'
        key_def2 = line[0] == '' and line[2] == 'NEW'
        if key_def1 or key_def2:
            route_layer_name = line[2] if key_def1 else line[3]
            layer_type = layer_map[route_layer_name+'_drawing']['layer_type']
            layer_type = layer_type.split(',')
            num_coords = line.count('(')
            cur_x, cur_y, prev_x, prev_y = None, None, None, None
            first_paren_ind, second_paren_ind = None, None
            try: 
                first_paren_ind =  line.index('(')
                second_paren_ind = line.index('(', first_paren_ind + 1)
            except:
                second_paren_ind = None
            for ind, el in enumerate(line):
                if line[ind] == '(':
                    cur_x = line[ind+1]
                    cur_y = line[ind+2]
                    cur_x = prev_x if cur_x == '*' else int(cur_x)
                    cur_y = prev_y if cur_y == '*' else int(cur_y)
                    if prev_x != None and num_coords >= 2:
                        left = min(prev_x, cur_x)
                        right = max(prev_x, cur_x)
                        bot = min(prev_y, cur_y)
                        top = max(prev_y, cur_y)
                        # Check for the start and end of a route to pad the ends
                        route_start = ind == second_paren_ind
                        last_paren_ind = len(line) - 1 - line[::-1].index('(')
                        route_end = last_paren_ind == ind
                        routed_edges = route_start or route_end
                        update_routed_str(left, bot, right, top, route_layer_name, layer_type, route_edge=routed_edges)
                    prev_x = cur_x
                    prev_y = cur_y
            # Via parsing
            if '_' in line[-2]:
                via_ref = line[-2][:-2]
                if via_ref not in via_doc:
                    via_def = find_via_in_lef(via_ref, os.path.join(pwd, file_name), dbu)
                    via_doc[via_ref] = via_def
                via_def = via_doc[via_ref]
                for via in via_def:
                    layer_type = layer_map[via[0]+'_drawing']['layer_type']
                    layer_type = layer_type.split(',')
                    update_routed_str(int(cur_x)+int(via[1]), int(cur_y)+int(via[2]), int(cur_x)+int(via[3]), int(cur_y)+int(via[4]), via[0], layer_type, parse_vias=True)

    for line in def_file:
        line = line.split(' ')
        if line[0] == 'NETS' or line[0] == 'SPECIALNETS':
            parse_nets = True
            special_net = True if line[0] == 'SPECIALNETS' else False
        elif parse_nets and line[0] == '-':
            prev_coords = set()
        elif parse_nets and (line[0] == ';'):
            prev_coords = None
        elif parse_nets:
            parse_nets = False if (line[0] == 'END' and parse_nets) else parse_nets
            special_net = False if (line[0] == 'END' and special_net) else special_net
            merge_nonqrouter_def() if (router_tool != 'qrouter') else merge_qrouter_def()
        # VIAS keyword was generated by triton route. 
        elif line[0] == 'VIAS':
            parse_vias = True
        elif parse_vias:
            parse_vias = False if (line[0] == 'END' and parse_vias) else parse_vias
            if len(line) == 3 and parse_vias: 
                update_via_doc = True
                via_name = line[1]
                via_doc.update({via_name: []}) 
            elif update_via_doc:
                update_via_doc = False if line[1] == ';' else update_via_doc
                if line[0] and parse_vias: via_doc[via_name].append((line[2], line[4], line[5], line[8], line[9]))
    holes = detector.find_holes()
    for hole, route_layer_name, direction in holes:
        if 'VIA' not in route_layer_name:
            layer_type = layer_map[route_layer_name+'_drawing']['layer_type']
            layer_type = layer_type.split(',')
            update_routed_str(hole[0][0], hole[0][1], hole[1][0], hole[1][1], route_layer_name, layer_type)
        if verbose: print(f"{direction.capitalize()} hole found on layer {route_layer_name}: {hole}")
    def_file.close()

    outfile = open(os.path.join(pwd, file_name + '_gds.txt'), 'r')
    outfile_routed = open(os.path.join(pwd, f'{file_name}_merged.txt'), 'w')
    for line in outfile:
        outfile_routed.write(line)
        if line == f'STRNAME: "{file_name}"\n':
            outfile_routed.write(''.join(routed_str))
    outfile.close()
    outfile_routed.close()


if __name__ == '__main__':
    # All units in nanometers
    tech_process = 'privA_65'
    dbu = 1000
    track_spacing = 250
    # placement offset to make space for pin routing
    # june run, small frame settings
    x_offset = 500*2*track_spacing 
    y_offset = 15*2*track_spacing
    design_area = (20.5e4, 21.76e4, 270.5e4, 24.25e4, x_offset, y_offset)
    
    start = time.time()
    gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, file_name, routed_def=False)
    end = time.time()
    #print('Time Taken:', (end-start) * 1000, "ms" )

