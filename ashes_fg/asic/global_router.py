import numpy as np
import re
import math
from collections import OrderedDict as OD
from ashes_fg.asic.exceptions import *

track_idx_margin = 2 # number of tracks to skip from edges of design
verbose = True

def global_router(island_info, cell_info, nets_table, island_place, metal_layers, track_spacing, file_path, neighbor, design_area, frame_module):
    '''
    Generate a guide file that serves as global route input to the detailed router
    - Create bounding boxes around pins and extend them in pref direction
    - Seperate nets into channel based and A* nets
    - Handles all* combination of horizontal and vertical channel based nets
        - implemented: 
        [x] multi channel vertical routers
        [x] left only pins in vertical only channels
        [x] fix edge cases in combined channels with vert solution
        [x] Account for matrix instances
        [x] Write to guide file
        [x] bottom only pins
    - Implement IO pad routing
        - implemented:
        [x] add frame nets to table
            [x] calculate their preferred routing dir from design area
        [x] I think i want to move all non channel pins to the end of nets table, so they're handled last
        [x] Add a placement offset field, to give space for pin routing
        [x] separate nets that go directly from pin to pad vs nets that already connect other pins also going to pad
            [x] it would be good to use the traditional channel routing for connecting any internal nets
            [x] then for specifying io pins, I connect to that track
            [x] that way, im either connecting directly to a pin or a track!    
        [x] extend beyond routing are then Snap pins/tracks to both a vertical and horizontal global track
            [x] for tracks, first vert or horz then choose which direction i extend them to.
    TODO: 
    - Bug fix
        [] empty prev_poly array for random values of x/y offset
        [-] if an extension from a pin overlaps with a horizontal block, go up a layer. (detailed router can handle it)
            - this also means i need to start storing horizontal and vertical blocks under their layer names
    - Horizontal channel issues
        - adjust min height after detecting a vertical column next to the horizontal channel or adjust max height per channel
        - entering a separate horizontal channel (multi horizontal channel nets) 
    - backlog: 
        - implement pad to pad routing
        - handle when a vertical net already exists above the current pin
        - remove bounding box (?) or add as polygon to gds 
        - extend using the pin layer then lower/raise to routing layer (this exists hardcoded for just bottom facing pins)
    - open optimization question
        - figure out how to shift islands when a larger channel is needed
    '''
    net_str = []
    min_height = 0 
    min_width = 0 
    vert_widths = {} # dictionary of min/max widths for vertical channels
    max_width = None
    max_height = None
    horz_height = {} # dictionary of min/max heights per island
    bot_horz_chan = int(design_area[1] + design_area[5]) # input to global router should define the bottom row island placement of the horizontal channel its routing 
    def_guide = []
    sorted_nets_table = OD(nets_table)
    obstacles = [] # list of all fixed islands or densely routed areas.
    track_usage = {'horz': {}, 'vert': {}} # index of all vertical and horizontal placed polygons as part of a net
    
    # presort nets table to move pad nets to the back
    frame_nets = []
    for val in nets_table.keys():
        if val[0].lower() != 'c':
            frame_nets.append(val)
    for val in frame_nets:
        sorted_nets_table.move_to_end(val)
             
    
    for net_name, net_list in sorted_nets_table.items():
        net_str.append(f'{net_name}\n(\n')
        for idx, pin in enumerate(net_list):
            # split instance name to check for matrices
            inst_name = pin[0].split('_')
            inst_name_len = len(inst_name)
            # why am i determining matrices based on name length :/
            if inst_name_len == 3:
                # Get pin location in full design
                i_name = pin[0]
                cell_placement = island_info[pin[0]]['placement']
                pin_info = cell_info[island_info[pin[0]]['module_name']]['cell_pins'][pin[1]]
            elif inst_name_len == 4:
                # Get pin location in full design
                i_name = f'{inst_name[0]}__{inst_name[2]}'
                cell_mat_place = island_info[i_name]['placement']
                pin_info = cell_info[island_info[i_name]['module_name']]['cell_pins'][pin[1]]
                cell_width, cell_height = int(cell_info[island_info[i_name]['module_name']]['width']), int(cell_info[island_info[i_name]['module_name']]['height'])
                # Calculate offset for instance within the matrix
                #   - this code is just finding which row or column by dividng the current value by the total number in row or column
                #   - then it multiplies by the cell width or height to scale and adds the offset from placement
                # TODO: The if statement tries to account for edge case when the instance name is higher than the col/row even though it shouldnt be. 
                #   - for example 1 row with two columns but the net bundle has 4 nets all connected to the same bundle on a different cell. The net vector has 4 so i_name goes to 3 but there are only 2 instances. There is likely a better way to address this.
                col_multiple =  (int(island_info[i_name]['matrix_row']) - math.floor(int(inst_name[3]) / int(island_info[i_name]['matrix_col'])) - 1 ) if int(island_info[i_name]['matrix_row']) > math.floor(int(inst_name[3]) / int(island_info[i_name]['matrix_col'])) else 0

                cell_placement = [cell_mat_place[0] + (int(inst_name[3]) % int(island_info[i_name]['matrix_col']))*cell_width, cell_mat_place[1] + col_multiple*cell_height, cell_mat_place[2] + (int(inst_name[3]) % int(island_info[i_name]['matrix_col']))*cell_width, cell_mat_place[3] + col_multiple*cell_height]
            elif inst_name[0].lower() == 'frame':
                cell_placement = (0, 0)
                pin_info = cell_info[frame_module.module_name]['cell_pins'][pin[1]]
            else:
                raise WrongInstanceName(f'Instance {pin[0]} has too many underscores (Format: I__##). Please review def file to ensure the component was placed properly.')
            
            pin_left, pin_bot, pin_right, pin_top = cell_placement[0] + pin_info['RECT'][0], cell_placement[1] + pin_info['RECT'][1], cell_placement[0] + pin_info['RECT'][2], cell_placement[1] + pin_info['RECT'][3]
            # Figure out preferred extension direction
            if inst_name[0].lower() == 'frame':
                extension_dirs = [abs(design_area[2] - pin_left), abs(design_area[3] - pin_bot), abs(design_area[0] - pin_right), abs(design_area[1] - pin_top)]
            else:
                extension_dirs = [abs(cell_placement[0] - pin_left), abs(cell_placement[1] - pin_bot), abs(cell_placement[2] - pin_right), abs(cell_placement[3] - pin_top)]
            index_min = min(range(len(extension_dirs)), key=extension_dirs.__getitem__)
            pin_layer = pin_info['Layer']
            # Create bounding boxes around pins
            if index_min == 0:
                # Extend bounding box to the left
                net_list[idx] = (pin[0], pin[1], 'LEFT', pin_left - 400, pin_bot - 100, pin_right + 100, pin_top + 100, pin_layer)
                net_str.append(f'{pin_left - 400} {pin_bot - 100} {pin_right + 100} {pin_top + 100} {pin_layer}\n')
                def_guide.append((pin_left - 400, pin_bot - 100, pin_right + 100, pin_top + 100))
            elif index_min == 1:
                # Extend bounding box to the bottom
                net_list[idx] = (pin[0], pin[1], 'BOT', pin_left - 100, pin_bot - 400, pin_right + 100, pin_top + 100, pin_layer)
                net_str.append(f'{pin_left - 100} {pin_bot - 400} {pin_right + 100} {pin_top + 100} {pin_layer}\n')
                def_guide.append((pin_left - 100, pin_bot - 400, pin_right + 100, pin_top + 100))
                if pin_layer == 'M4':
                    net_str.append(f'{pin_left - 100} {pin_bot - 400} {pin_right + 100} {pin_top + 100} M3\n')
                    def_guide.append((pin_left - 100, pin_bot - 400, pin_right + 100, pin_top + 100))
            elif index_min == 2:
                # Extend bounding box to the right
                net_list[idx] = (pin[0], pin[1], 'RIGHT', pin_left - 100, pin_bot - 100, pin_right + 400, pin_top + 100, pin_layer)
                net_str.append(f'{pin_left - 100} {pin_bot - 100} {pin_right + 400} {pin_top + 100} {pin_layer}\n')
                def_guide.append((pin_left - 100, pin_bot - 100, pin_right + 400, pin_top + 100))
            elif index_min == 3:
                # Extend bounding box to the top
                net_list[idx] = (pin[0], pin[1], 'TOP', pin_left - 100, pin_bot - 100, pin_right + 100, pin_top + 400, pin_layer)
                net_str.append(f'{pin_left - 100} {pin_bot - 100} {pin_right + 100} {pin_top + 400} {pin_layer}\n')
                def_guide.append((pin_left - 100, pin_bot - 100, pin_right + 100, pin_top + 400)) 
        
        # Redirect channel based nets
        # Improvements to make:
        # [x] if there are multiple pins outside of the io pin, then 
        #   [x] modify netlist to extract io_pin out
        #   [x] go into island channel routing and store the track used to connect pins
        # [x] if theres pad routing to be done, confirm its either to a pin or track
        #       [x] extend the destination to a vertical or horizontal track  
        net_matrix = np.array(net_list)
        inst_names = net_matrix[:,0]
        pad_to_pin = True if 'FRAME' in inst_names else False
        pad_to_track = True if 'FRAME' in inst_names and len(np.where(inst_names != 'FRAME')[0]) > 1 else False
        channel_island = True if net_name[0].lower() == 'c' else False
        if channel_island or pad_to_track:
            if pad_to_track:
                iopad_pin = net_matrix[np.where(inst_names == 'FRAME')[0]][0]
                iopad_track = None
                net_matrix = net_matrix[np.where(inst_names != 'FRAME')[0]]
            
            # Check which type of channel the net is in
            pin_directions = net_matrix[:,2]
            vert_chan = True if 'LEFT' in pin_directions or 'RIGHT' in pin_directions else False
            horz_chan = True if 'TOP' in pin_directions or 'BOT' in pin_directions else False
            
            if vert_chan and horz_chan:
                # Find min height for horizontal
                # - Get all instance names that are below the channel
                tops_index = np.where(net_matrix == 'TOP')[0]  # finds the rows of top facing pins
                bot_index = np.where(net_matrix == 'BOT')[0]
                bot_pins_only = False
                
                # If top only or combination, generate a min height. For bottoms, generate max height
                #   - how to deal with variable max height? ie multi channel horizontal nets. 
                #   > I could just punt this as a more complex feature. Focus on simple one channel approach for both min and max height. I hate this approach but it is most pragmatic.
                if len(tops_index) > 0:
                    tops_insts = net_matrix[:,0][tops_index] # use rows for instance names
                    tops_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in tops_insts] # remove extra characters from matrix name
                    top_nums = np.unique(np.array([int(island_info[key]['island_num']) for key in tops_insts])) # use instance names to get their islands
                    min_height = max(np.amax(np.array(island_place)[:,3][top_nums]) + track_spacing, min_height)
                else:
                    bot_insts = net_matrix[:,0][bot_index]
                    bot_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in bot_insts]
                    bot_nums = np.unique(np.array([int(island_info[key]['island_num']) for key in bot_insts]))
                    max_height = np.amin(np.array(island_place)[:, 1][bot_nums]) - track_spacing if max_height is None else min(np.amin(np.array(island_place)[:, 1][bot_nums]) - track_spacing, max_height)
                    bot_pins_only = True

                # Find the pins in vertical channels, separate into lefts and rights
                right_index = np.where(net_matrix == 'RIGHT')[0]
                left_index = np.where(net_matrix == 'LEFT')[0]

                all_insts = net_matrix[:, 0]
                all_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in all_insts] # remove extra characters from matrix name
                right_insts = net_matrix[:,0][right_index]
                right_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in right_insts] # remove extra characters from matrix name
                
                island_nums =  np.array([int(island_info[key]['island_num']) for key in all_insts]) # island number at the pin index
                island_num_uni = np.unique(island_nums)
                
                '''
                - iterate through all islands mentioned in the net matrix and handle vertical channels
                - For each island, route the right facing and left facing pins at once
                    - right facing
                        - get adjacent island
                        - on the adjacent island, get the left facing pins on this net
                        - check for min width of the island, place track, route pins
                        - update vert_widths, track min and max x
                        - Add routed pin indices to a set
                    - left facing
                        - check if pin index has been routed
                        - if not, use max width to place track and route pins
                        - update routed pin set, vert min and max x, vert_widths
                '''
                vert_min_x, vert_max_x = None, None
                routed_pins = set()

                for num in island_num_uni: # For each island, route the right facing and left facing pins at once
                    # Right facing steps
                    right_face_idx = [i for i, val in enumerate(island_nums) if (i in right_index and val == num) ]  # index of pins from net matrix facing right on the current island
                    if len(right_face_idx) > 0:
                        adj_num = neighbor[num] # get the adjacent island
                        adj_isle_idx = None
                        if adj_num: 
                            adj_isle_idx = [i for i, val in enumerate(island_nums) if (i in left_index and val == adj_num) ] # index of pins facing left in the adjacent island
                        merged_idx = right_face_idx + adj_isle_idx if adj_isle_idx else right_face_idx # indices of all pins in channel

                        # pull min width from dictionary
                        if num in vert_widths and 'min_width' in vert_widths[num]: 
                            min_width = vert_widths[num]['min_width']
                        else:
                            min_width = island_place[num][2] + track_spacing
                        
                        # Calculate min_height
                        # find the max of the tops of all islands who are placed at bot_horz_chan
                        place_matrix = np.array(island_place)[:,1]
                        bot_chan_idxs = np.where(place_matrix == bot_horz_chan)[0]
                        min_height = np.amax(np.array(island_place)[:,3][bot_chan_idxs]) + track_spacing if not min_height else min_height

                        # Place track
                        track_left = min_width
                        track_bot = min(np.amin(net_matrix[:,4].astype(int)[merged_idx]), min_height) if not bot_pins_only else min(np.amin(net_matrix[:,4].astype(int)[merged_idx]), max_height)
                        track_right = min_width + track_spacing
                        track_top = max(min_height, np.amax(net_matrix[:,6].astype(int)[merged_idx])) if not bot_pins_only else max(max_height, np.amax(net_matrix[:,6].astype(int)[merged_idx]))
                        if num not in vert_widths:
                            vert_widths.update({num: {'min_width': track_right + track_spacing} })
                        else:
                            vert_widths[num].update({'min_width': track_right + track_spacing})
                        def_guide.append((track_left, track_bot, track_right, track_top))
                        net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[1]}\n')
            
                        
                        # Track the minimum and maximum placment of vertical tracks
                        vert_min_x = track_left if not vert_min_x else min(vert_min_x, track_left)
                        vert_max_x = track_right if not vert_max_x else max(vert_max_x, track_right)

                        # connect right facing and adjacent island pins to track
                        for pin in merged_idx:
                            box_left = min(net_list[pin][3], track_left)
                            box_bot = net_list[pin][4]
                            box_right = max(net_list[pin][5], track_right)
                            box_top = net_list[pin][6]
                            def_guide.append((box_left, box_bot, box_right, box_top))
                            net_str.append(f'{box_left} {box_bot} {box_right} {box_top} {metal_layers[0]}\n')
                        routed_pins.update(merged_idx)

                    # Left facing steps
                    left_face_idx = [i for i, val in enumerate(island_nums) if (i in left_index and i not in routed_pins and val == num) ]  # index of pins from net matrix facing left on the current island that havent been routed yet
                    if len(left_face_idx) > 0:
                        # update maximum width per vertical channel
                        if num in vert_widths and 'max_width' in vert_widths[num]:
                            max_width = min(vert_widths[num]['max_width'], island_place[num][0] - track_spacing)
                        else:
                            max_width = island_place[num][0] - track_spacing
                        
                        if num not in vert_widths:
                            vert_widths.update({num: {'max_width': max_width - 2*track_spacing} })
                        else:
                            vert_widths[num].update({'max_width': max_width - 2*track_spacing})

                        # Calculate min_height
                        # find the max of the tops of all islands who are placed at bot_horz_chan
                        place_matrix = np.array(island_place)[:,1]
                        bot_chan_idxs = np.where(place_matrix == bot_horz_chan)[0]
                        min_height = np.amax(np.array(island_place)[:,3][bot_chan_idxs]) + track_spacing if not min_height else min_height

                        # Assign track
                        track_left = max_width - track_spacing
                        track_bot = min(np.amin(net_matrix[:,4].astype(int)[left_face_idx]), min_height) if not bot_pins_only else min(np.amin(net_matrix[:,4].astype(int)[left_face_idx]), max_height)
                        track_right = max_width
                        track_top = max(min_height, np.amax(net_matrix[:,6].astype(int)[left_face_idx])) + track_spacing if not bot_pins_only else max(max_height, np.amax(net_matrix[:,6].astype(int)[left_face_idx]))
                        def_guide.append((track_left, track_bot, track_right, track_top))
                        net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[1]}\n')

                        # Track the minimum and maximum placment of vertical tracks
                        vert_min_x = track_left if not vert_min_x else min(vert_min_x, track_left)
                        vert_max_x = track_right if not vert_max_x else max(vert_max_x, track_right)

                        # Connect left facing pins to track
                        for pin in left_face_idx:
                            box_left = min(net_list[pin][3], track_left)
                            box_bot = net_list[pin][4]
                            box_right = max(net_list[pin][5], track_right)
                            box_top = net_list[pin][6]
                            def_guide.append((box_left, box_bot, box_right, box_top))
                            net_str.append(f'{box_left} {box_bot} {box_right} {box_top} {metal_layers[0]}\n')
                        routed_pins.update(left_face_idx)

                # Handle horizontal track placement and pin connections
                bot_index = np.where(net_matrix == 'BOT')[0]
                top_bot_idx = np.concatenate((tops_index, bot_index))
                leftmost_horz_pin = np.amin(net_matrix[:,3].astype(int)[top_bot_idx])
                rightmost_horz_pin = np.amax(net_matrix[:,5].astype(int)[top_bot_idx])
                track_left = min(leftmost_horz_pin, vert_min_x)
                track_bot = min_height if not bot_pins_only else max_height - track_spacing
                track_right = max(rightmost_horz_pin, vert_max_x)
                track_top = min_height + track_spacing if not bot_pins_only else max_height 
                if not bot_pins_only:
                    min_height = track_top + track_spacing
                else:
                    max_height = track_bot - track_spacing
                def_guide.append((track_left, track_bot, track_right, track_top))
                net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[0]}\n')
                iopad_track = (track_left, track_bot, track_right, track_top)

                for pin in top_bot_idx:
                    box_left = net_list[pin][3]
                    box_bot = min(net_list[pin][4], track_bot)
                    box_right = net_list[pin][5]
                    box_top = max(net_list[pin][6], track_top)
                    def_guide.append((box_left, box_bot, box_right, box_top))
                    net_str.append(f'{box_left} {box_bot} {box_right} {box_top} {metal_layers[1]}\n')

            # TODO (nice to have): 
            # - For both single channel and multi channel nets, calculate track capacity and ensure nets dont bump into adjacent island. For now, the spacing is sufficient
            #   - can get this from the min and max widths of adjacent islands
            # - check how much of a track is in use and how to fit more dog legs on the same row
            elif horz_chan and not vert_chan:
                # Get all instance names that are below the channel
                tops_index = np.where(net_matrix == 'TOP')[0]  # finds the indices of top facing pins
                bot_index = np.where(net_matrix == 'BOT')[0]
                bot_pins_only = False
                
                if len(tops_index) > 0:
                    tops_insts = net_matrix[:,0][tops_index] # use rows for instance names
                    tops_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in tops_insts] # remove extra characters from matrix name
                    island_nums = np.unique(np.array([int(island_info[key]['island_num']) for key in tops_insts])) # use instance names to get their islands
                    min_height = max(np.amax(np.array(island_place)[:,3][island_nums]) + track_spacing, min_height) # find the heights of just the selected islands and pick the max for min height to clear. This is the first track
                else:
                    bot_insts = net_matrix[:,0][bot_index]
                    bot_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in bot_insts]
                    bot_nums = np.unique(np.array([int(island_info[key]['island_num']) for key in bot_insts]))
                    max_height = np.amin(np.array(island_place)[:, 1][bot_nums]) - track_spacing if max_height is None else min(np.amin(np.array(island_place)[:, 1][bot_nums]) - track_spacing, max_height)
                    bot_pins_only = True
                
                # Assign Track 
                track_left = np.amin(net_matrix[:,3].astype(int)) # find left most pin
                track_bot = min_height if not bot_pins_only else max_height - track_spacing
                track_right = np.amax(net_matrix[:,5].astype(int)) # find right most pin
                track_top = min_height + track_spacing if not bot_pins_only else max_height 
                def_guide.append((track_left, track_bot, track_right, track_top))
                net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[0]}\n')
                iopad_track = (track_left, track_bot, track_right, track_top)

                # Connect pins to track 
                for pin in net_list:
                    box_left = pin[3]
                    box_bot = min(pin[4], track_bot)
                    box_right = pin[5]
                    box_top = max(pin[6], track_top)
                    def_guide.append((box_left, box_bot, box_right, box_top))
                    net_str.append(f'{box_left} {box_bot} {box_right} {box_top} {metal_layers[1]}\n')
                if not bot_pins_only:
                    min_height = min_height + 2*track_spacing
                else:
                    max_height = track_bot - track_spacing
            
            elif vert_chan and not horz_chan: 
                right_index = np.where(net_matrix == 'RIGHT')[0]
                left_index = np.where(net_matrix == 'LEFT')[0]
                all_insts = net_matrix[:, 0] 
                all_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in all_insts] # remove extra characters from matrix name
                right_insts = net_matrix[:,0][right_index]
                right_insts = [re.sub(r'_[^_]*$', '', val) if len(val) > 4 else val for val in right_insts] # remove extra characters from matrix name
                island_nums =  np.array([int(island_info[key]['island_num']) for key in all_insts]) # island number at the pin index
                island_num_uni = np.unique(island_nums)
                
                single_channel = False
                pins_on_one_island = len(island_num_uni) == 1 and ( len(left_index) == 0 or len(right_index) == 0 ) # pins on same island facing the same direction
                pins_on_adj_island = len(island_num_uni) == 2 and neighbor[island_num_uni[0]] == island_num_uni[1] # pins on adjacent islands facing each other
                # for each instance on this net
                # check if they're on the neighboring island
                # check if they're facing right, if so then set adj pins to false and break loop
                if pins_on_adj_island:
                    adj_neighbor = neighbor[island_num_uni[0]]
                    for pin_val in net_matrix:
                        if int(island_info[pin_val[0]]['island_num']) == int(adj_neighbor) and pin_val[2] == 'RIGHT':
                            pins_on_adj_island = False
                            break
                        elif int(island_info[pin_val[0]]['island_num']) == int(island_num_uni[0]) and pin_val[2] == 'LEFT':
                            pins_on_adj_island = False
                            break
                single_channel = True if pins_on_one_island or pins_on_adj_island else False

                if single_channel:
                    left_only_net = True if (len(right_index) == 0 and len(left_index) > 0) else False
                    if not left_only_net:
                        island_nums_right = np.unique(np.array([int(island_info[key]['island_num']) for key in right_insts]))
                        island_max = np.amax(np.array(island_place)[:,2][island_nums_right])
                        min_width = max(island_max + track_spacing, min_width)

                        num = island_nums_right[0]
                        # update minimum width per vertical channel
                        if num in vert_widths and 'min_width' in vert_widths[num]:
                            min_width = max(vert_widths[num]['min_width'], min_width)
                        
                        if num not in vert_widths:
                            vert_widths.update({num: {'min_width': min_width + 2*track_spacing} })
                        else:
                            vert_widths[num].update({'min_width': min_width + 2*track_spacing})
                        
                        # Assign Track 
                        track_left = min_width
                        track_bot = np.amin(net_matrix[:, 4].astype(int))
                        track_right = min_width + track_spacing
                        track_top = np.amax(net_matrix[:, 6].astype(int))
                        def_guide.append((track_left, track_bot, track_right, track_top))
                        net_str.append(f' {track_left} {track_bot} {track_right} {track_top} {metal_layers[1]}\n')
                        iopad_track = (track_left, track_bot, track_right, track_top)
                    
                    else: # Handle left only pins
                        num = island_nums[0]
                        # update maximum width per vertical channel
                        if num in vert_widths and 'max_width' in vert_widths[num]:
                            max_width = min(vert_widths[num]['max_width'], island_place[num][0] - track_spacing)
                        else:
                            max_width = island_place[num][0] - track_spacing
                        
                        if num not in vert_widths:
                            vert_widths.update({num: {'max_width': island_place[num][0] - 2*track_spacing} })
                        else:
                            vert_widths[num].update({'max_width': island_place[num][0] - 2*track_spacing})

                        # Assign track
                        track_left = max_width - track_spacing
                        track_bot = np.amin(net_matrix[:,4].astype(int))
                        track_right = max_width
                        track_top = np.amax(net_matrix[:,6].astype(int))
                        def_guide.append((track_left, track_bot, track_right, track_top))
                        net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[1]}\n')
                        iopad_track = (track_left, track_bot, track_right, track_top)

                    # Connect pins to track 
                    for pin in net_matrix:
                        box_left = min(int(pin[3]), track_left)
                        box_bot = pin[4]
                        box_right = max(int(pin[5]), track_right)
                        box_top = pin[6]
                        def_guide.append((box_left, box_bot, box_right, box_top))
                        net_str.append(f'{box_left} {box_bot} {box_right} {box_top} {metal_layers[0]}\n')
                
                else: # Handle multi channel vertical nets
                    vert_min_x, vert_max_x = None, None
                    routed_pins = set()

                    for num in island_num_uni: # For each island, route the right facing and left facing pins at once
                        # Right facing steps
                        right_face_idx = [i for i, val in enumerate(island_nums) if (i in right_index and val == num) ]  # index of pins from net matrix facing right on the current island
                        if len(right_face_idx) > 0:
                            adj_num = neighbor[num] # get the adjacent island
                            adj_isle_idx = None
                            if adj_num: 
                                adj_isle_idx = [i for i, val in enumerate(island_nums) if (i in left_index and val == adj_num) ] # index of pins facing left in the adjacent island
                            merged_idx = right_face_idx + adj_isle_idx if adj_isle_idx else right_face_idx # indices of all pins in channel

                            # pull min width from dictionary
                            if num in vert_widths and 'min_width' in vert_widths[num]: 
                                min_width = vert_widths[num]['min_width']
                            else:
                                min_width = island_place[num][2] + track_spacing
                            
                            # Calculate min_height
                            # find the max of the tops of all islands who are placed at bot_horz_chan
                            place_matrix = np.array(island_place)[:,1]
                            bot_chan_idxs = np.where(place_matrix == bot_horz_chan)[0]
                            min_height = np.amax(np.array(island_place)[:,3][bot_chan_idxs]) + track_spacing if not min_height else min_height

                            # Place track
                            track_left = min_width
                            track_bot = min(np.amin(net_matrix[:,4].astype(int)[merged_idx]), min_height)
                            track_right = min_width + track_spacing
                            track_top = max(min_height, np.amax(net_matrix[:,6].astype(int)[merged_idx]))
                            if num not in vert_widths:
                                vert_widths.update({num: {'min_width': track_right + track_spacing} })
                            else:
                                vert_widths[num].update({'min_width': track_right + track_spacing})
                            def_guide.append((track_left, track_bot, track_right, track_top))
                            net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[1]}\n')
                            
                            # Track the minimum and maximum placment of vertical tracks
                            vert_min_x = track_left if not vert_min_x else min(vert_min_x, track_left)
                            vert_max_x = track_right if not vert_max_x else max(vert_max_x, track_right)

                            # connect right facing and adjacent island pins to track
                            for pin in merged_idx:
                                box_left = min(net_list[pin][3], track_left)
                                box_bot = net_list[pin][4]
                                box_right = max(net_list[pin][5], track_right)
                                box_top = net_list[pin][6]
                                def_guide.append((box_left, box_bot, box_right, box_top))
                                net_str.append(f'{box_left} {box_bot} {box_right} {box_top} {metal_layers[0]}\n')
                            routed_pins.update(merged_idx)

                        # Left facing steps
                        left_face_idx = [i for i, val in enumerate(island_nums) if (i in left_index and i not in routed_pins and val == num) ]  # index of pins from net matrix facing left on the current island that havent been routed yet
                        if len(left_face_idx) > 0:
                            # update maximum width per vertical channel
                            if num in vert_widths and 'max_width' in vert_widths[num]:
                                max_width = min(vert_widths[num]['max_width'], island_place[num][0] - track_spacing)
                            else:
                                max_width = island_place[num][0] - track_spacing
                            if num not in vert_widths:
                                vert_widths.update({num: {'max_width': island_place[num][0] - 2*track_spacing} })
                            else:
                                vert_widths[num].update({'max_width': island_place[num][0] - 2*track_spacing})

                            # Calculate min_height
                            # find the max of the tops of all islands who are placed at bot_horz_chan
                            place_matrix = np.array(island_place)[:,1]
                            bot_chan_idxs = np.where(place_matrix == bot_horz_chan)[0]
                            min_height = np.amax(np.array(island_place)[:,3][bot_chan_idxs]) + track_spacing if not min_height else min_height

                            # Assign track
                            track_left = max_width - track_spacing
                            track_bot = min(np.amin(net_matrix[:,4].astype(int)[left_face_idx]), min_height)
                            track_right = max_width
                            track_top = max(np.amax(net_matrix[:,6].astype(int)[left_face_idx]), min_height)
                            def_guide.append((track_left, track_bot, track_right, track_top))
                            net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[1]}\n')

                            # Track the minimum and maximum placment of vertical tracks
                            vert_min_x = track_left if not vert_min_x else min(vert_min_x, track_left)
                            vert_max_x = track_right if not vert_max_x else max(vert_max_x, track_right)

                            # Connect left facing pins to track
                            for pin in left_face_idx:
                                box_left = min(net_list[pin][3], track_left)
                                box_bot = net_list[pin][4]
                                box_right = max(net_list[pin][5], track_right)
                                box_top = net_list[pin][6]
                                def_guide.append((box_left, box_bot, box_right, box_top))
                                net_str.append(f'{box_left} {box_bot} {box_right} {box_top} {metal_layers[0]}\n')
                            routed_pins.update(left_face_idx)
                            # subsequently update the max width each time
                            vert_widths[num]['max_width'] = track_left - track_spacing

                    # Horizontal Handling
                    track_left = vert_min_x
                    track_bot = min_height
                    track_right = vert_max_x
                    track_top = min_height + track_spacing
                    def_guide.append((track_left, track_bot, track_right, track_top))
                    net_str.append(f'{track_left} {track_bot} {track_right} {track_top} {metal_layers[0]}\n')
                    iopad_track = (track_left, track_bot, track_right, track_top)
                    min_height = min_height + 2*track_spacing
        
        if pad_to_track or pad_to_pin:
            # Connect the island track or pin to a global track
            if pad_to_track:
                # Extend the track beyond island placements 
                horz_track = True if (iopad_track[3] - iopad_track[1]) == track_spacing else False
                if horz_track:
                    # Extend left or right based on IO Pad location
                    ext_left = iopad_track[2] >= int(iopad_pin[3]) 
                    if ext_left:
                        # minimum of island placements, max widths rounded to the nearest track then go one track over
                        min_net, min_net_idx = min_placed_net(vert_widths)
                        min_island = np.amin(np.array(island_place)[:, 0])
                        far_left = min(min_net, min_island)
                        def_guide.append((far_left, iopad_track[1], iopad_track[2], iopad_track[3])) # Extend track out of channel
                        poly_left = round((far_left - design_area[0])/(2*track_spacing))*2*track_spacing - 2*track_spacing + design_area[0]
                        poly_bot = round((iopad_track[1] - design_area[1])/(2*track_spacing))*2*track_spacing + design_area[1] # extract the closest multiple of the track for the new bottom
                        poly_right = far_left + track_spacing
                        poly_top = poly_bot + track_spacing
                        # Add track spacing to create overlap between the extension and the track
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top)) # snap extension to a global track
                        if far_left == min_net:
                            vert_widths[min_net_idx]['min_width'] = poly_left
                    else: # extend right
                        max_net, max_net_idx = max_placed_net(vert_widths)
                        max_net = 0 if max_net is None else max_net
                        max_island = np.amax(np.array(island_place)[:, 2])
                        far_right = max(max_net, max_island)
                        def_guide.append((iopad_track[0], iopad_track[1], far_right, iopad_track[3])) # Extend track out of channel
                        poly_right = round((far_right - design_area[0])/(2*track_spacing))*2*track_spacing + 2*track_spacing + design_area[0]
                        poly_bot = round((iopad_track[1] - design_area[1])/(2*track_spacing))*2*track_spacing + design_area[1] # extract the closest multiple of the track for the new bottom
                        poly_top = poly_bot + track_spacing
                        # Subtract track spacing to create overlap between the extension and the track
                        poly_left = far_right - track_spacing
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top)) # snap extension to a global track
                        if far_right == max_net:
                            vert_widths[max_net_idx]['min_width'] = poly_right
                else: # vertical track
                    ext_bot = int(iopad_pin[4]) <= iopad_track[1]
                    if ext_bot:
                        min_island = min(np.amin(np.array(island_place)[:, 1]), max_height) if max_height else np.amin(np.array(island_place)[:, 1])
                        def_guide.append((iopad_track[0], min_island, iopad_track[2], iopad_track[1]))
                        poly_bot = round((min_island - design_area[1])/(2*track_spacing))*2*track_spacing - 2*track_spacing + design_area[1] # extract the closest multiple of the track for the new bottom
                        poly_left = round((iopad_track[0] - design_area[0])/(2*track_spacing))*2*track_spacing + design_area[0]
                        poly_right = poly_left + track_spacing
                        poly_top = min_island + track_spacing
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top)) # snap extension to a global track
                        if min_island == max_height:
                            max_height = poly_bot
                    else: # extend top
                        max_island = max(np.amax(np.array(island_place)[:, 3]), min_height)
                        def_guide.append((iopad_track[0], iopad_track[1], iopad_track[2], max_island))
                        poly_top = round((max_island - design_area[1])/(2*track_spacing))*2*track_spacing + 2*track_spacing + design_area[1] # extract the closest multiple of the track for the new top
                        poly_left = round((iopad_track[0] - design_area[0])/(2*track_spacing))*2*track_spacing + design_area[0]
                        poly_right = poly_left + track_spacing
                        poly_bot = max_island - track_spacing
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top)) # snap extension to a global track
                        if max_island == min_height:
                            min_height = poly_top
            else: # extend the pin beyond island area to help connect pad to pin
                island_pin = net_matrix[np.where(inst_names != 'FRAME')][0]
                pin_island_number = int(island_info[island_pin[0]]['island_num'])
                frame_pin = net_matrix[np.where(inst_names == 'FRAME')][0]
                if island_pin[2] == 'TOP':
                    min_height = horz_height[pin_island_number]['min_height'] if pin_island_number in horz_height and 'min_height' in horz_height[pin_island_number] else 0
                    max_island = max(island_place[pin_island_number][3], min_height)
                    poly_top = round((max_island - design_area[1])/(2*track_spacing))*2*track_spacing + 2*track_spacing + design_area[1] # extract the closest multiple of the track for the new top
                    def_guide.append((island_pin[3], island_pin[4], island_pin[5], poly_top))
                    net_str.append(f'{int(island_pin[3])} {int(island_pin[4])} {int(island_pin[5])} {int(poly_top)} {metal_layers[1]}\n')
                    ext_left =  int(frame_pin[3]) <= int(island_pin[3])
                    if ext_left:
                        min_net, min_net_idx = min_placed_net(vert_widths)
                        min_island = island_place[pin_island_number][0]
                        far_left = min(min_net, min_island) if min_net else min_island
                        poly_left = round((far_left - design_area[0])/(2*track_spacing))*2*track_spacing - 2*track_spacing + design_area[0]
                        poly_bot = poly_top - track_spacing
                        poly_right = int(island_pin[5])
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top))
                        net_str.append(f'{poly_left} {poly_bot} {poly_right} {poly_top} {metal_layers[0]}\n')
                        if far_left == min_net:
                            vert_widths[min_net_idx]['min_width'] = poly_left
                        if pin_island_number in horz_height:
                            horz_height[pin_island_number]['min_height'] = poly_top
                        else:
                            horz_height.update({pin_island_number: {'min_height': poly_top}})
                    else: # extend right
                        max_net, max_net_idx = max_placed_net(vert_widths)
                        max_net = 0 if max_net is None else max_net
                        max_right_island = island_place[pin_island_number][2]
                        far_right = max(max_net, max_right_island)
                        poly_right = round((far_right - design_area[0])/(2*track_spacing))*2*track_spacing + 2*track_spacing + design_area[0]
                        poly_left = int(island_pin[3])
                        poly_bot = poly_top - track_spacing
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top))
                        net_str.append(f'{int(poly_left)} {int(poly_bot)} {int(poly_right)} {int(poly_top)} {metal_layers[0]}\n')
                        if far_right == max_net:
                            vert_widths[max_net_idx]['min_width'] = poly_right
                        if pin_island_number in horz_height:
                            horz_height[pin_island_number]['min_height'] = poly_top
                        else:
                            horz_height.update({pin_island_number: {'min_height': poly_top}})
                elif island_pin[2] == 'BOT':
                    max_height = horz_height[pin_island_number]['max_height'] if pin_island_number in horz_height and 'max_height' in horz_height[pin_island_number] else None
                    min_island = min(island_place[pin_island_number][1], max_height) if max_height else island_place[pin_island_number][1]
                    poly_bot = round((min_island - design_area[1])/(2*track_spacing))*2*track_spacing - 2*track_spacing + design_area[1]
                    def_guide.append((island_pin[3], poly_bot, island_pin[5], island_pin[6]))
                    net_str.append(f'{island_pin[3]} {poly_bot} {island_pin[5]} {island_pin[6]} {metal_layers[1]}\n')
                    ext_left =  int(frame_pin[3]) <= int(island_pin[3])
                    if ext_left:
                        min_net, min_net_idx = min_placed_net(vert_widths)
                        min_left_island = island_place[pin_island_number][0]
                        far_left = min(min_net, min_left_island) if min_net else min_left_island
                        poly_left = round((far_left - design_area[0])/(2*track_spacing))*2*track_spacing - 2*track_spacing + design_area[0]
                        poly_top = poly_bot + track_spacing
                        poly_right = int(island_pin[5])
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top))
                        net_str.append(f'{int(poly_left)} {int(poly_bot)} {int(poly_right)} {int(poly_top)} {metal_layers[0]}\n')
                        if far_left == min_net:
                            vert_widths[min_net_idx]['min_width'] = poly_left
                        if pin_island_number in horz_height:
                            horz_height[pin_island_number]['max_height'] = poly_bot
                        else:
                            horz_height.update({pin_island_number: {'max_height': poly_bot}})
                    else: # extend right
                        max_net, max_net_idx = max_placed_net(vert_widths)
                        max_net = 0 if max_net is None else max_net
                        max_island = island_place[pin_island_number][2]
                        far_right = max(max_net, max_island)
                        poly_right = round((far_right - design_area[0])/(2*track_spacing))*2*track_spacing + 2*track_spacing + design_area[0]
                        poly_left = int(island_pin[3])
                        poly_top = poly_bot + track_spacing
                        def_guide.append((poly_left, poly_bot, poly_right, poly_top))
                        net_str.append(f'{int(poly_left)} {int(poly_bot)} {int(poly_right)} {int(poly_top)} {metal_layers[0]}\n')
                        if far_right == max_net:
                            vert_widths[max_net_idx]['min_width'] = poly_right
                        if pin_island_number in horz_height:
                            horz_height[pin_island_number]['max_height'] = poly_bot
                        else:
                            horz_height.update({pin_island_number: {'max_height': poly_bot}})
                # For vertical pins, extend passed the min or max width, then extend to the closer of: (top if islands/min height) or (bottom of islands)
                elif island_pin[2] == 'LEFT':
                    if pin_island_number in vert_widths:
                        min_net = None if 'max_width' not in vert_widths[pin_island_number] else vert_widths[pin_island_number]['max_width']
                    else:
                        min_net = None
                    far_left = min(island_place[pin_island_number][0], min_net) if min_net is not None else island_place[pin_island_number][0]
                    poly_left = round((far_left - design_area[0])/(2*track_spacing))*2*track_spacing - 2*track_spacing + design_area[0]
                    def_guide.append((poly_left, island_pin[4], island_pin[5], island_pin[6]))
                    net_str.append(f'{poly_left} {island_pin[4]} {island_pin[5]} {island_pin[6]} {metal_layers[0]}\n')
                    if far_left == min_net:
                            vert_widths[pin_island_number]['min_width'] = poly_left
                    poly_bot = int(island_pin[4])
                    poly_right = int(island_pin[5])
                    poly_top = int(island_pin[6])

                else: # Right Facing pins
                    if pin_island_number in vert_widths:
                        max_net = None if 'min_width' not in vert_widths[pin_island_number] else vert_widths[pin_island_number]['min_width']
                    else:
                        max_net = None
                    far_right = max(island_place[pin_island_number][2], max_net) if max_net is not None else island_place[pin_island_number][2]
                    poly_right = round((far_right - design_area[0])/(2*track_spacing))*2*track_spacing + 2*track_spacing + design_area[0]
                    poly_left = int(island_pin[3])
                    poly_bot = int(island_pin[4])
                    poly_top = int(island_pin[6])
                    def_guide.append((poly_left, poly_bot, int(poly_right), poly_top))
                    net_str.append(f'{poly_left} {poly_bot} {int(poly_right)} {poly_top} {metal_layers[0]}\n')
                    if far_right == max_net:
                            vert_widths[pin_island_number]['min_width'] = poly_right
            
            # Generate obstacles
            far_left = min(min_placed_net(vert_widths)[0], np.amin(np.array(island_place)[:, 0])) if min_placed_net(vert_widths)[0] else np.amin(np.array(island_place)[:, 0])
            far_right = max(max_placed_net(vert_widths)[0], np.amax(np.array(island_place)[:, 2])) if max_placed_net(vert_widths)[0] else np.amax(np.array(island_place)[:, 2])
            far_top = max(min_height, np.amax(np.array(island_place)[:, 3])) if min_height else np.amax(np.array(island_place)[:, 3])
            far_bot = min(max_height, np.amin(np.array(island_place)[:, 1])) if max_height else np.amin(np.array(island_place)[:, 1])
            # obstacles.append((far_left, far_bot, far_right, far_top)) 
            obstacles = island_place
            
            iopad_pin = frame_pin if not pad_to_track else iopad_pin
            if iopad_pin[2] == 'TOP' or iopad_pin[2] == 'BOT':
                des_horz_track_top_idx = round((design_area[3] - design_area[1])/(2*track_spacing)) - track_idx_margin
                horz_track_bot = design_area[1] + 2*track_spacing if iopad_pin[2] == 'TOP' else design_area[1] + (des_horz_track_top_idx-1)*2*track_spacing
                horz_track_top = horz_track_bot + track_spacing
                
                free_track = False
                track_idx_start = 1 + track_idx_margin if iopad_pin[2] == 'TOP' else des_horz_track_top_idx
                track_idx_stop = des_horz_track_top_idx -1 if iopad_pin[2] == 'TOP' else 0 + track_idx_margin
                track_idx_cnt = 1 if iopad_pin[2] == 'TOP' else -1
                
                # Find first unobstructed (by obstacles) track close to the frame
                for track_idx in range(track_idx_start, track_idx_stop, track_idx_cnt):
                    obstructed = True if (far_left < int(iopad_pin[3]) < far_right or far_left < int(iopad_pin[5]) < far_right) and (far_bot < horz_track_bot < far_top or far_bot < horz_track_top < far_top) else False
                    
                    if not obstructed:
                        free_track = True
                        break
                    else:
                        horz_track_bot = track_idx*2*track_spacing + design_area[1]
                        horz_track_top = horz_track_bot + track_spacing
                
                if not free_track:
                    raise NoHorizontalTracks(f'Too many obstacles in design are preventing net {net_name} from finding an open track.')
                
                # Extend the pin from the frame into the design area on a vertical track
                # TODO: make sure to only extend over obstacles with higher layer metals (or do i want to route around?)
                #   - specify the option from a higher level. how many levels of metal available and ask user for pref
                vert_track_left = round((int(iopad_pin[3]) - design_area[0])/(2*track_spacing))*2*track_spacing + design_area[0]
                vert_track_right = vert_track_left + track_spacing
                track_idx = round((vert_track_left - design_area[0])/(2*track_spacing))
                track_usage_bot = min(int(iopad_pin[6]), horz_track_bot)
                track_usage_top = max(int(iopad_pin[6]), horz_track_bot)
                if track_idx in track_usage['vert']:
                    track_usage['vert'][track_idx].append((track_usage_bot, track_usage_top))
                else:
                    track_usage['vert'][track_idx] = [(track_usage_bot, track_usage_top)]
                def_guide.append((vert_track_left, iopad_pin[6], vert_track_right, horz_track_bot))
                net_str.append(f'{int(vert_track_left)} {int(iopad_pin[6])} {int(vert_track_right)} {int(horz_track_bot)} {metal_layers[1]}\n')
                
                prev_dir = None
                prev_poly = []
                # Extend left or right to the pin
                if vert_track_left > poly_right:
                    start = (vert_track_left, horz_track_bot, vert_track_right, horz_track_top)
                    if island_pin[2] == 'TOP' or island_pin[2] == 'BOT' or island_pin[2] == 'RIGHT':
                        stop = (poly_right, poly_bot, poly_right, poly_top)
                    else:
                        stop = (poly_left, poly_bot, poly_left, poly_top)
                    ex_val = extend(start, stop, 'LEFT', obstacles, track_usage, design_area, track_spacing, prev_dir, prev_poly, metal_layers)
                    prev_dir = 'LEFT'

                elif vert_track_left <= poly_right:
                    start = (vert_track_left, horz_track_bot, vert_track_right, horz_track_top)
                    if island_pin[2] == 'TOP' or island_pin[2] == 'BOT' or island_pin[2] == 'LEFT':
                        stop = (poly_left, poly_bot, poly_left + track_spacing, poly_top)
                    else:
                        stop = (poly_right, poly_bot, poly_right, poly_top)
                    ex_val = extend(start, stop, 'RIGHT', obstacles, track_usage, design_area, track_spacing, prev_dir, prev_poly, metal_layers)
                    prev_dir = 'RIGHT'
               
                # Extend up or down to the pin
                if verbose: 
                    print(f'\nprev poly state:\n{prev_poly} \nand direction {prev_dir} \nwhen routing net {net_name}')
                    print(f'vert track left: {vert_track_left} and poly left {poly_left} and poly right {poly_right}')
                    print(f'iopad_pin {iopad_pin}')
                curr_poly = prev_poly[-1]
                if horz_track_bot > int(poly_top):
                    if prev_dir == 'LEFT':
                        start = (curr_poly[0], curr_poly[1], curr_poly[0] + track_spacing, curr_poly[3])
                        stop = (curr_poly[0], poly_bot, curr_poly[0] + track_spacing, poly_top)
                    elif prev_dir == 'RIGHT':
                        start = (curr_poly[2] - track_spacing, curr_poly[1], curr_poly[2], curr_poly[3])
                        stop = (curr_poly[2] - track_spacing, poly_bot, curr_poly[2], poly_top)
                    ex_val = extend(start, stop, 'BOT', obstacles, track_usage, design_area, track_spacing, prev_dir, prev_poly, metal_layers)

                elif horz_track_top < poly_bot:
                    if prev_dir == 'LEFT':
                        start = (curr_poly[0], curr_poly[1], curr_poly[0] + track_spacing, curr_poly[3])
                        stop = (curr_poly[0], poly_bot, curr_poly[0] + track_spacing, poly_top)
                    elif prev_dir == 'RIGHT':
                        start = (curr_poly[2] - track_spacing, curr_poly[1], curr_poly[2], curr_poly[3])
                        stop = (curr_poly[2] - track_spacing, poly_bot, curr_poly[2], poly_top)

                    ex_val = extend(start, stop, 'TOP', obstacles, track_usage, design_area, track_spacing, prev_dir, prev_poly, metal_layers)
                
                for item in prev_poly:
                    net_str.append(f'{int(item[0])} {int(item[1])} {int(item[2])} {int(item[3])} {item[4]}\n')
                    def_guide.append((int(item[0]), int(item[1]), int(item[2]), int(item[3])))
        net_str.append(')\n')
    
    if verbose: print(f'island min and max widths:\n{vert_widths}')
    if verbose: print(f'Track usage:\n {track_usage}')
    guide_file = open(file_path, 'w', newline='\n')
    guide_file.write(''.join(net_str))
    guide_file.close()
    nets_table = sorted_nets_table
    return def_guide   

