from . import fpaa
from . import asic
import json
import os
import sys

def update_class_lib(json_file = 'cells.json', library='class_lib.py'):
    with open(json_file,'r') as f:
        data = json.load(f)
    
    t = open(library, "w")

    # Base ASIC class
    t.write('class std_cell:\n')
    t.write('\tdef __init__(self, input, num_instances, cell_type):\n')
    t.write('\t\tself.input = input\n')
    t.write('\t\tself.num_instances = num_instances\n')
    t.write('\t\tself.cell_type = cell_type\n\n')

    #iopads
    t.write("class inpad:\n")
    t.write("\tdef __init__(self,pad_number):\n")
    t.write("\t\tself.pad_number=pad_number\n")
    t.write("\n")
    t.write("class outpad:\n")
    t.write("\tdef __init__(self,input,pad_number):\n")
    t.write("\t\tself.input=input\n")
    t.write("\t\tself.pad_number=pad_number\n")
    t.write("\n")
    t.write("class outpada:\n")
    t.write("\tdef __init__(self,input,pad_number):\n")
    t.write("\t\tself.input=input\n")
    t.write("\t\tself.pad_number=pad_number\n")
    t.write("\n")

    #general blocks
    for block in data:
        if data[block]['type'] == 'ASIC':
            t.write(f'class {block}(std_cell):\n')
            t.write('\tpass\n\n')
        elif block == 'dc_in':
            t.write("class dc_in:\n")
            t.write("\tdef __init__(self,DC_value):\n")
            t.write("\t\tself.DC_value=DC_value\n")
            t.write("\n")
        elif block == 'gnd':
            t.write("class gnd:\n")
            t.write("\tdef __init__(self):\n")
            t.write("\t\tpass\n")
            t.write("\n")
        elif block == 'vdd':
            t.write("class vdd:\n")
            t.write("\tdef __init__(self):\n")
            t.write("\t\tpass\n")
            t.write("\n")
        elif block == 'GENARB_f':
            t.write("class GENARB_f:\n")
            t.write("\tdef __init__(self,input):\n")
            t.write("\t\tself.input=input\n")
            t.write("\n")
        elif block == 'meas_volt':
            t.write("class meas_volt:\n")
            t.write("\tdef __init__(self,input):\n")
            t.write("\t\tself.input=input\n")
            t.write("\n")
        elif block == 'gpio_in':
            t.write("class gpio_in:\n")
            t.write("\tdef __init__(self):\n")
            t.write("\t\tpass\n")
            t.write("\n")
        elif "?" not in block:
            t.write("class ")
            t.write(block+":\n")
            t.write("\tdef __init__(self,input,num_instances='1'")
            for key,value in data[block].items():
                if type(value) != list:
                    t.write(","+str(key)+"='"+str(value)+"'")
                else:
                    t.write(","+str(key)+"="+str(value))
            t.write("):\n")
            t.write("\t\tself.input=input\n")
            t.write("\t\tself.num_instances=num_instances\n")
            for key,value in data[block].items():
                if "type" not in key and "board" not in key and "foundry" not in key and "process_node" not in key:
                    t.write("\t\tself."+str(key)+"="+str(key)+"\n")
            t.write("\n")
                    
    t.close()