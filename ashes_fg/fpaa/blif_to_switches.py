import os
import sys

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
    
    
    
    os.system('python /home/ubuntu/rasp30/vpr2swcs/genswcs.py -c ' + path +'/'+ fname + ' -d ' + path + brdtype)
