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



def gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, proj_name, routed_def=False):
    

    verilog_file_name = proj_name + '.v'
    file_name_no_ext = proj_name
    file_path = os.path.join('.', file_name_no_ext)
    ver_file = open(os.path.join('.', proj_name, 'verilog_files', verilog_file_name), 'r')
    ver_file_content = ver_file.read()
    ver_file.close()
    
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

    # Pre fill the module list with unique names of instances used
    for item in ast.modules:
        if item.module_name == 'TOP':
            top_module = item
            for inst in item.module_instances:
                if inst.module_name not in module_list:
                    module_list.add(inst.module_name)
    
    # Instantiate cells in output layout based on modules used in verilog
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
    for inst in top_module.module_instances:
        if inst.instance_name.lower() != 'frame':
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
        else:
            frame_module = inst
    if verbose: print('Old Island Info:')
    if verbose: pprint.pprint(island_info)
    island_text = generate_islands(island_info, cell_info, island_place, design_area, frame_module, track_spacing)
    if verbose: print(f'Island Placements:\n {island_place}')

    txt2gds_path = os.path.join('.','ashes_fg','asic','txt2gds.py')
    if not routed_def:
        get_island_adjacent(island_place, island_neighbor)
        
        update_output_layout('BGNSTR: 122, 9, 12, 16, 36, 29, 122, 9, 24, 14, 16, 22\n', text_layout_path)
        update_output_layout(f'STRNAME: "{file_name_no_ext}"\n', text_layout_path)
        update_output_layout(island_text, text_layout_path)
        update_output_layout('ENDSTR\n', text_layout_path)
        update_output_layout('ENDLIB\n', text_layout_path)
        os.system(f'{pypath} {txt2gds_path} -o {gds_path} {text_layout_path}')
        
        
        generate_lef(module_list, cell_info, tech_process, lef_file_path, dbu)

        metal_layers = count_metal_layers(layer_map, tech_process)
        def_blocks, def_nets = generate_def(island_info, cell_info, track_spacing, def_file_path, dbu, design_area, metal_layers, nets_table, file_name_no_ext, frame_module)

        island_info = sanitize_island_info(island_info)
        if verbose: print(f'Cleaned up island info:\n {island_info}\n')
        
        def_guide = global_router(island_info, cell_info, nets_table, island_place, metal_layers, track_spacing, guide_file_path, island_neighbor, design_area, frame_module)
        if verbose: print(f'Nets Table\n {nets_table}\n')

        add_guide_to_def(def_file_path[:-4] + '_guide.def', def_blocks, def_nets, def_guide)
    else:
        rev_layer_map = reverse_pdk_doc(layer_map)
        if verbose: print(f'Reversed layer map:\n {rev_layer_map}')
        merge_def_with_gds(file_path, file_name_no_ext, rev_layer_map, cell_info, dbu, file_path)
        os.system(f'{pypath} {txt2gds_path} -o {merged_gds_file_path} {text_merged_layout_path}')
    

