# -*- coding: utf-8 -*-
"""
@author: lyang

TODO: 1. block location (ask Aishwarya)---not needed
      2. special cases - currently only handling first argument as block number
      3. refine code/debug - no longer need list, point or minus
"""

################# pre processing file into compatible format ###############
import os
import math
import sys


def v2blif(verilog_data, out_path):
    '''
    Generates a .blif netlist file from input verilog string. File is placed at <out_path>
    '''
    filedata = verilog_data

    newdata = filedata.replace('.','point')
    newdata = newdata.replace('D-','e-')
    newdata = newdata.replace('-','minus')
    newdata = newdata.replace('= [','= listx')
    newdata = newdata.replace('=[','= listx')
    newdata = newdata.replace(',','x')
    newdata = newdata.replace('listx\'','listx')
    newdata = newdata.replace('\'x \'','x')
    newdata = newdata.replace('\'','')
    newdata = newdata.replace('];',';')
    newdata = newdata.replace('()','(none)')
    newdata = newdata.replace('= 0','= _0')
    newdata = newdata.replace('= 1','= _1')
    newdata = newdata.replace('= 2','= _2')
    newdata = newdata.replace('= 3','= _3')
    newdata = newdata.replace('= 4','= _4')
    newdata = newdata.replace('= 5','= _5')
    newdata = newdata.replace('= 6','= _6')
    newdata = newdata.replace('= 7','= _7')
    newdata = newdata.replace('= 8','= _8')
    newdata = newdata.replace('= 9','= _9')
    newdata = newdata.replace('=0','= _0')
    newdata = newdata.replace('=1','= _1')
    newdata = newdata.replace('=2','= _2')
    newdata = newdata.replace('=3','= _3')
    newdata = newdata.replace('=4','= _4')
    newdata = newdata.replace('=5','= _5')
    newdata = newdata.replace('=6','= _6')
    newdata = newdata.replace('=7','= _7')
    newdata = newdata.replace('=8','= _8')
    newdata = newdata.replace('=9','= _9')

    path = os.path.join(out_path, 'test_token_out.v')
    outfile = open(path,'w')
    #+++++++++++++++++++++++outfile = open('test_token_out.v','w')
    outfile.write(newdata)
    outfile.close()

    ###################### parsing verilog starts here ################
    from verilog_parser.parser import parse_verilog

    path = os.path.join(out_path, 'test_token_out.v')
    modules = parse_verilog(open(path).read()).modules
    #+++++++++++++++++++++++++++modules = parse_verilog(open('test_token_out.v').read()).modules
    path = os.path.join(out_path, str(modules[0].module_name)+'.blif')
    f = open(path,'w')
    #++++++++++++++++++++++++++++f = open(modules[0].module_name+'.blif','w')
    f.write('.model '+modules[0].module_name+'\n')
    input_list = []
    output_list = []
    in_pad = []
    out_pad = []

    for i in range(1,len(modules)):
        if 'pad_in' in modules[i].module_name:
            in_pad.append(' '.join(modules[i].assignments[0].assignments[0][1].split('x')[1:]))
            for j in modules[i].output_declarations:
                if j.range == None:
                    input_list.append(j.net_name+'_1')
                else:
                    for k in range(int(j.range.start)+1):
                        input_list.append(j.net_name+'_'+str(k+1))
                        
        elif 'pad_out' in modules[i].module_name:
            out_pad.append(' '.join(modules[i].assignments[0].assignments[0][1].split('x')[1:]))
            for j in modules[i].input_declarations:
                if j.range == None:
                    output_list.append(j.net_name+'_1')
                else:
                    for k in range(int(j.range.start)+1):
                        output_list.append(j.net_name+'_'+str(k+1))
        #GENARB_f io handling
        elif 'GENARB_f' in modules[i].module_name:
            for j in modules[i].output_declarations:
                if j.range == None:
                    input_list.append(j.net_name+'_1')
                else:
                    for k in range(int(j.range.start)+1):
                        input_list.append(j.net_name+'_'+str(k+1))
        #meas_volt io halding  
        elif 'meas_volt' in modules[i].module_name:
            output_list.append('out_mite_adc_1')
        #dc and gpio input handling
        elif 'dc_in' in modules[i].module_name:
            if 'vcc' not in input_list:
                input_list.append('vcc')
        elif 'gpio' in modules[i].module_name:
            for j in modules[i].output_declarations:
                if j.range == None:
                    input_list.append(j.net_name+'_1')
                else:
                    for k in range(int(j.range.start)+1):
                        input_list.append(j.net_name+'_'+str(k+1))
                        
    for i in range(1,len(modules)):
        for j in modules[i].input_declarations:
            if j.net_name == 'vcc':
                if 'vcc' not in input_list:
                    input_list.append('vcc')
            elif j.net_name == 'gnd':
                if 'gnd' not in input_list:
                    input_list.append('gnd')
                        
    f.write('.inputs '+' '.join(input_list)+'\n')
    f.write('.outputs '+' '.join(output_list)+'\n')
    if in_pad == []:
        f.write('# pad_in\n')
    else:
        f.write('# '+' '.join(in_pad)+' pad_in\n')
    if out_pad == []:
        f.write('# pad_out\n')
    else:
        f.write('# '+' '.join(out_pad)+' pad_out\n')
    f.write('\n')

    block_num = 1
            
    for i in range(1,len(modules)):
        if 'pad_in' not in modules[i].module_name and 'pad_out' not in modules[i].module_name:
            #io block needs special param handling
            if 'dc_in' in modules[i].module_name:
                param_assignment = []
            elif 'GENARB_f' in modules[i].module_name:
                param_assignment = []
            elif 'meas_volt' in modules[i].module_name:
                param_assignment = []
            elif 'sr_1i_16o' in modules[i].module_name:
                param_assignment = []
            else:
                block_num = modules[i].assignments[0].assignments[0][1].split('_')[1]
                param_assignment = modules[i].assignments[1:]
            param_out = []
            for j in param_assignment:
                if 'listx' in j.assignments[0][1]:
                    temp = j.assignments[0][1].split('x')[1:]
                    for k in range(len(temp)):
                        if 'point' in temp[k] and 'minus' in temp[k]:
                            temp2 = temp[k].split('point')
                            temp3 = temp2[1].split('minus')
                            temp[k] = str(temp2[0])+'.'+str(temp3[0])+'-'+str(temp3[1])
                        elif 'point' in temp[k]:
                            temp2 = temp[k].split('point')
                            temp[k] = str(temp2[0]+'.'+str(temp2[1]))
                        elif 'minus' in temp[k]:
                            temp2 = temp[k].split('minus')
                            temp[k] = str(temp2[0])+'-'+str(temp2[1])
                    param_out.append(j.assignments[0][0]+' ='+','.join(temp))
                else:
                    if 'point' in j.assignments[0][1] and 'minus' in j.assignments[0][1]:
                        temp = j.assignments[0][1].split('_')[1].split('point')
                        temp2 = temp[1].split('minus')
                        param_out.append(j.assignments[0][0]+' ='+str(temp[0])+'.'+str(temp2[0])+'-'+str(temp2[1]))
                    elif 'point' in j.assignments[0][1]:
                        temp = j.assignments[0][1].split('_')[1].split('point')
                        param_out.append(j.assignments[0][0]+' ='+str(temp[0]+'.'+str(temp[1])))
                    elif 'minus' in j.assignments[0][1]:
                        temp = j.assignments[0][1].split('_')[1].split('minus')
                        param_out.append(j.assignments[0][0]+' ='+str(temp[0])+'-'+str(temp[1]))
                    else:
                        temp = j.assignments[0][1].split('_')[1]
                        param_out.append(j.assignments[0][0]+' ='+temp)
                    
            input_num = len(modules[i].input_declarations)
            output_num = len(modules[i].output_declarations)
            for j in range(1,int(block_num)+1):
                #dc_in param handling
                if modules[i].module_name == 'dc_in':
                    f.write('# dc_in\n')
                    f.write('.subckt fgota in[0]=vcc in[1]='+modules[i].output_declarations[0].net_name+'_'+str(j))
                    f.write(' out[0]='+modules[i].output_declarations[0].net_name+'_'+str(j))
                    if 'point' in modules[i].assignments[0].assignments[0][1]:
                        temp = modules[i].assignments[0].assignments[0][1]
                        temp2 = temp.split('_')[1].split('point')
                        volt = float(temp2[0]+'.'+temp2[1])
                    else:
                        temp = modules[i].assignments[0].assignments[0][1]
                        volt = float(temp.split('_')[1])
                    n_bias_ln = 1.658236340989905*volt-16.781129443839024
                    n_bias = round(math.exp(n_bias_ln),10)
                    f.write(' #fgota_bias =2e-06&fgota_p_bias =2e-06&fgota_n_bias ='+str(n_bias))
                    ## MODIFIED
                    f.write('&fgota_small_cap =0') ## remove double line break after =0
                    f.write('&fix_loc_enabled =' + str(modules[i].assignments[1].assignments[0][1][1:]))  
                    f.write('&fix_loc_x =' + str(modules[i].assignments[2].assignments[0][1][1:]))
                    f.write('&fix_loc_y =' + str(modules[i].assignments[3].assignments[0][1][1:]))
                    f.write('\n\n') ## double line break after new parameters
                    '''
                    print("Assingments")
                    print('&fix_loc_enabled =' + str(modules[i].assignments[1].assignments[0][1][1:]))
                    '''
                #lpf handling
                elif modules[i].module_name == 'lpfota':
                    f.write('# LPF\n')
                    f.write('.subckt ota in[0]='+modules[i].input_declarations[0].net_name+'_'+str(j))
                    f.write(' in[1]='+modules[i].output_declarations[0].net_name+'_'+str(j))
                    f.write(' out[0]='+modules[i].output_declarations[0].net_name+'_'+str(j))
                    if 'point' in modules[i].assignments[1].assignments[0][1]:
                        temp = modules[i].assignments[1].assignments[0][1]
                        temp2 = temp.split('_')[1].split('point')
                        freq = float(temp2[0]+'.'+temp2[1])
                    else:
                        temp = modules[i].assignments[1].assignments[0][1]
                        freq = float(temp.split('_')[1])
                    ota_bias = round(2*3.14*freq*0.00000000001*2*0.026/0.7,14)
                    f.write(' #ota_bias ='+str(ota_bias))
                    f.write('\n\n')
                #meas_volt handling
                elif modules[i].module_name == 'meas_volt':
                    f.write(' # MITE_ADC\n')
                    f.write('.subckt meas_volt_mite in[0]='+modules[i].input_declarations[0].net_name+'_'+str(j))
                    f.write(' out[0]=out_mite_adc_1 #meas_fg =0.00001\n\n')
                #GENARB and gpio seem to be only a net in blif
                elif modules[i].module_name == 'GENARB_f':
                    pass
                elif modules[i].module_name == 'gpio_in':
                    pass
                #c4 block handling
                elif modules[i].module_name == 'c4_sp':
                    if j == 1:
                        param_out[0] = param_out[0].split(' =')[1]
                        param_out[1] = param_out[1].split(' =')[1]
                        param_out[2] = param_out[2].split(' =')[1]
                        param_out[3] = param_out[3].split(' =')[1]
                        param_out[4] = param_out[4].split(' =')[1]
                        param_out[5] = param_out[5].split(' =')[1]
                        param_out[6] = param_out[6].split(' =')[1]
                    f.write('# C4\n')
                    if modules[i].input_declarations[0].net_name!='gnd' or 'vcc':
                        f.write('.subckt c4_sp in[0]='+modules[i].input_declarations[0].net_name+'_1')
                    else:
                        f.write('.subckt c4_sp in[0]='+modules[i].input_declarations[0].net_name)
                    if modules[i].input_declarations[1].net_name!='gnd' or 'vcc':
                        f.write(' in[1]='+modules[i].input_declarations[1].net_name+'_1')
                    else:
                        f.write(' in[1]='+modules[i].input_declarations[1].net_name)
                    f.write(' out[0]='+modules[i].output_declarations[0].net_name+'_'+str(j))
                    f.write(' #c4_sp_ota_bias[0] ='+param_out[0].split(',')[j-1])
                    f.write('&c4_sp_ota_bias[1] ='+param_out[3].split(',')[j-1])
                    f.write('&c4_sp_fg[0] =0')
                    f.write('&c4_sp_ota_small_cap[0] =0')
                    f.write('&c4_sp_ota_small_cap[1] =0')
                    f.write('&c4_sp_ota_p_bias[0] ='+param_out[2].split(',')[j-1])
                    f.write('&c4_sp_ota_n_bias[0] ='+param_out[1].split(',')[j-1])
                    f.write('&c4_sp_ota_p_bias[1] ='+param_out[5].split(',')[j-1])
                    f.write('&c4_sp_ota_n_bias[1] ='+param_out[4].split(',')[j-1]+'&')
                    if int(param_out[6].split(',')[j-1])==6:
                        f.write('c4_sp_cap_3x[0] =0&c4_sp_cap_2x[0] =0&c4_sp_cap_1x[0] =0')
                    elif int(param_out[6].split(',')[j-1])==5:
                        f.write('c4_sp_cap_3x[0] =0&c4_sp_cap_2x[0] =0')
                    elif int(param_out[6].split(',')[j-1])==4:
                        f.write('c4_sp_cap_3x[0] =0&c4_sp_cap_1x[0] =0')
                    elif int(param_out[6].split(',')[j-1])==3:
                        f.write('c4_sp_cap_3x[0] =0')
                    elif int(param_out[6].split(',')[j-1])==2:
                        f.write('c4_sp_cap_2x[0] =0')
                    elif int(param_out[6].split(',')[j-1])==1:
                        f.write('c4_sp_cap_1x[0] =0')
                    f.write('\n\n')
                #shift reg handling
                elif modules[i].module_name == 'sr_1i_16o':
                    f.write('# Shift register 1input 16outputs\n')
                    f.write('.subckt sftreg3 in[0]='+modules[i].input_declarations[0].net_name+'_'+str(j))
                    f.write(' in[1]='+modules[i].input_declarations[1].net_name+'_'+str(j))
                    f.write(' in[2]='+modules[i].input_declarations[2].net_name+'_'+str(j))
                    f.write(' in[3]='+modules[i].input_declarations[3].net_name+'_'+str(j))
                    f.write(' out[0]=net_floated_1')
                    f.write(' out[1]=net0_1')
                    f.write(' out[2]='+modules[i].output_declarations[0].net_name+'_'+str(j))
                    f.write(' out[3]='+modules[i].output_declarations[1].net_name+'_'+str(j))
                    output_num = int(modules[i].assignments[0].assignments[0][1].split('_')[1])
                    for y in range(1,output_num+1):
                        f.write(' out['+str(y+3)+']='+modules[i].output_declarations[2].net_name+'_'+str(y))
                    f.write(' #sftreg3_fg =0\n\n')
                #vmm12x4 handling
                elif modules[i].module_name == 'vmm_12x4':
                    f.write('#vmm_12x4\n')
                    if modules[i].input_declarations[0].range==None:
                        f.write('.subckt vmm_12x4 in[0]='+modules[i].input_declarations[0].net_name+'_1')
                        f.write(' in[1]='+modules[i].input_declarations[1].net_name+'_1')
                        f.write(' in[2]='+modules[i].input_declarations[2].net_name+'_1')
                        f.write(' in[3]='+modules[i].input_declarations[3].net_name+'_1')
                        f.write(' in[4]='+modules[i].input_declarations[4].net_name+'_1')
                        f.write(' in[5]='+modules[i].input_declarations[5].net_name+'_1')
                        f.write(' in[6]='+modules[i].input_declarations[6].net_name+'_1')
                        f.write(' in[7]='+modules[i].input_declarations[7].net_name+'_1')
                        f.write(' in[8]='+modules[i].input_declarations[8].net_name+'_1')
                        f.write(' in[9]='+modules[i].input_declarations[9].net_name+'_1')
                        f.write(' in[10]='+modules[i].input_declarations[10].net_name+'_1')
                        f.write(' in[11]='+modules[i].input_declarations[11].net_name+'_1')
                        f.write(' out[0]='+modules[i].output_declarations[0].net_name+'_1')
                        f.write(' out[1]='+modules[i].output_declarations[1].net_name+'_1')
                        f.write(' out[2]='+modules[i].output_declarations[2].net_name+'_1')
                        f.write(' out[3]='+modules[i].output_declarations[3].net_name+'_1')
                    else:
                        f.write('.subckt vmm_12x4 in[0]='+modules[i].input_declarations[0].net_name+'_1')
                        f.write(' in[1]='+modules[i].input_declarations[0].net_name+'_2')
                        f.write(' in[2]='+modules[i].input_declarations[0].net_name+'_3')
                        f.write(' in[3]='+modules[i].input_declarations[0].net_name+'_4')
                        f.write(' in[4]='+modules[i].input_declarations[1].net_name+'_1')
                        f.write(' in[5]='+modules[i].input_declarations[1].net_name+'_2')
                        f.write(' in[6]='+modules[i].input_declarations[1].net_name+'_3')
                        f.write(' in[7]='+modules[i].input_declarations[1].net_name+'_4')
                        f.write(' in[8]='+modules[i].input_declarations[2].net_name+'_1')
                        f.write(' in[9]='+modules[i].input_declarations[2].net_name+'_2')
                        f.write(' in[10]='+modules[i].input_declarations[2].net_name+'_3')
                        f.write(' in[11]='+modules[i].input_declarations[2].net_name+'_4')
                        f.write(' out[0]='+modules[i].output_declarations[0].net_name+'_1')
                        f.write(' out[1]='+modules[i].output_declarations[0].net_name+'_2')
                        f.write(' out[2]='+modules[i].output_declarations[0].net_name+'_3')
                        f.write(' out[3]='+modules[i].output_declarations[0].net_name+'_4')
                    f.write(' #vmm_12x4_ls =0')
                    vmm_12x4_param = []
                    for aa in range(1,int(modules[i].module_name.split('_')[1].split('x')[1])+1):
                        for bb in range(1,int(modules[i].module_name.split('_')[1].split('x')[0])+1):
                            f.write('&vmm_12x4_in'+str(aa)+'_'+str(bb)+' ='+param_out[aa].split(' =')[1].split(',')[bb-1])
                    f.write('\n\n')
                #output_floated handling
                elif modules[i].module_name == 'output_f':
                    pass
                #general block
                else:
                    f.write('#'+modules[i].module_name+'\n')
                    f.write('.subckt '+modules[i].module_name)
                    if modules[i].input_declarations!=[]:
                        for k in range(input_num):
                            if modules[i].input_declarations[k].net_name == 'vcc':
                                f.write(' in['+str(k)+']=vcc')
                            elif modules[i].input_declarations[k].net_name == 'gnd':
                                f.write(' in['+str(k)+']=gnd')
                            else:
                                one2mult_flag = False
                                for p in range(1,len(modules)):
                                    for net_num in range(len(modules[p].output_declarations)):
                                        if modules[i].input_declarations[k].net_name == modules[p].output_declarations[net_num].net_name and modules[p].output_declarations[net_num].range==None:
                                            one2mult_flag = True
                                        #else:
                                            #one2mult_flag = False
                                if one2mult_flag:
                                    f.write(' in['+str(k)+']='+modules[i].input_declarations[k].net_name+'_1')
                                else:
                                    f.write(' in['+str(k)+']='+modules[i].input_declarations[k].net_name+'_'+str(j))
                    if modules[i].output_declarations!=[]:
                        for k in range(output_num):
                            f.write(' out['+str(k)+']='+modules[i].output_declarations[k].net_name+'_'+str(j))
                    if param_out != []:
                        f.write(' #')
                        for param in param_out:
                            if ',' in param:
                                param_name = param.split(' =')[0]
                                param_value = param.split(' =')[1].split(',')[j-1]
                                f.write(param_name+' ='+param_value+'&')
                            else:
                                param_name = param.split(' =')[0]
                                param_value = param.split(' =')[1]
                                f.write(param_name+' ='+param_value+'&')
                    f.write('\n')
                    f.write('\n')
    f.write('.end')
    f.write('\n')
    #f.write('\n#blif generated from new flow\n')

    f.close()
    path = os.path.join(out_path, str(modules[0].module_name)+'.blif')
    with open(path) as trim:
        new_list = []
        for line in trim:
            if '&\n' in line:      
                new_list.append(line.replace('&\n','\n'))
            elif 'gnd_1' in line:
                new_list.append(line.replace('gnd_1','gnd'))
            elif 'vcc_1' in line:
                new_list.append(line.replace('vcc_1','vcc'))
            else:
                new_list.append(line)

    f = open(path,'w')
    for item in new_list:
        f.write(item)
    f.close()


    path = os.path.join(out_path, 'test_token_out.v')
    os.remove(path)
    #++++++++++++++++++++++++os.remove('test_token_out.v')
