"""
@author: lyang

TO DO:
    1. CUSTOMIZE BLOCKS WITH SPECIAL BUS REPRESENTATION (VMM12x1_wowta AS AN EXAMPLE IN CODE)
       UPDATE: SHOULD CATEGORIZE INSTEAD OF CUSTOMIZING STUFF. NEED TO FIND A PATTERN OF SPECIAL BLOCKS
    2. BUG FIX: CODE DOES NOT WORK WITH JOIN BLOCK IMMEDIATELY FOLLOWED BY SPLIT BLOCK. HAVE NO IDEA HOW TO HANDLE.
       ONE POSSIBLE WAY IS TO RUN SETTING I/O OF SPLIT AND JOIN MULTIPLE TIMES. 
       BEST SOLUTION IS PERHAPS JUST FORBIDDING DOING SUCH THING IN XCOS.
    3. AFTER BUS HANDLING IS COMPLETE, CONSIDER REMOVING THE PARAMETER SUGGESTING BUS SIZE (AKA 1ST PARAMETER IN MOST CASES).
    4. HOW TO MAKE THE CODE MORE FRIENDLY FOR PARSING INTO BLIF?
"""

import xml.etree.ElementTree as ET
import json
import os
import sys

outpath = sys.argv[2]
infile = sys.argv[1]

#+++++++++++++++with open(outpath+'analog_std_cells.json', 'r') as cell_library:
with open('/home/ubuntu/rasp30/sci2blif/analog_std_cells.json', 'r') as cell_library:
    lib = json.load(cell_library)

######################## INPUT XCOS FILE HERE. MAKE SURE XCOS IS IN THE SAME FOLDER AS THIS FILE ################################

tree = ET.parse(infile)
#++++++++++++++++tree = ET.parse('Vect_test2.xcos')
#PARSE XML AS A TREE
root = tree.getroot()
f = open(outpath+root.attrib['title']+'_xcos2interm.va','w')
#++++++++++++++++++++++f = open(root.attrib['title']+'_xcos2interm.va','w')
f.write('module '+root.attrib['title']+'()'+'\n')
f.write('endmodule\n')
f.write('\n')
'''for ele in root.iter('BasicBlock'):
    if ele.attrib['interfaceFunctionName'] == 'pad_in':
        print('input IOpad'+ele[0][1].attrib['value'])
for ele in root.iter('BasicBlock'):
    if ele.attrib['interfaceFunctionName'] == 'pad_out':
        print('output IOpad'+ele[0][1].attrib['value'])
print()'''


#BUILDING AN ARRAY OF ALL NETS
net_array = []
for ele in root.iter('ExplicitLink'):
    net_array.append(ele.attrib['id'])

#ADD THE ID OF SPLIT AND JOIN BLOCKS TO A LIST
split_array = []
for ele in root.iter('SplitBlock'):
    split_array.append(ele.attrib['id'])
for ele in root.iter('BasicBlock'):
    if ele.attrib['interfaceFunctionName'] == 'join':
        split_array.append(ele.attrib['id'])
        
#ARRAY OF NET NUMBER, EACH CORRESPONDS TO AN ITEM IN NET_ARRAY (COULD'VE USED A DICTIONARY, MY BAD). 
#ALSO SET THE I/O OF SPLIT AND JOIN BLOCKS TO THE SAME NET NUMBER
net_num = []
for i in net_array:
    net_num.append(net_array.index(i)+1)

for i in net_array:
    for j in root.iter('ExplicitLink'):
        if j.attrib['id'] == i and j[2].attrib['parent'] in split_array:
            for k in root.iter('ExplicitLink'):
                if k[3].attrib['parent'] == j[2].attrib['parent']:
                    net_num[net_array.index(i)] = net_num[net_array.index(k.attrib['id'])]
                    
              
#PADDING THE NET_NUM TO CONSECUTIVE NUMBERS