def parse_cell_gds(name, first_cell, cell_info, module_list, pin_list, layer_map, tech_process):
    """
    Convert the cell gds to text
    - Omit header and libary tags for subsequent cells
    - Omit cell definitions for already defined cells
    - Track cell size and update cell info
    - Track cell pin location and update cell info
    """
    ret_string, cell_pin_names, cell_pin_boxes = [], [], []
    lib_tags = {'HEADER', 'BGNLIB', 'UNITS', 'LIBNAME', 'ENDLIB'}
    max_x, min_x, max_y, min_y, cell_width, cell_height = None, None, None, None, None, None
    omit_record, track_pins, check_pin_text_layer, check_poly_layer, mirror_cell_x, mirror_cell_y = False, False, False, False, False, False
    sub_cell_name, text_layer, text_name, text_loc_X, text_loc_Y, poly_pin_layer = None, None, None, None, None, None
    poly_left, poly_bottom, poly_right, poly_top = None, None, None, None
    sref_name, aref_flag = None, False

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
                        max_x, min_x, max_y, min_y = None, None, None, None
                        cell_info.update({sub_cell_name: {'width': cell_width, 'height': cell_height}})
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
                    if rec.tag_name == 'STRANS' and (rec.data & 0b1000000000000000):
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

                    # Check for height and width of the cell
                    # Get location of pin
                    if rec.tag_name == 'XY':
                        for idx, item in enumerate(rec.data):
                            if idx % 2:
                                # keep track of min and max y
                                min_y = item if min_y is None else min(item, min_y)
                                max_y = item if max_y is None else max(item, max_y)
                            else:
                                # if cell is mirrored, update x pos
                                if mirror_cell_y:
                                    temp_w = cell_info[sref_name]['width']
                                    #print(f'For a mirrored cell {sref_name}, its x pos is: {item}, cell width is {temp_w}')
                                    item = item - int(temp_w) if not aref_flag else item
                                # keep track of min and max x
                                min_x = item if min_x is None else min(item, min_x)
                                max_x = item if max_x is None else max(item, max_x)
                        #if (sub_cell_name == 'sky130_hilas_cellAttempt01d3_pt1'):
                            #print(f'Tracking sky130_hilas_cellAttempt01d3_pt1 min x: {min_x}')
                            #print(f'Rec Data: {rec.data}')        
                        # For a text record on a pin layer, get pin location
                        if check_pin_text_layer and text_layer:
                            text_loc_X, text_loc_Y = rec.data[0], rec.data[1]
                        # For a boundary record on a pin layer, get polygon location
                        if check_poly_layer and poly_pin_layer:
                            poly_left, poly_bottom, poly_right, poly_top = rec.data[0], rec.data[1], rec.data[4], rec.data[5]         
    except:
        raise CellNotFound(f'Problem opening cell {name}.gds file ?')
    return ''.join(ret_string)
    

def generate_islands(island_info, cell_info, island_place, design_area, frame_module, track_spacing):
    ''' 
    Generate gds output for islands 
    - Place all cells and matrices into islands
    - Track cell placement and update island info
    - Track island placement 
    '''
    # TODO: Dynamic spacing for islands in design area. 
    # - I could choose to have a variable offset value that represents the placed
    
    ret_string = []
    x_loc, y_loc, x_base, y_base = 0, 0, 0, 0

    if design_area:
        # Assign starting location for placement
        x_loc, y_loc, x_base, y_base = int(design_area[0] + design_area[4]), int(design_area[1] + design_area[5]), int(design_area[0] + design_area[4]), int(design_area[1] + design_area[5])

    # Place pad frame if present
    if frame_module:
        ret_string.append('SREF\n')
        ret_string.append(f'SNAME: "{frame_module.module_name}"\n')
        ret_string.append('XY: 0, 0\n')
        ret_string.append('ENDEL\n')

    # TODO: 
    # - equally space the islands based on design area
    # - Think about how I want to place islands whose height differs from others on the row
    #       - do i want to go back shift previous islands around?
    # - implement feature to push cell placement to back of queue if column offset hasnt been defined yet (eg WTA common bias)
    for val in island_info:
        island = island_info[val]
        col_widths = {}
        prev_row, prev_height, prev_col, prev_width = -1, -1, -1, -1
        block_left, block_bot, block_right, block_top = None, None, None, None
        first_cell = True
        cell_pitch = 6500
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
        ip = np.array(island_place)
        _, _, br_max, bt_max = ip.max(axis=0)
        # Island offset
        '''
        ip_widths = np.sum(ip[:, 2]) - np.sum(ip[:, 0]) # cant use ip because its empty as i havent placed all islands
        avail_width = design_area[2] - design_area[0] - ip_widths - design_area[4]
        horz_spacing = round(avail_width/len(island_info))
        x_base = br_max + horz_spacing

        # june run offset
        x_base = br_max + 115000
        y_base = int(design_area[1] + design_area[5])
        '''
        # arbgen offset values
        
        if val == 0:
            x_base = int(design_area[0] + design_area[4])
            y_base = bt_max + 35000
        else:
            x_base = br_max + 20000
            y_base = int(design_area[1] + design_area[5])
        
        
    return ''.join(ret_string)