def min_placed_net(widths):
    ret, idx = None, None
    for key, val in widths.items():
        if 'max_width' in val:
            ret = val['max_width'] if ret is None else min(val['max_width'], ret)
            if ret == val['max_width']:
                idx = key
    return ret, idx

def max_placed_net(widths):
    ret,idx = None, None
    for key, val in widths.items():
        if 'min_width' in val:
            ret = val['min_width'] if ret is None else max(val['min_width'], ret)
            if ret == val['min_width']:
                idx = key
    return ret, idx

def extend(start, stop, routing_dir, obstacles, track_usage, design_area, track_spacing, prev_dir, prev_poly, metal_layers):
    '''
    Return polygons connecting two points along a track in the specified routing direction while avoiding obstacles
    '''
    #TODO: 
    # - [x] convert distance values to idxs when looking up track usage 
    # - [x] fix vertical dictionary indices
    # - [x] make sure subsequent tracks are connected to the original start point
    # - [x] add in track usage look up logic
    # - add in obstacle detection logic
     
    start_left = start[0]
    start_bot = start[1]
    start_right = start[2]
    start_top = start[3]

    stop_left = stop[0]
    stop_bot = stop[1]
    stop_right = stop[2]
    stop_top = stop[3]

    start_left_idx = round((start_left - design_area[0])/(2*track_spacing))
    start_bot_idx = round((start_bot - design_area[1])/(2*track_spacing))
    horz_max_idx = round((design_area[2] - design_area[0])/(2*track_spacing)) - track_idx_margin
    vert_max_idx = round((design_area[3] - design_area[1])/(2*track_spacing)) - track_idx_margin


    if routing_dir == 'TOP':
        increment_right = False
        if prev_dir:
            # find the closest island, and calculate preferred track increment from its sides
            closest_blob_idx, closest_blob_val = None, None
            for blob_idx, blob in enumerate(obstacles):
                dist_to_blob = min( min( abs(start_left - blob[0]), abs(start_left - blob[2]) ) ,  min( abs(start_right - blob[0]), abs(start_right - blob[2]) ) ) 
                if closest_blob_idx:
                    closest_blob_idx = blob_idx if dist_to_blob < closest_blob_val else closest_blob_idx
                    closest_blob_val = dist_to_blob if dist_to_blob < closest_blob_val else closest_blob_val
                else:
                    closest_blob_idx = blob_idx
                    closest_blob_val = dist_to_blob
            closest_blob = obstacles[closest_blob_idx]
            increment_right = abs(closest_blob[2] - start_left) < abs(closest_blob[0] - start_left)
        elif prev_dir is None:
            # choose increment direction based on start's proximity to either left or right of the design (ie which side of the frame are we on)
            pass
        
        if increment_right:
            rng_start = start_left_idx
            rng_stop = horz_max_idx
            rng_count = 1
        else:
            rng_start = start_left_idx
            rng_stop = 1 + track_idx_margin
            rng_count = -1
        
        for idx in range(rng_start, rng_stop, rng_count):
            naive_place = True
            if idx in track_usage['vert']:
                for item in track_usage['vert'][idx]:
                    if item[0] <= start_bot <= item[1] or item[0] <= stop_top <= item[1] or (start_bot <= item[0] and stop_top >= item[1]):
                        naive_place = False
                if naive_place:
                    new_left = idx*2*track_spacing + design_area[0]
                    new_right = new_left + track_spacing
                    stitch_left = min(new_left, start_left)
                    stitch_right = max(new_right, start_right)
                    if not increment_right and len(prev_poly) > 0 and prev_dir == 'RIGHT':
                        prev_poly[-1][2] = new_right # adjust the last track, horizontal, to match the right of the new right
                    elif increment_right and len(prev_poly) > 0 and prev_dir == 'LEFT':
                        prev_poly[-1][0] = new_left # adjust the last track, horizontal, to match the right of the new left
                    if (increment_right and prev_dir == 'RIGHT') or (not increment_right and prev_dir == 'LEFT'): # when to stitch vertical track back to horz
                        prev_poly.append([stitch_left, start_bot, stitch_right, start_top, metal_layers[0]])
                    prev_poly.append([stitch_left, stop_bot, stitch_right, stop_top, metal_layers[0]])  # stitch vertical track to island
                    prev_poly.append([new_left, start_bot, new_right, stop_top, metal_layers[1]])
                    track_usage['vert'][idx].append((start_bot, stop_top))
                    return
            else:
                new_left = idx*2*track_spacing + design_area[0]
                new_right = new_left + track_spacing
                stitch_left = min(new_left, start_left)
                stitch_right = max(new_right, start_right)
                if not increment_right and len(prev_poly) > 0 and prev_dir == 'RIGHT':
                    prev_poly[-1][2] = new_right # adjust the last track, horizontal, to match the right of the new right
                elif increment_right and len(prev_poly) > 0 and prev_dir == 'LEFT':
                    prev_poly[-1][0] = new_left # adjust the last track, horizontal, to match the right of the new left
                if (increment_right and prev_dir == 'RIGHT') or (not increment_right and prev_dir == 'LEFT'): # when to stitch vertical track back to horz
                    prev_poly.append([stitch_left, start_bot, stitch_right, start_top, metal_layers[0]])
                prev_poly.append([stitch_left, stop_bot, stitch_right, stop_top, metal_layers[0]])
                prev_poly.append([new_left, start_bot, new_right, stop_top, metal_layers[1]])
                track_usage['vert'][idx] = [(start_bot, stop_top)]
                return
    
    elif routing_dir == 'BOT':
        increment_right = False
        if prev_dir:
            # find the closest island, and calculate preferred track increment from its sides
            closest_blob_idx, closest_blob_val = None, None
            for blob_idx, blob in enumerate(obstacles):
                dist_to_blob = min( min( abs(start_left - blob[0]), abs(start_left - blob[2]) ) ,  min( abs(start_right - blob[0]), abs(start_right - blob[2]) ) ) 
                if closest_blob_idx:
                    closest_blob_idx = blob_idx if dist_to_blob < closest_blob_val else closest_blob_idx
                    closest_blob_val = dist_to_blob if dist_to_blob < closest_blob_val else closest_blob_val
                else:
                    closest_blob_idx = blob_idx
                    closest_blob_val = dist_to_blob
            closest_blob = obstacles[closest_blob_idx]
            increment_right = abs(closest_blob[2] - start_left) < abs(closest_blob[0] - start_left)
        elif prev_dir is None:
            # choose increment direction based on start's proximity to either left or right of the design (ie which side of the frame are we on)
            pass
        
        if increment_right:
            rng_start = start_left_idx
            rng_stop = horz_max_idx
            rng_count = 1
        else:
            rng_start = start_left_idx
            rng_stop = 1 + track_idx_margin
            rng_count = -1
        for idx in range(rng_start, rng_stop, rng_count):
            naive_place = True
            if idx in track_usage['vert']:
                for item in track_usage['vert'][idx]:
                    if item[0] <= stop_bot <= item[1] or item[0] <= start_top <= item[1] or (stop_bot <= item[0] and start_top >= item[1]):
                        naive_place = False
                if naive_place:
                    new_left = idx*2*track_spacing + design_area[0]
                    new_right = new_left + track_spacing
                    stitch_left = min(new_left, start_left)
                    stitch_right = max(new_right, start_right)
                    if not increment_right and len(prev_poly) > 0 and prev_dir == 'RIGHT':
                        prev_poly[-1][2] = new_right # adjust the last track, horizontal, to match the right of the new right
                    elif increment_right and len(prev_poly) > 0 and prev_dir == 'LEFT':
                        prev_poly[-1][0] = new_left # adjust the last track, horizontal, to match the right of the new left
                    if (increment_right and prev_dir == 'RIGHT') or (not increment_right and prev_dir == 'LEFT'): # when to stitch vertical track back to horz
                        prev_poly.append([stitch_left, start_bot, stitch_right, start_top, metal_layers[0]])
                    prev_poly.append([stitch_left, stop_bot, stitch_right, stop_top, metal_layers[0]])  # stitch vertical track to island
                    prev_poly.append([new_left, stop_bot, new_right, start_top, metal_layers[1]])
                    track_usage['vert'][idx].append((stop_bot, start_top))
                    return
            else:
                new_left = idx*2*track_spacing + design_area[0]
                new_right = new_left + track_spacing
                stitch_left = min(new_left, start_left)
                stitch_right = max(new_right, start_right)
                if not increment_right and len(prev_poly) > 0 and prev_dir == 'RIGHT':
                    prev_poly[-1][2] = new_right # adjust the last track, horizontal, to match the right of the new right
                elif increment_right and len(prev_poly) > 0 and prev_dir == 'LEFT':
                    prev_poly[-1][0] = new_left # adjust the last track, horizontal, to match the right of the new left
                if (increment_right and prev_dir == 'RIGHT') or (not increment_right and prev_dir == 'LEFT'): # when to stitch vertical track back to horz
                    prev_poly.append([stitch_left, start_bot, stitch_right, start_top, metal_layers[0]])
                prev_poly.append([stitch_left, stop_bot, stitch_right, stop_top, metal_layers[0]])  # stitch vertical track to island
                prev_poly.append([new_left, stop_bot, new_right, start_top, metal_layers[1]])
                track_usage['vert'][idx] = [(stop_bot, start_top)]
                return
    
    elif routing_dir == 'LEFT':
        if abs(start_bot - design_area[1]) <= abs(start_bot - design_area[3]):
            rng_start = start_bot_idx
            rng_stop = vert_max_idx
            rng_count = 1
        else:
            rng_start = start_bot_idx
            rng_stop = 1 + track_idx_margin
            rng_count = -1
        
        for idx in range(rng_start, rng_stop, rng_count):
            naive_place = True
            if idx in track_usage['horz']:
                for item in track_usage['horz'][idx]:
                    if item[0] <= start_left <= item[1] or item[0] <= stop_right <= item[1] or (start_left <= item[0] and stop_right >= item[1]):
                        naive_place = False
                        break
                if naive_place:
                    new_bot = idx*2*track_spacing + design_area[1]
                    new_top = new_bot + track_spacing
                    # these connect the start polygon to the further placed track
                    stitch_bot = min(new_bot, start_bot)
                    stitch_top = max(new_top, start_top)
                    stitch_right = max(start_left + track_spacing, start_right)
                    prev_poly.append([start_left, stitch_bot, stitch_right, stitch_top, metal_layers[1]])
                    prev_poly.append([stop_left, new_bot, start_right, new_top, metal_layers[0]])
                    track_usage['horz'][idx].append((stop_left, start_right))
                    return
            else:
                new_bot = idx*2*track_spacing + design_area[1]
                new_top = new_bot + track_spacing
                # these connect the start polygon to the further placed track
                stitch_bot = min(new_bot, start_bot)
                stitch_top = max(new_top, start_top)
                stitch_right = max(start_left + track_spacing, start_right)
                prev_poly.append([start_left, stitch_bot, stitch_right, stitch_top, metal_layers[1]])
                prev_poly.append([stop_left, new_bot, start_right, new_top, metal_layers[0]])
                track_usage['horz'][idx] = [(stop_left, start_right)]
                return
    
    elif routing_dir == 'RIGHT':
        if abs(start_bot - design_area[1]) <= abs(start_bot - design_area[3]):
            rng_start = start_bot_idx
            rng_stop = vert_max_idx
            rng_count = 1
        else:
            rng_start = start_bot_idx
            rng_stop = 1
            rng_count = -1
        
        for idx in range(rng_start, rng_stop, rng_count):
            naive_place = True
            if idx in track_usage['horz']:
                for item in track_usage['horz'][idx]:
                    if (item[0] <= start_left <= item[1] or item[0] <= stop_right <= item[1]) or (start_left <= item[0] and stop_right >= item[1]):
                        naive_place = False
                        break
                if naive_place:
                    new_bot = idx*2*track_spacing + design_area[1]
                    new_top = new_bot + track_spacing
                    # these connect the start polygon to the further placed track
                    stitch_bot = min(new_bot, start_bot)
                    stitch_top = max(new_top, start_top)
                    stitch_right = max(start_left + track_spacing, start_right)
                    prev_poly.append([start_left, stitch_bot, stitch_right, stitch_top, metal_layers[1]])
                    prev_poly.append([start_left, new_bot, stop_right, new_top, metal_layers[0]])
                    track_usage['horz'][idx].append((start_left, stop_right))
                    return
            else:
                new_bot = idx*2*track_spacing + design_area[1]
                new_top = new_bot + track_spacing
                # these connect the start polygon to the further placed track
                stitch_bot = min(new_bot, start_bot)
                stitch_top = max(new_top, start_top)
                stitch_right = max(start_left + track_spacing, start_right)
                prev_poly.append([start_left, stitch_bot, stitch_right, stitch_top, metal_layers[1]])
                prev_poly.append([start_left, new_bot, stop_right, new_top, metal_layers[0]])
                track_usage['horz'][idx] = [(start_left, stop_right)]
                return
    