final_set = list(range(1,len(set(net_num))+1))
max_net_num=1
for i in net_num:
    if i == max_net_num+1:
        max_net_num = max_net_num+1
    elif i > max_net_num+1:
        new_net = max_net_num+1
        for j in net_num:
            if j == i:
                net_num[net_num.index(j)] = new_net
        max_net_num = max_net_num+1
    else:
        pass

net_num_final = net_num
    
    
         
#CORE FUNCTION. ITERATE EACH BLOCK, ASSIGNING NETS TO THAT BLOCK, PRINTING I/O AND PARAMETERS            
for ele in root.iter('BasicBlock'):
    if ele.attrib['interfaceFunctionName'] != 'join':
        block_id = ele.attrib['id']
        #HANDLING VDD AND GND BLOCKS
        if ele[0][0].attrib['value'] == ' ':
            bus_in = 1
            bus_out = 1
        ######################## ADD BLOCKS WITH SPECIAL BUS CASES USING ELIF STATEMENTS HERE #################################
        ########## UPDATE: JEN BELIEVES THAT WE SHOULD NOT CUSTOMIZE BLOCKS. WE SHOULD CATEGORIZE THEM INSTEAD#################
        #HANDLING VMM BLOCKS
        elif 'vmm' in ele.attrib['interfaceFunctionName']:
            bus_in = len(ele[0][1].attrib['value'].split(','))
            bus_out = 1
        #HANDLING _NV SHIFT REGISTERS
        elif '_nv' in ele.attrib['interfaceFunctionName']:
            bus_in = int(ele[0][0].attrib['value'])
            bus_out = int(ele[0][0].attrib['value'])
        #HANDLING IN2IN BLOCKS
        elif 'in2in_x' in ele.attrib['interfaceFunctionName']:
            bus_in = int(ele[0][0].attrib['value'])
            bus_out = int(ele[0][0].attrib['value']) 
        #HANDLING 1 INPUT SHIFT REGISTERS
        elif '_1o' in ele.attrib['interfaceFunctionName']:
            bus_in = int(ele[0][0].attrib['value'])
            bus_out = 1
        #HANDLING 1 OUTPUT SHIFT REGISTERS
        elif '_1i_' in ele.attrib['interfaceFunctionName']:
            bus_in = 1
            bus_out = int(ele[0][0].attrib['value']) 
        #HANDLING WHEN FIRST ARGUMENT IS A STRING
        elif ele[0][0].attrib['value'].isdigit() == False:
            bus_in = 1
            bus_out = 1
        #C4
        elif 'c4_sp' in ele.attrib['interfaceFunctionName']:
            bus_in = 1
            bus_out = int(ele[0][0].attrib['value']) 
        #NON-SPECIAL CASE (conventional)
        else:
            bus_in = int(ele[0][0].attrib['value'])
            bus_out = int(ele[0][0].attrib['value'])
        f.write('module '+ele.attrib['interfaceFunctionName']+'()'+'\n')
        net_in = []
        net_out = []
        parameters = []
        #IF NET IS SINGLE NET, DO NOT ADD [X:0] IN FRONT. ELSE ADD [X:0] WHERE X IS BUS_NUM-1
        for item in root.iter('ExplicitLink'):
            if item[2].attrib['parent'] == block_id and bus_out == 1:
                net_out.append('net'+str(net_num_final[net_array.index(item.attrib['id'])]))
            elif item[3].attrib['parent'] == block_id and bus_in == 1:
                net_in.append('net'+str(net_num_final[net_array.index(item.attrib['id'])]))
            elif item[2].attrib['parent'] == block_id and bus_out > 1:
                net_out.append('['+str(bus_out-1)+':0]net'+str(net_num_final[net_array.index(item.attrib['id'])]))
            elif item[3].attrib['parent'] == block_id and bus_in > 1:
                net_in.append('['+str(bus_in-1)+':0]net'+str(net_num_final[net_array.index(item.attrib['id'])]))
        #WRITE TO FILE. OUTPUT FILE HAS EXTENSION 'va' AND SHOULD BE IN THE SAME FOLDER AS THIS FILE
        f.write('input '+' '.join(net_in)+'\n')
        f.write('output '+' '.join(net_out)+'\n')
        for i in range (0, int(ele[0].attrib['height'])):
            parameters.append(ele[0][i].attrib['value'])
        f.write('parameters ')
        for i in parameters:
            f.write(i+' ')
        f.write('\n')
        #f.write('parameters '+str(parameters)+'\n')
        f.write('endmodule\n')
        f.write('\n')
    