def generate_lef(module_list, cell_info, tech_process, file_path, dbu):
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

    for module in module_list:
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
    lef_file.write('END LIBRARY')
    lef_file.close()

def generate_def(island_info, cell_info, track_spacing, file_path, dbu, design_area, metal_layers, nets_table, file_name, frame_module):
    '''
    Create a def file for the design
    - Place def instances around the edge for matrices
    - Route correct nets to correct instances
    '''

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
    # Iterate over components for handling:
    # [x] Placement for both matrices and single
    # [x] Blockages for both matrices and single
    # [x] Net connectivity for both matrices (vectorized) and single
    comp_string = []
    rect_string = []
    
    nets_cnt, comp_cnt = 0, 0
    # Place frame among def components
    if frame_module:
            comp_string.append(f'- {frame_module.instance_name} {frame_module.module_name} + PLACED ( 0 0 ) N ;\n')
            comp_cnt += 1
    
    for island in island_info:
        inst_list = island_info[island]['deq']
        for inst in inst_list:
            loc = inst.ports['placement']
            # If module is a matrix, place all cells around the edges
            if 'matrix_row' in inst.ports:
                total_row = int(inst.ports['matrix_row'])
                total_col = int(inst.ports['matrix_col'])
                cell_height = cell_info[inst.module_name]['height']
                cell_width = cell_info[inst.module_name]['width']
                for i in range(total_row):
                    for j in range(total_col):
                        if i == 0 or i == total_row - 1 or j == 0 or j == total_col - 1: 
                            comp_string.append(f'- {inst.instance_name}_{i*total_col + j} {inst.module_name} + PLACED ( {loc[0] + ((j)*cell_width) } {loc[1] + ((total_row - i - 1)*cell_height)} ) N ;\n')
                            comp_cnt += 1
            else:
                comp_string.append(f'- {inst.instance_name} {inst.module_name} + PLACED ( {loc[0]} {loc[1]} ) N ;\n')
                comp_cnt += 1
            # generate blockages based on cell size
            rect = f'    RECT ( {loc[0]} {loc[1]} ) ( {loc[2]} {loc[3]} )\n'
            rect_string.append(rect)
            # Track nets for both matrices and cells
            vals = inst.ports.values()
            # Convert all port values to string for substring search,
            # note: i dont like generators here, its just the first thing that worked
            vals = [str(i) for i in vals]
            # Check if instance has a net in the port list
            # note: i dont like generators here, its just the first thing that worked
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
    
    def_file.write(f'\nCOMPONENTS {comp_cnt} ;\n')
    def_file.write(''.join(comp_string))
    def_file.write('END COMPONENTS\n\n')
    def_file.close()
    shutil.copy(file_path, file_path[:-4] + '_guide.def')
    def_file = open(file_path, 'a')
    rect_string[-1] = rect_string[-1][:-1] + ' ;\n'

    def_file.write(f'BLOCKAGES {stop_layer} ;\n')
    for num in range(stop_layer):
        def_file.write(f'  - LAYER {metal_layers[num]}\n')
        def_file.write(''.join(rect_string))
    def_file.write(f'END BLOCKAGES\n\n')
    def_blocks = f'BLOCKAGES {stop_layer} ;\n'
    def_blocks += f'  - LAYER {metal_layers[0]}\n'
    rect_string[-1] = rect_string[-1][:-2] # These are for regenerating a def file with visible guide nets
    def_blocks += ''.join(rect_string)

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
 

