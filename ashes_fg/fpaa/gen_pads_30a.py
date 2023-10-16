# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:33:13 2023

@author: lyang
"""
import os
import sys

infile_name = sys.argv[1]
outpath = sys.argv[2]

file1 = open(infile_name+'.blif','r')
lines = file1.readlines()

file2 = open(infile_name+'.v','r')
lines2 = file2.readlines()

pads_final = []

for i in range(len(lines2)):
    if 'GENARB_f' in lines2[i]:
        dac_in = lines2[i+1].split(' ')[1].split(';')[0]
        pads_final.append('out:out_mite_adc_1 8 1 0 #int[0]\n')
        pads_final.append(dac_in+'_1 0 8 3 #int[3]\n')

for line in lines:
    if '.inputs ' in line:
        in_nets = line.split('.inputs ')[1].split('\n')[0].split(' ')
        for in_net in in_nets:
            if 'vcc' in in_nets:
                pads_final.append('vcc 7 0 5 #int[5]\n')
                in_nets.remove('vcc')
        for in_net in in_nets:
            if 'gnd' in in_nets:
                pads_final.append('gnd 7 0 4 #int[4]\n')
                in_nets.remove('gnd')
            
    if '.outputs ' in line:
        out_nets = line.split('.outputs ')[1].split('\n')[0].split(' ')
        
    if ' pad_in\n' in line and len(line.split(' '))>2:
        pads_temp = line.split(' pad_in\n')[0].split('# ')[1].split(' ')
        for i in range(len(pads_temp)):
            if pads_temp[i]=='1':
                pads_final.append(in_nets[i]+' 8 1 5 #tgate[1]\n')
            elif pads_temp[i]=='2':
                pads_final.append(in_nets[i]+' 8 2 5 #tgate[1]\n')
            elif pads_temp[i]=='3':
                pads_final.append(in_nets[i]+' 8 3 5 #tgate[1]\n')
            elif pads_temp[i]=='4':
                pads_final.append(in_nets[i]+' 8 4 5 #tgate[1]\n')
            elif pads_temp[i]=='5':
                pads_final.append(in_nets[i]+' 8 5 5 #tgate[1]\n')
            elif pads_temp[i]=='6':
                pads_final.append(in_nets[i]+' 8 6 5 #tgate[1]\n')                                  
            elif pads_temp[i]=='7':
                pads_final.append(in_nets[i]+' 8 7 5 #tgate[1]\n')                                  
            elif pads_temp[i]=='8':
                pads_final.append(in_nets[i]+' 8 8 5 #tgate[1]\n')                                 
            elif pads_temp[i]=='9':
                pads_final.append(in_nets[i]+' 8 9 5 #tgate[1]\n')
            elif pads_temp[i]=='10':
                pads_final.append(in_nets[i]+' 8 10 5 #tgate[1]\n')
            elif pads_temp[i]=='11':
                pads_final.append(in_nets[i]+' 8 11 5 #tgate[1]\n')
            elif pads_temp[i]=='12':
                pads_final.append(in_nets[i]+' 8 12 5 #tgate[1]\n')
            elif pads_temp[i]=='40':
                pads_final.append(in_nets[i]+' 0 12 5 #int[5]\n')
            elif pads_temp[i]=='41':
                pads_final.append(in_nets[i]+' 0 13 0 #int[0]\n')
            elif pads_temp[i]=='42':
                pads_final.append(in_nets[i]+' 0 13 1 #int[1]\n')
            elif pads_temp[i]=='43':
                pads_final.append(in_nets[i]+' 0 13 2 #int[2]\n')
            elif pads_temp[i]=='44':
                pads_final.append(in_nets[i]+' 0 13 3 #int[3]\n')                                  
            elif pads_temp[i]=='45':
                pads_final.append(in_nets[i]+' 0 13 4 #int[4]\n')                                  
            elif pads_temp[i]=='46':
                pads_final.append(in_nets[i]+' 0 13 5 #int[5]\n')                                 
            elif pads_temp[i]=='47':
                pads_final.append(in_nets[i]+' 0 14 0 #int[0]\n')
            elif pads_temp[i]=='48':
                pads_final.append(in_nets[i]+' 0 14 1 #int[1]\n')
            elif pads_temp[i]=='49':
                pads_final.append(in_nets[i]+' 0 14 2 #int[2]\n')
            elif pads_temp[i]=='50':
                pads_final.append(in_nets[i]+' 0 14 3 #int[3]\n')
            elif pads_temp[i]=='51':
                pads_final.append(in_nets[i]+' 0 14 4 #int[4]\n')                                 
            elif pads_temp[i]=='52':
                pads_final.append(in_nets[i]+' 0 14 5 #int[5]\n')
            elif pads_temp[i]=='53':
                pads_final.append(in_nets[i]+' 1 15 0 #int[0]\n')
            elif pads_temp[i]=='54':
                pads_final.append(in_nets[i]+' 1 15 1 #int[1]\n')
            elif pads_temp[i]=='55':
                pads_final.append(in_nets[i]+' 1 15 2 #int[2]\n')
            elif pads_temp[i]=='56':
                pads_final.append(in_nets[i]+' 1 15 3 #int[3]\n')
            elif pads_temp[i]=='57':
                pads_final.append(in_nets[i]+' 1 15 4 #int[4]\n')
            elif pads_temp[i]=='58':
                pads_final.append(in_nets[i]+' 1 15 5 #int[5]\n')
                                  
    if ' pad_out\n' in line and len(line.split(' '))>2:
        pads_temp = line.split(' pad_out\n')[0].split('# ')[1].split(' ')
        for i in range(len(pads_temp)):
            if pads_temp[i]=='1':
                pads_final.append('out:'+out_nets[i]+' 8 1 5 #tgate[1]\n')
            elif pads_temp[i]=='2':
                pads_final.append('out:'+out_nets[i]+' 8 2 5 #tgate[1]\n')
            elif pads_temp[i]=='3':
                pads_final.append('out:'+out_nets[i]+' 8 3 5 #tgate[1]\n')
            elif pads_temp[i]=='4':
                pads_final.append('out:'+out_nets[i]+' 8 4 5 #tgate[1]\n')
            elif pads_temp[i]=='5':
                pads_final.append('out:'+out_nets[i]+' 8 5 5 #tgate[1]\n')
            elif pads_temp[i]=='6':
                pads_final.append('out:'+out_nets[i]+' 8 6 5 #tgate[1]\n')                                  
            elif pads_temp[i]=='7':
                pads_final.append('out:'+out_nets[i]+' 8 7 5 #tgate[1]\n')                                  
            elif pads_temp[i]=='8':
                pads_final.append('out:'+out_nets[i]+' 8 8 5 #tgate[1]\n')                                 
            elif pads_temp[i]=='9':
                pads_final.append('out:'+out_nets[i]+' 8 9 5 #tgate[1]\n')
            elif pads_temp[i]=='10':
                pads_final.append('out:'+out_nets[i]+' 8 10 5 #tgate[1]\n')
            elif pads_temp[i]=='11':
                pads_final.append('out:'+out_nets[i]+' 8 11 5 #tgate[1]\n')
            elif pads_temp[i]=='12':
                pads_final.append('out:'+out_nets[i]+' 8 12 5 #tgate[1]\n')
            elif pads_temp[i] == '13':
                pads_final.append('out:'+out_nets[i]+' 1 15 0 #ana_buff_out[0]\n')
            elif pads_temp[i] == '14':
                pads_final.append('out:'+out_nets[i]+' 2 15 0 #ana_buff_out[0]\n')
            elif pads_temp[i] == '15':
                pads_final.append('out:'+out_nets[i]+' 3 15 0 #ana_buff_out[0]\n')
            elif pads_temp[i] == '16':
                pads_final.append('out:'+out_nets[i]+' 4 15 0 #ana_buff_out[0]\n')
            elif pads_temp[i] == '17':
                pads_final.append('out:'+out_nets[i]+' 5 15 0 #ana_buff_out[0]\n')                                  
            elif pads_temp[i]=='40':
                pads_final.append('out:'+out_nets[i]+' 0 12 5 #int[5]\n')
            elif pads_temp[i]=='41':
                pads_final.append('out:'+out_nets[i]+' 0 13 0 #int[0]n')
            elif pads_temp[i]=='42':
                pads_final.append('out:'+out_nets[i]+' 0 13 1 #int[1]\n')
            elif pads_temp[i]=='43':
                pads_final.append('out:'+out_nets[i]+' 0 13 2 #int[2]\n')
            elif pads_temp[i]=='44':
                pads_final.append('out:'+out_nets[i]+' 0 13 3 #int[3]\n')                                  
            elif pads_temp[i]=='45':
                pads_final.append('out:'+out_nets[i]+' 0 13 4 #int[4]\n')                                  
            elif pads_temp[i]=='46':
                pads_final.append('out:'+out_nets[i]+' 0 13 5 #int[5]\n')                                 
            elif pads_temp[i]=='47':
                pads_final.append('out:'+out_nets[i]+' 0 14 0 #int[0]\n')
            elif pads_temp[i]=='48':
                pads_final.append('out:'+out_nets[i]+' 0 14 1 #int[1]\n')
            elif pads_temp[i]=='49':
                pads_final.append('out:'+out_nets[i]+' 0 14 2 #int[2]\n')
            elif pads_temp[i]=='50':
                pads_final.append('out:'+out_nets[i]+' 0 14 3 #int[3]\n')
            elif pads_temp[i]=='51':
                pads_final.append('out:'+out_nets[i]+' 0 14 4 #int[4]\n')                                 
            elif pads_temp[i]=='52':
                pads_final.append('out:'+out_nets[i]+' 0 14 5 #int[5]\n')
            elif pads_temp[i]=='53':
                pads_final.append('out:'+out_nets[i]+' 1 15 0 #int[0]\n')
            elif pads_temp[i]=='54':
                pads_final.append('out:'+out_nets[i]+' 1 15 1 #int[1]\n')
            elif pads_temp[i]=='55':
                pads_final.append('out:'+out_nets[i]+' 1 15 2 #int[2]\n')
            elif pads_temp[i]=='56':
                pads_final.append('out:'+out_nets[i]+' 1 15 3 #int[3]\n')
            elif pads_temp[i]=='57':
                pads_final.append('out:'+out_nets[i]+' 1 15 4 #int[4]\n')
            elif pads_temp[i]=='58':
                pads_final.append('out:'+out_nets[i]+' 1 15 5 #int[5]\n')



f = open(infile_name+'.pads','w')

for i in pads_final:
    f.write(i)

f.close()














                                  
                                  