f.close()

with open (outpath+root.attrib['title']+'_xcos2interm.va','r') as interm:
#+++++++++++++++++++++with open (root.attrib['title']+'_xcos2interm.va','r') as interm:
    lines = interm.readlines()
    lines = [line.rstrip() for line in lines]
interm.close()


f = open(outpath+root.attrib['title']+'.v','w')
#+++++++++++++++++++++++f = open(root.attrib['title']+'.v','w')


vcc_line = []
gnd_line = []

for i in range(len(lines)):
    if 'vdd_i' in lines[i]:
        vcc_line.append(lines[i+2].split(' ')[1])
for i in range(len(lines)):
    if 'gnd_i' in lines[i]:
        gnd_line.append(lines[i+2].split(' ')[1])        

for i in vcc_line:
    lines = [w.replace(i,'vcc') for w in lines]
for i in gnd_line:
    lines = [w.replace(i,'gnd') for w in lines]
   
remove_list = []
for i in range(len(lines)):
    if 'vdd_i' in lines[i]:
        remove_list.append(i)
        remove_list.append(i+2)
        remove_list.append(i+3)
        remove_list.append(i+4)
    elif 'gnd_i' in lines[i]:
        remove_list.append(i)
        remove_list.append(i+2)
        remove_list.append(i+3)
        remove_list.append(i+4)
    elif lines[i] == 'input':
        remove_list.append(i)
    elif lines[i] == 'output':
        remove_list.append(i)
            
remove_list.sort(reverse=True)

for i in remove_list:
    lines.pop(i)
    

i = 0
while i<len(lines):
    if 'pad_in' in lines[i]:
        temp = lines[i+2].split(' ')
        lines[i+2] = 'assign pad_num = ['+temp[2]+']'
    elif 'pad_out' in lines[i]:
        temp = lines[i+2].split(' ')
        lines[i+2] = 'assign pad_num = ['+temp[2]+']'
    #io block handling
    elif 'dc_in' in lines[i]:
        temp = lines[i+2].split(' ')
        lines[i+2] = 'assign DC_value = '+temp[2]
    elif 'GENARB_f' in lines[i]:
        lines[i+2] = 'assign block_num = 1'
    elif 'meas_volt' in lines[i]:
        lines[i+2] = 'assign block_num = 1'
    elif 'gpio_in' in lines[i]:
        lines[i+2] = 'assign block_num = 1'
    elif 'sr_1i_16o' in lines[i]:
        pass
    elif 'output_f' in lines[i]:
        temp = lines[i+2].split(' ')
        lines[i+2] = 'assign block_num = '+temp[1]
    else:
        for block in lib:
            if 'module '+block+'()' in lines[i]:
                #vmm12x1 param handling
                if block == 'vmm12x1_wowta':
                    block_num = '1'
                    param_value = lines[i+3].split(' ')[2:]
                    param_value.insert(0,'0')
                #vmm12x4 param handling
                if block == 'vmm_12x4':
                    block_num = '1'
                    param1 = lines[i+3].split(' ')[3:15]
                    param2 = lines[i+3].split(' ')[15:27]
                    param3 = lines[i+3].split(' ')[27:39]
                    param4 = lines[i+3].split(' ')[39:51]
                    param_value = []
                    param_value.append(param1)
                    param_value.append(param2)
                    param_value.append(param3)
                    param_value.append(param4)
                    
                #ota_buf param handling
                elif block == 'ota_buf':
                    block_num = lines[i+3].split(' ')[1]
                    param_value = ['0.00001','[0;0;0]']
                #delay_block
                elif block == 'delay_block':
                    block_num = lines[i+3].split(' ')[1]
                    param_value = lines[i+3].split(' ')[3:]
                #nmirror
                elif block == 'nmirror_w_bias':
                    block_num = lines[i+3].split(' ')[1]
                    param_value = lines[i+3].split(' ')[3:]
                #ota
                elif block == 'ota':
                    block_num = lines[i+3].split(' ')[1]
                    param_value = lines[i+3].split(' ')[3:]
                else:
                    block_num = lines[i+3].split(' ')[1]
                    param_value = lines[i+3].split(' ')[2:]
                lines[i+3] = 'assign block_num = '+block_num
                k = 0
                for key,value in lib[block].items():
                    if '_ls' in key and 'type' not in key and 'board' not in key and 'foundry' not in key and 'process_node' not in key and param_value[0]!='0':
                        lines.insert(i+4, 'assign '+str(key)+' = '+str(value))
                        k = k+1
                        param_value.insert(0,'0')
                    elif '_ls' in key and 'type' not in key and 'board' not in key and 'foundry' not in key and 'process_node' not in key and param_value[0]=='0':
                        lines.insert(i+4, 'assign '+str(key)+' = '+str(value))
                        k = k+1
                    elif 'type' not in key and 'board' not in key and 'foundry' not in key and 'process_node' not in key:
                        lines.insert(i+4+k, 'assign '+str(key)+' = '+ str(param_value[k]))
                        k = k+1
    i = i+1
        

