import os
import pprint
from ashes_fg.class_lib_ext import *
from collections import OrderedDict
verbose = False

def asic_compiler(func, filename):
    # create directory to place verilog files
    if filename == None:
        filename = func.__name__
    file_path = os.path.join('.', filename, 'verilog_files')
    if not os.path.exists(file_path): os.makedirs(file_path)
    file_path = os.path.join(file_path, filename + '.v')
    
    modules = func()

    # Separate objects into their respective islands
    islands = OrderedDict()
    for item in modules:
        if item.island not in islands:
            islands[item.island] = [item]
        else:
            islands[item.island].append(item)
    if verbose: pprint.pprint(islands)

    # Track nets between islands
    # key: cell_name, value: [(pinname, netname)]
    # TODO: handle nets with 3+ pins, verilog to gds already handles it
    nets = {} 
    net_num = 0
    for item in modules:
        # check if any nets connect to a separate island
        for key, attr in item.__dict__.items():
            if isinstance(attr, std_cell) and attr not in islands[item.island]:
                # Place first object on the net into dictionary
                if item not in nets:
                    nets[item] = [(key, 'c_net'+str(net_num))]
                else:
                    nets[item].append((key, 'c_net'+str(net_num)))
                # Place second object on the net into dictionary
                output = get_attr_output(attr)
                if attr not in nets:
                    nets[attr] = [(output[0], 'c_net'+str(net_num))]
                else:
                    nets[attr].append((output[0], 'c_net'+str(net_num)))
                net_num += 1
            # handle cells with a vector of inputs that could also be from a separate island
            # TODO: optimize this logic
            elif isinstance(attr, list):
                #print('vector input inter island handling')
                #print(attr)
                in_pins = get_attr_input(item)
                out_pins_offset = 0
                for elem in attr:
                    if elem[0] not in islands[item.island]:
                        num_wires = elem[0].num_outputs
                        wires_per_input = int(num_wires/len(in_pins))
                        # For each input on the item with vector inputs, generate the nets (ie vmm cell has two gates, each one needs half the vector inputs)
                        for pin in in_pins:
                            # Place first object on the net into dictionary
                            if item not in nets:
                                nets[item] = [(pin, f'c_net{net_num}[0:{str(wires_per_input)}]')]
                            else:
                                nets[item].append((pin, f'c_net{net_num}[0:{str(wires_per_input)}]'))
                            # next for the items that the vector inputs originate, connect the other end of the net
                            out_pins = get_attr_output(elem[0])
                            out_start = int(out_pins_offset)
                            out_end = int(out_start + wires_per_input)
                            out_cnt = 0
                            for pin in out_pins[out_start:out_end]:
                                if elem[0] not in nets:
                                    nets[elem[0]] = [(pin, f'c_net{net_num}[{out_cnt}]')]
                                else:
                                    nets[elem[0]].append((pin, f'c_net{net_num}[{out_cnt}]'))
                                out_cnt +=1
                            net_num+=1
                            out_pins_offset = out_end       
    if verbose: pprint.pprint(nets)
    # Write output verilog
    # TODO: build verilog file in a more generalized way. Eg checking nets, matrix vs single cell instances should slowly append to an array for each cell
    ver_file = open(file_path, 'w')
    ver_file.write('module TOP(port1);\n')
    # For each cell in the islands, look up the net in table. if none, write out verilog. if yes, add them to verilog
    island_num = 0
    inst_num = 0
    for isle, arr in islands.items():
        if isle == func.__name__:
            row, col = 1, 1
            for cell in arr:
                cell_name = cell.cell_name
                net_str = []
                if cell in nets:
                    cell_nets = nets[cell]
                    for item in cell_nets:
                        net_str.append(f'.{item[0]}({item[1]}), ')
                net_str = ''.join(net_str)
                if not net_str: 
                    ver_file.writelines(f'\t{cell_name} I__{inst_num} (.island_num({island_num}), .row({row}), .col({col}));\n')
                else:
                    net_str = net_str[:-2]
                    ver_file.writelines(f'\t{cell_name} I__{inst_num} (.island_num({island_num}), .row({row}), .col({col}), {net_str});\n')
                island_num += 1
                inst_num += 1
        else:
            row, col = 1, 1
            for cell in arr:
                cell_name = cell.cell_name
                net_str = []
                if cell in nets:
                    cell_nets = nets[cell]
                    for item in cell_nets:
                        net_str.append(f'.{item[0]}({item[1]}), ')
                net_str = ''.join(net_str)
                vectorized_str = ''
                if 'matrix_row' in cell.__dict__:
                    vectorized_str += f', .matrix_row({cell.matrix_row}), .matrix_col({cell.matrix_column})'
                if not net_str:
                    ver_file.writelines(f'\t{cell_name} I__{inst_num} (.island_num({island_num}), .row({row}), .col({col}));\n')
                else:
                    net_str = net_str[:-2]
                    ver_file.writelines(f'\t{cell_name} I__{inst_num} (.island_num({island_num}), .row({row}), .col({col}){vectorized_str}, {net_str});\n')
                col += 1
                inst_num +=1
            island_num +=1
    
    ver_file.writelines('\nendmodule')
    ver_file.close()

    
def get_attr_output(obj):
    ret_val = []
    for key, elem in obj.__dict__.items():
        if isinstance(elem, str) and 'output' in elem:
            ret_val.append(key)
    return ret_val

def get_attr_input(obj):
    ret_val = []
    for key, elem in obj.__dict__.items():
        if isinstance(elem, str) and 'input' in elem:
            ret_val.append(key)
    return ret_val

'''
    fh = open(file_path, 'w')
    fh.write('module TOP(port1);\n')
    
    modules = func()
    net_table = {}
    net_num, inst_num = 0, 0
    frame_module = None
    for module in modules:
        if not issubclass(type(module), frame):
            fh.write(f'\t{module.__class__.__name__} I__{inst_num} (.island_num({inst_num}), .row(1), .col(1)')
            for key, val in enumerate(module.__dict__):
                if type(module.__dict__[val]) == iopad:
                    net_table[f'a_net{net_num}'] = module.__dict__[val].pad_num
                    fh.write(f', .{val}(a_net{net_num})')
                    net_num += 1
            fh.write(');\n')
            inst_num += 1
        else:
            frame_module = module
    if frame_module:
        fh.write(f'\n\t{frame_module.__class__.__name__} FRAME (')
        first_elem = True
        for net_name, pad_num in net_table.items():
            if not first_elem: 
                fh.write(', ')
            first_elem = False
            fh.write(f'.{pad_num}({net_name})')
        fh.write(');\n')
    fh.write('endmodule')
    fh.close()
    '''