def merge_def_with_gds(file_path, file_name, layer_map, cell_info, dbu, pwd):
    '''
    Convert routed def into polygons for gds
    '''
    def_file_name = f'{file_name}_routed.def'
    def_file_name = os.path.join(file_path, def_file_name)
    if not os.path.exists(def_file_name): 
        raise CellNotFound(f'Routed def file cannot be found. Is it named {file_name}_routed.def ?')
    
    routed_str = []
    def_file = open(def_file_name)
    parse_nets, parse_vias, update_via_doc = False, False, False
    single_net = False
    via_doc, metal_widths = {}, {}

    def update_routed_str(left, bottom, right, top, routing_layer, parse_vias=False):
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
            if left == right:
                # Before expanding the vertical route, check if we're connecting an exisiting path
                if (int(left), int(bottom)) in prev_coords:
                    bottom = int(bottom) - net_width
                if (int(right), int(top)) in prev_coords:
                    top = int(top) + net_width
                # Expand the path as normal
                left = int(left) - net_width
                right = int(right) + net_width
            elif top == bottom:
                # Before expanding the horizontal route, check if we're connecting an exisiting path
                if (int(left), int(bottom)) in prev_coords:
                    left = int(left) - net_width
                if (int(right), int(top)) in prev_coords:
                    right = int(right) + net_width
                # Expand the path as normal
                bottom = int(bottom) - net_width 
                top = int(top) + net_width
            prev_coords.add(coord_start)
            prev_coords.add(coord_end)

        routed_str.append(f'LAYER: {layer_type[0]}\n')
        routed_str.append(f'DATATYPE: {layer_type[1]}\n')
        routed_str.append(f'XY: {left}, {bottom}, {right}, {bottom}, {right}, {top}, {left}, {top}, {left}, {bottom}\n')
        routed_str.append('ENDEL\n')

    for line in def_file:
        line = line.split(' ')
        if line[0] == 'NETS':
            parse_nets = True
        elif parse_nets and line[0] == '-':
            single_net = True
            prev_coords = set()
        elif parse_nets and line[0] == ';':
            single_net = False
            prev_coords = None
        elif parse_nets:
            parse_nets = False if line[0] == 'END' else parse_nets
            if len(line) > 11 and line[3] == 'ROUTED':
                routed_str.append('BOUNDARY\n')
                layer_type = layer_map[line[4]+'_drawing']['layer_type']
                layer_type = layer_type.split(',')
                left, bottom = line[6], line[7]
                right = line[10] if line[8] != '0' else line[11]
                top = line[11] if line[8] != '0' else line[12]
                update_routed_str(left, bottom, right, top, line[4])
            
            elif len(line) > 11 and len(line) < 17 and line[4] == 'NEW':
                routed_str.append('BOUNDARY\n')
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
                        routed_str.append('BOUNDARY\n')
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
                        routed_str.append('BOUNDARY\n')
                        layer_type = layer_map[item[0]+'_drawing']['layer_type']
                        layer_type = layer_type.split(',')
                        left, bottom = int(line[7]) + int(item[1]), int(line[8]) + int(item[2])
                        right, top = int(line[7]) + int(item[3]), int(line[8]) + int(item[4])
                        update_routed_str(left, bottom, right, top, None, parse_vias=True)
                        
            elif len(line) >= 17 and line[4] == 'NEW':
                # This case handles when routes are described with single coordinate + rectangle offsets
                routed_str.append('BOUNDARY\n')
                layer_type = layer_map[line[5]+'_drawing']['layer_type']
                layer_type = layer_type.split(',')
                left, bottom, right, top = int(line[7]) + int(line[12]), int(line[8]) + int(line[13]), int(line[7]) + int(line[14]), int(line[8]) + int(line[15])
                update_routed_str(left, bottom, right, top, line[5])
        
        elif line[0] == 'VIAS':
            parse_vias = True
        elif parse_vias:
            parse_vias = False if line[0] == 'END' else parse_vias
            if len(line) == 3 and parse_vias: 
                update_via_doc = True
                via_name = line[1]
                via_doc.update({via_name: []}) 
            elif update_via_doc:
                update_via_doc = False if line[1] == ';' else update_via_doc
                if line[0] and parse_vias: via_doc[via_name].append((line[2], line[4], line[5], line[8], line[9]))
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