for i in range(len(lines)):
    if 'input' in lines[i] and len(lines[i].split(' '))>2:
        temp = lines[i].split(' ')
        first_in = temp[0:2]
        lines[i] = ' '.join(first_in)
        for j in range(2,len(temp)):
            lines.insert(i+1,'input '+temp[j])
            i = i+1
            
for i in range(len(lines)):
    if 'output' in lines[i] and len(lines[i].split(' '))>2:
        temp = lines[i].split(' ')
        first_out = temp[0:2]
        lines[i] = ' '.join(first_out)
        for j in range(2,len(temp)):
            lines.insert(i+1,'output '+temp[j])
            i = i+1

final_out = []


#lines = [w.replace(':0]',':0] ') for w in lines]
    
i = 0
while i<len(lines):
    #shift reg handling
    if 'sr_1i_16o' in lines[i]:
        strip_1 = lines[i+5].split(' ')
        lines[i+5] = strip_1[0]+' '+strip_1[2]
        strip_2 = lines[i+6].split(' ')
        lines[i+6] = strip_2[0]+' '+strip_2[2]
        output_num = lines[i+8].split(' ')[1] 
        lines[i+8] = 'assign output_num = '+output_num
    elif 'input' in lines[i] and len(lines[i].split(' '))>2:
        split_input = lines[i].split(' ')
        lines[i] = 'input '+split_input[1]
        for j in range(2,len(split_input)):
            lines.insert(i+j-1, 'input '+str(split_input[j]))
    i+=1
    
    
#for alice only
if root.attrib['title'] == 'alice':
    for i in range(len(lines)):
        if 'delay_block()' in lines[i]:
            temp1 = lines[i+1]
            temp2 = lines[i+2]
            lines[i+1] = temp2
            lines[i+2] = temp1
            temp3 = lines[i+3]
            temp4 = lines[i+4]
            lines[i+3] = temp4
            lines[i+4] = temp3
        elif 'wta_new()' in lines[i]:
            temp1 = lines[i+2]
            temp2 = lines[i+3]
            lines[i+2] = temp2
            lines[i+3] = temp1
        
    
lines = [w.replace(':0]',':0] ') for w in lines]

for line in lines:
    if line!='endmodule' and line!='':
        final_out.append(line+';')
    else:
        final_out.append(line)

        
        
        
for i in final_out:
    f.write(i+'\n')

f.close()
os.remove(outpath+root.attrib['title']+'_xcos2interm.va')
#+++++++++++++++++++++++++++os.remove(root.attrib['title']+'_xcos2interm.va')

        





