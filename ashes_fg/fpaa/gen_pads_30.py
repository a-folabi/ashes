# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:33:15 2023

@author: lyang
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:33:13 2023

@author: lyang
"""

def gen_pads_30(infile_name, outpath):
    file1 = open(f'{infile_name}.blif','r')
    lines = file1.readlines()

    pads_final = []

    for line in lines:
        if '.inputs ' in line:
            in_nets = line.split('.inputs ')[1].split('\n')[0].split(' ')
            if 'vcc' in in_nets:
                pads_final.append('vcc 7 0 5 #int[5]\n')
                in_nets.remove('vcc')
            elif 'gnd' in in_nets:
                pads_final.append('gnd 7 0 4 #int[4]\n')
                in_nets.remove('gnd')
                
        if '.outputs ' in line:
            out_nets = line.split('.outputs ')[1].split('\n')[0].split(' ')
            
        if ' pad_in\n' in line:
            pads_temp = line.split(' pad_in\n')[0].split('# ')[1].split(' ')
            for i in range(len(pads_temp)):
                if pads_temp[i]=='1':
                    pads_final.append(in_nets[i]+' 9 0 0 #tgate[1]\n')
                elif pads_temp[i]=='2':
                    pads_final.append(in_nets[i]+' 11 0 0 #tgate[1]\n')
                elif pads_temp[i]=='3':
                    pads_final.append(in_nets[i]+' 12 0 0 #tgate[1]\n')
                elif pads_temp[i]=='4':
                    pads_final.append(in_nets[i]+' 12 0 3 #tgate[1]\n')
                elif pads_temp[i]=='5':
                    pads_final.append(in_nets[i]+' 13 0 0 #tgate[1]\n')
                elif pads_temp[i]=='6':
                    pads_final.append(in_nets[i]+' 13 0 3 #tgate[1]\n')                                  
                elif pads_temp[i]=='7':
                    pads_final.append(in_nets[i]+' 14 0 0 #tgate[1]\n')                                  
                elif pads_temp[i]=='8':
                    pads_final.append(in_nets[i]+' 14 0 3 #tgate[1]\n')                                 
                elif pads_temp[i]=='9':
                    pads_final.append(in_nets[i]+' 3 0 0 #tgate[1]\n')
                elif pads_temp[i]=='10':
                    pads_final.append(in_nets[i]+' 3 0 3 #tgate[1]\n')
                elif pads_temp[i]=='11':
                    pads_final.append(in_nets[i]+' 4 0 0 #tgate[1]\n')
                elif pads_temp[i]=='12':
                    pads_final.append(in_nets[i]+' 4 0 3 #tgate[1]\n')
                elif pads_temp[i]=='40':
                    pads_final.append(in_nets[i]+' 13 0 1 #int[1]\n')
                elif pads_temp[i]=='41':
                    pads_final.append(in_nets[i]+' 13 0 2 #int[2]\n')
                elif pads_temp[i]=='42':
                    pads_final.append(in_nets[i]+' 13 0 3 #int[3]\n')
                elif pads_temp[i]=='43':
                    pads_final.append(in_nets[i]+' 13 0 4 #int[4]\n')
                elif pads_temp[i]=='44':
                    pads_final.append(in_nets[i]+' 13 0 5 #int[5]\n')                                  
                elif pads_temp[i]=='45':
                    pads_final.append(in_nets[i]+' 14 0 0 #int[0]\n')                                  
                elif pads_temp[i]=='46':
                    pads_final.append(in_nets[i]+' 14 0 1 #int[1]\n')                                 
                elif pads_temp[i]=='47':
                    pads_final.append(in_nets[i]+' 14 0 2 #int[2]\n')
                elif pads_temp[i]=='48':
                    pads_final.append(in_nets[i]+' 14 0 3 #int[3]\n')
                elif pads_temp[i]=='49':
                    pads_final.append(in_nets[i]+' 14 0 4 #int[4]\n')
                elif pads_temp[i]=='50':
                    pads_final.append(in_nets[i]+' 14 0 5 #int[5]\n')
                elif pads_temp[i]=='51':
                    pads_final.append(in_nets[i]+' 15 1 0 #int[0]\n')                                 
                elif pads_temp[i]=='52':
                    pads_final.append(in_nets[i]+' 15 1 1 #int[1]\n')
                elif pads_temp[i]=='53':
                    pads_final.append(in_nets[i]+' 15 1 2 #int[2]\n')
                elif pads_temp[i]=='54':
                    pads_final.append(in_nets[i]+' 15 1 3 #int[3]\n')
                elif pads_temp[i]=='55':
                    pads_final.append(in_nets[i]+' 15 1 4 #int[4]\n')
                elif pads_temp[i]=='56':
                    pads_final.append(in_nets[i]+' 15 1 5 #int[5]\n')
                elif pads_temp[i]=='57':
                    pads_final.append(in_nets[i]+' 15 2 0 #int[0]\n')
                elif pads_temp[i]=='58':
                    pads_final.append(in_nets[i]+' 15 2 1 #int[1]\n')
                                    
        if ' pad_out\n' in line:
            pads_temp = line.split(' pad_out\n')[0].split('# ')[1].split(' ')
            for i in range(len(pads_temp)):
                if pads_temp[i]=='1':
                    pads_final.append('out:'+out_nets[i]+' 9 0 0 #tgate[1]\n')
                elif pads_temp[i]=='2':
                    pads_final.append('out:'+out_nets[i]+' 11 0 0 #tgate[1]\n')
                elif pads_temp[i]=='3':
                    pads_final.append('out:'+out_nets[i]+' 12 0 0 #tgate[1]\n')
                elif pads_temp[i]=='4':
                    pads_final.append('out:'+out_nets[i]+' 12 0 3 #tgate[1]\n')
                elif pads_temp[i]=='5':
                    pads_final.append('out:'+out_nets[i]+' 13 0 0 #tgate[1]\n')
                elif pads_temp[i]=='6':
                    pads_final.append('out:'+out_nets[i]+' 13 0 3 #tgate[1]\n')                                  
                elif pads_temp[i]=='7':
                    pads_final.append('out:'+out_nets[i]+' 14 0 0 #tgate[1]\n')                                  
                elif pads_temp[i]=='8':
                    pads_final.append('out:'+out_nets[i]+' 14 0 3 #tgate[1]\n')                                 
                elif pads_temp[i]=='9':
                    pads_final.append('out:'+out_nets[i]+' 3 0 0 #tgate[1]\n')
                elif pads_temp[i]=='10':
                    pads_final.append('out:'+out_nets[i]+' 3 0 3 #tgate[1]\n')
                elif pads_temp[i]=='11':
                    pads_final.append('out:'+out_nets[i]+' 4 0 0 #tgate[1]\n')
                elif pads_temp[i]=='12':
                    pads_final.append('out:'+out_nets[i]+' 4 0 3 #tgate[1]\n')
                elif pads_temp[i] == '13':
                    pads_final.append('out:'+out_nets[i]+' 1 0 3 #tgate[1]\n')
                elif pads_temp[i] == '14':
                    pads_final.append('out:'+out_nets[i]+' 2 0 3 #tgate[1]\n')
                elif pads_temp[i] == '15':
                    pads_final.append('out:'+out_nets[i]+' 3 15 0 #ana_buff_out[0]\n')
                elif pads_temp[i] == '16':
                    pads_final.append('out:'+out_nets[i]+' 4 15 0 #ana_buff_out[0]\n')
                elif pads_temp[i] == '17':
                    pads_final.append('out:'+out_nets[i]+' 5 15 0 #ana_buff_out[0]\n')                                  
                elif pads_temp[i]=='40':
                    pads_final.append('out:'+out_nets[i]+' 13 0 1 #int[1]\n')
                elif pads_temp[i]=='41':
                    pads_final.append('out:'+out_nets[i]+' 13 0 2 #int[2]\n')
                elif pads_temp[i]=='42':
                    pads_final.append('out:'+out_nets[i]+' 13 0 3 #int[3]\n')
                elif pads_temp[i]=='43':
                    pads_final.append('out:'+out_nets[i]+' 13 0 4 #int[4]\n')
                elif pads_temp[i]=='44':
                    pads_final.append('out:'+out_nets[i]+' 13 0 5 #int[5]\n')                                  
                elif pads_temp[i]=='45':
                    pads_final.append('out:'+out_nets[i]+' 14 0 0 #int[0]\n')                                  
                elif pads_temp[i]=='46':
                    pads_final.append('out:'+out_nets[i]+' 14 0 1 #int[1]\n')                                 
                elif pads_temp[i]=='47':
                    pads_final.append('out:'+out_nets[i]+' 14 0 2 #int[2]\n')
                elif pads_temp[i]=='48':
                    pads_final.append('out:'+out_nets[i]+' 14 0 3 #int[3]\n')
                elif pads_temp[i]=='49':
                    pads_final.append('out:'+out_nets[i]+' 14 0 4 #int[4]\n')
                elif pads_temp[i]=='50':
                    pads_final.append('out:'+out_nets[i]+' 14 0 5 #int[5]\n')
                elif pads_temp[i]=='51':
                    pads_final.append('out:'+out_nets[i]+' 15 1 0 #int[0]\n')                                 
                elif pads_temp[i]=='52':
                    pads_final.append('out:'+out_nets[i]+' 15 1 1 #int[1]\n')
                elif pads_temp[i]=='53':
                    pads_final.append('out:'+out_nets[i]+' 15 1 2 #int[2]\n')
                elif pads_temp[i]=='54':
                    pads_final.append('out:'+out_nets[i]+' 15 1 3 #int[3]\n')
                elif pads_temp[i]=='55':
                    pads_final.append('out:'+out_nets[i]+' 15 1 4 #int[4]\n')
                elif pads_temp[i]=='56':
                    pads_final.append('out:'+out_nets[i]+' 15 1 5 #int[5]\n')
                elif pads_temp[i]=='57':
                    pads_final.append('out:'+out_nets[i]+' 15 2 0 #int[0]\n')
                elif pads_temp[i]=='58':
                    pads_final.append('out:'+out_nets[i]+' 15 2 1 #int[1]\n')



    f = open(f'{infile_name}.pads','w')

    for i in pads_final:
        f.write(i)

    f.close()














                                  
                                  