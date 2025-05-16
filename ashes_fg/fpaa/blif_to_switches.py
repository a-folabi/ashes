import os
import sys
import ashes_fg.fpaa.genswcs as gs

def blif2swcs(sys_name, project_name, board_type, out_path):
    '''
    Generates the switch list from input .blif netlist and pads files
    '''
    if board_type == '3.0a':
        arch = 'rasp3a'
        brdtype = ' -'+arch
    elif board_type == '3.0':
        arch = 'rasp3'
        brdtype = ''
    elif board_type == '3.0n':
        arch = 'rasp3n'
        brdtype = ' -'+arch
    elif board_type == '3.0h':
        arch = 'rasp3h'
        brdtype = ' -'+arch
    fname = project_name
    path = str(out_path)
    
    # Creates a dummy input vector & gpin vector file. These allow normal iopads to pass through
    # But should be updated for arb gen deisgns
    with open(path + "/input_vector", "w") as f:
    	f.write("0x0000 0x0000 0x03e8 0xffff")
    with open(path + "/gpin_vector", "w") as f:
    	f.write("0x0000 0x0000 0x03e8 0xffff")
    gs.main(path + '/' + fname, path, arch, bs_vpr_disp='-route')
