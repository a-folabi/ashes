#************************************Need to hand route OutMatrix prog_r, run_r, AVDD_r, Vgrun_r
#******************************Input from CEW is CEW col-8, Input from CNS is CNS col-10
#*****************************Amatrix col+ Bmatrix col needs to be >= CEW_col+CNS_col+2

#----------------------------To Do: drain cutoff to matrix connection, pin to drain cutoff connection

import json
import math
import os

with open('cell2cell_350nm.json','r') as file:
    data = json.load(file)
    
with open('analog_std_cells.json','r') as lib:
    lib = json.load(lib)
    



cab_list = []
for general_info in data:
    foundry=data["foundry"]
    process_node=data["process_node"]
    if "cab" in general_info and "_" not in general_info:
        cab_list.append(general_info)
    #block_list=data["cab"]
    #if "cab2" in data:
    #    block_list2=data["cab2"]
        
    
for cab in cab_list:
    f = open('cab.py','w')
    block_list = data[cab]
    #calculate A and B matrix size
    cab_input_num=0
    cab_output_num=0
    for block in block_list:
        for lib_block in lib:
            if block[-1].isnumeric():
                block = block.split("__")[0]
            if block==lib_block:
                for input_port in lib[lib_block]["W"]:
                    if "VD_P" not in input_port and "[" not in input_port:
                        cab_input_num += 1
                    elif "VD_P" not in input_port and "[" in input_port:
                        cab_input_num += int(input_port.split(":")[1].split("]")[0])+1
                for output_port in lib[lib_block]["E"]:
                    if "VD_P" not in output_port and "[" not in output_port:
                        cab_output_num += 1
                    elif "VD_P" not in output_port and "[" in output_port:
                        cab_output_num += int(output_port.split(":")[1].split("]")[0])+1
                        
                        
    #Calculate C block size
    Cblock_row = data[cab+"_Cblock_rows"]
    CEW_col = data[cab+"_CEW_cols"]
    CNS_col = data[cab+"_CNS_cols"]
    Cblock_row_inst = int(Cblock_row/4)
    CEW_col_inst = int(CEW_col/2)
    CNS_col_inst = int(CNS_col/2)
       
    Amatrix_row = len(block_list)
    Amatrix_col = int(data[cab+"_Amatrix_cols"]/2)
    Bmatrix_row = len(block_list)-1
    Bmatrix_col = math.ceil(cab_output_num/2)
                        
                        
    #importing modules
    f.write("import ashes_fg as af\n")
    f.write("from ashes_fg.asic.asic_compile import *\n")
    f.write("from ashes_fg.class_lib_new import *\n")
    f.write("from ashes_fg.class_lib_mux import *\n")
    f.write("from ashes_fg.class_lib_cab import *\n")
    f.write("from ashes_fg.asic.asic_systems import *\n\n")
    
    #CSC block
    f.write("Top = Circuit()\n\n")
    f.write("# C,S,C Blocks\n")
    f.write("BlockIsland = Island(Top)\n\n")
    f.write("#VMM's\n")
            
            
    f.write("C_EW = IndirectVMM(Top,["+str(Cblock_row)+","+str(CEW_col)+"],island=BlockIsland,decoderPlace=False)\n")
    f.write("C_NS = IndirectVMM(Top,["+str(Cblock_row)+","+str(CNS_col)+"],island=BlockIsland,decoderPlace=False,loc = [0,"+str(CEW_col_inst+Cblock_row_inst+5)+"])\n\n")
    f.write("Block_Switch = ST_BMatrix(Top,BlockIsland,["+str(Cblock_row_inst)+",1])\n")
    f.write("Block_Switch.place([0,"+str(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst)+"])\n\n")
    
    #Sblock
    f.write("#SBLOCK\n")
    f.write("SEC1 = S_SEC1(Top,BlockIsland,["+str(Cblock_row_inst)+",1])\n")
    f.write("SEC1.place([0,"+str(CEW_col_inst)+"])\n\n")
    f.write("SBuff = S_Buffer(Top,BlockIsland,["+str(Cblock_row_inst)+",1])\n")
    f.write("SBuff.place([0,"+str(CEW_col_inst+1)+"])\n\n")
    
    
    for i in range(Cblock_row_inst):
        if i+1-Cblock_row_inst<0: 
            f.write("SpaceUp_"+str(i)+" = S_spaceUP(Top,BlockIsland,["+str(Cblock_row_inst-1-i)+",1])\n")
            f.write("SpaceUp_"+str(i)+".place([0,"+str(CEW_col_inst+2+i)+"])\n")
            if i+1-Cblock_row_inst==-1:
                f.write("SpaceUp_"+str(i)+".markAbut()\n\n")
        f.write("Conn_"+str(i)+" = S_Conn12(Top,BlockIsland)\n")
        f.write("Conn_"+str(i)+".place(["+str(Cblock_row_inst-1-i)+","+str(CEW_col_inst+2+i)+"])\n")
        f.write("Conn_"+str(i)+".markAbut()\n\n")
        if i>0:
            f.write("SpaceDown_"+str(i)+" = S_spaceDOWN(Top,BlockIsland,["+str(i)+",1])\n")
            f.write("SpaceDown_"+str(i)+".place(["+str(Cblock_row_inst-i)+","+str(CEW_col_inst+2+i)+"])\n")
            if i==1:
                f.write("SpaceDown_"+str(i)+".markAbut()\n\n")
                
    f.write("SEC2 = S_SEC2(Top,BlockIsland,["+str(Cblock_row_inst)+",1])\n")
    f.write("SEC2.place([0,"+str(CEW_col_inst+Cblock_row_inst+2)+"])\n\n")
    f.write("Conn_"+str(Cblock_row_inst)+" = S_Conn23(Top,BlockIsland,["+str(Cblock_row_inst)+",1])\n")
    f.write("Conn_"+str(Cblock_row_inst)+".place([0,"+str(CEW_col_inst+Cblock_row_inst+3)+"])\n\n")
    f.write("SEC3 = S_SEC3(Top,BlockIsland,["+str(Cblock_row_inst)+",1])\n")
    f.write("SEC3.place([0,"+str(CEW_col_inst+Cblock_row_inst+4)+"])\n\n")
    
    
    
    #Decoders for CSC
    f.write("# Decoders\n")
    if 32<(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2<65:
        C_gate_bit = 6
        f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=6)\n")
    elif 16<(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2<33:
        C_gate_bit = 5
        f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=5)\n")
    elif 64<(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2<129:
        f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=7)\n")
        C_gate_bit=7
    elif 8<(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2<17:
        C_gate_bit=4
        f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=4)\n")
        
    f.write("Block_GateSwitch = STD_IndirectGateSwitch(Top,island=BlockIsland,num="+str(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst)+")\n\n")
    
    if 16<Cblock_row_inst*4<33:
        C_drain_bit = 5
        f.write("Block_DrainDecode = STD_DrainDecoder(Top,island=BlockIsland,bits=5)\n")
        f.write("Block_DrainSelect = RunDrainSwitch(Top,island=BlockIsland,num="+str(Cblock_row_inst)+")\n")
        f.write("Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num="+str(Cblock_row_inst)+")\n")
    elif 32<Cblock_row_inst*4<65:
        C_drain_bit=6
        f.write("Block_DrainDecode = STD_DrainDecoder(Top,island=BlockIsland,bits=6)\n")
        f.write("Block_DrainSelect = RunDrainSwitch(Top,island=BlockIsland,num="+str(Cblock_row_inst)+")\n")
        f.write("Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num="+str(Cblock_row_inst)+")\n") 
    elif 8<Cblock_row_inst*4<17:
        C_drain_bit=4
        f.write("Block_DrainDecode = STD_DrainDecoder(Top,island=BlockIsland,bits=4)\n")
        f.write("Block_DrainSelect = RunDrainSwitch(Top,island=BlockIsland,num="+str(Cblock_row_inst)+")\n")
        f.write("Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num="+str(Cblock_row_inst)+")\n")
    
    
    f.write("for i in range("+str(CEW_col_inst+1)+","+str(CEW_col_inst+1+Cblock_row_inst+1)+"):\n")
    f.write("\tERASE_IndirectGateSwitch(Top,island=BlockIsland,col=i)\n")
    f.write("ERASE_IndirectGateSwitch(Top,island=BlockIsland,col="+str(CEW_col_inst+1+Cblock_row_inst+2)+")\n\n")
    
    
    #CAB 
    f.write("# CAB\n")
    f.write("CABIsland = Island(Top)\n\n")
    f.write("# A matrix\n")
    f.write("Atop = BlockTop(Top,CABIsland,[1,"+str(Amatrix_col)+"])\n")
    f.write("Atop.place([0,0])\n")
    f.write("Amatrix = IndirectVMM(Top,["+str(Amatrix_row*4)+","+str(Amatrix_col*2)+"],island=CABIsland,decoderPlace=False,loc=[1,0])\n\n")
    f.write("# B matrix\n")
    f.write("Btop = BlockTop(Top,CABIsland,[1,"+str(Bmatrix_col)+"])\n")
    f.write("Btop.place([0,"+str(Amatrix_col)+"])\n")
    f.write("Bmatrix = IndirectVMM(Top,["+str(Bmatrix_row*4)+","+str(Bmatrix_col*2)+"],island=CABIsland,decoderPlace=False,loc=[1,"+str(Amatrix_col)+"])\n")
    f.write("Bbot = B_bot(Top,CABIsland,[1,"+str(Bmatrix_col)+"])\n")
    f.write("Bbot.place(["+str(Bmatrix_row+1)+","+str(Amatrix_col)+"])\n\n")
    
    #CAB switches
    for block in block_list:
        if "4WTA_IndirectProg" in block or "TA2Cell_Direct" in block: 
            f.write("Bswitch"+str(block_list.index(block))+" = ST_BMatrix_NoSwitch(Top,CABIsland)\n")
            f.write("Bswitch"+str(block_list.index(block))+".place(["+str(block_list.index(block))+","+str(Amatrix_col+Bmatrix_col)+"])\n")
            f.write("Bswitch"+str(block_list.index(block))+".markAbut()\n\n")
        else:
            f.write("Bswitch"+str(block_list.index(block))+" = ST_BMatrix(Top,CABIsland)\n")
            f.write("Bswitch"+str(block_list.index(block))+".place(["+str(block_list.index(block))+","+str(Amatrix_col+Bmatrix_col)+"])\n")
            f.write("Bswitch"+str(block_list.index(block))+".markAbut()\n\n")
    f.write("Bswitch"+str(len(block_list))+" = ST_BMatrix(Top,CABIsland)\n")
    f.write("Bswitch"+str(len(block_list))+".place(["+str(len(block_list))+","+str(Amatrix_col+Bmatrix_col)+"])\n")
    f.write("Bswitch"+str(len(block_list))+".markAbut()\n\n")
    
    f.write("BtoOut = OutSwitch(Top,CABIsland,[1,"+str(Bmatrix_col)+"])\n")
    f.write("BtoOut.place(["+str(Bmatrix_row+3)+","+str(Amatrix_col)+"])\n\n")
    f.write("# Output Matrix\n")
    f.write("Outmatrix = IndirectVMM(Top,[8,"+str(Bmatrix_col*2)+"],island=CABIsland,decoderPlace=False,loc=["+str(Bmatrix_row+4)+","+str(Amatrix_col)+"])\n")
    f.write("Oswitch = ST_BMatrix(Top,CABIsland,[2,1])\n")
    f.write("Oswitch.place(["+str(Bmatrix_row+4)+","+str(Amatrix_col+Bmatrix_col)+"])\n\n")
    
    
    
    #CAB element placement
    CAB_device_row_count = 2
    f.write("# CAB Elements\n")
    for block in block_list:
            for lib_block in lib:
                if block[-1].isnumeric():
                    if block.split("__")[0] == lib_block:
                        f.write(block+" = "+foundry+process_node+"_"+block.split("__")[0]+"(Top,CABIsland)\n")
                        f.write(block+".place(["+str(CAB_device_row_count)+","+str(Amatrix_col+Bmatrix_col+1)+"])\n")
                        CAB_device_row_count += 1
                        f.write(block+".markCABDevice()\n\n")
                else:
                    if block == lib_block:
                        f.write(block+" = "+foundry+process_node+"_"+block+"(Top,CABIsland)\n")
                        f.write(block+".place(["+str(CAB_device_row_count)+","+str(Amatrix_col+Bmatrix_col+1)+"])\n")
                        CAB_device_row_count += 1
                        f.write(block+".markCABDevice()\n\n")
                        
    #volatile switch
    f.write("VolSwitchIsland = Island(Top)\n\n")
    f.write("VolSwitch = TSMC350nm_volatile_swcs(Top,VolSwitchIsland,[1,6])\n")
    f.write("VolSwitch.place([0,0])\n\n")
    
    #CAB decoders
    f.write("# Decoders\n")
    
    if 32<(Bmatrix_row+6)*4<65:
        CAB_drain_bit=6
        f.write("CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=6)\n")
        f.write("CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n")
        f.write("CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n\n")
    elif 16<(Bmatrix_row+6)*4<33:
        CAB_drain_bit=5
        f.write("CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=5)\n")
        f.write("CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n")
        f.write("CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n\n")
    elif 64<(Bmatrix_row+6)*4<129:
        CAB_drain_bit=7
        f.write("CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=7)\n")
        f.write("CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n")
        f.write("CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n\n")
    
    
    f.write("CAB_GateSwitch = STD_GorS_IndirectSwitches(Top,CABIsland,num="+str(Amatrix_col+Bmatrix_col+2)+")\n")
    f.write("ERASE_IndirectGateSwitch(Top,CABIsland,col="+str(Amatrix_col+Bmatrix_col)+")\n")
    f.write("CABElements_GateSwitch = STD_IndirectGateSwitch(Top,CABIsland,col="+str(Amatrix_col+Bmatrix_col+1)+")\n\n")
    
    
    # CAB device connections
    f.write("# Bmatrix <--> CAB Elements Connections\n\n")
    if cab_output_num%2 ==0:
        Bmatrix_feedback_offset = 0
    else:
        Bmatrix_feedback_offset = 1
            
    
    feedback_counter=0
    for block in block_list:
        f.write("\n")
        CAB_net_counter = block_list.index(block)
        for lib_block in lib:
            if block[-1].isnumeric():
                if block.split("__")[0] == lib_block:
                    port_counter=0
                    for port in lib[block.split("__")[0]]["W"]:
                        if port == "VD_P":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P\n")
                        elif port == "VD_P[0:1]":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P[0:2]\n")
                        elif port == "VD_P[0:2]":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P[0:3]\n")
                        elif port == "VD_P[0:3]":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P[0:4]\n")
                        else:
                            if "[0:1]" in port:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+":"+str(port_counter+2)+"]\n")
                                port_counter += 2
                            elif "[0:2]" in port:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+":"+str(port_counter+3)+"]\n")
                                port_counter += 3
                            elif "[0:3]" in port:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+":"+str(port_counter+4)+"]\n")
                                port_counter += 4
                            else:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+"]\n")
                                port_counter += 1
                    for feedback_port in lib[block.split("__")[0]]["E"]:
                        if "[0:1]" in feedback_port:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+":"+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter+2)+"]\n")
                            feedback_counter += 2
                        elif "[0:2]" in feedback_port:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+":"+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter+3)+"]\n")  
                            feedback_counter += 3
                        elif "[0:3]" in feedback_port:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+":"+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter+4)+"]\n")  
                            feedback_counter += 4
                        else:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+"]\n")  
                            feedback_counter += 1
                    if block_list.index(block) == 0:
                        for top_port in lib[block.split("__")[0]]["N"]:
                            if top_port == "Vs" and "4WTA_IndirectProg" in block:
                                f.write(block+"."+top_port+" += CABElements_GateSwitch.VDD[1]\n")
                            elif top_port == "Vsel[0:1]":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B\n")
                            elif top_port == "Vsel":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B[0]\n")
                            elif top_port == "VINJ":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VINJ\n")
                            elif top_port == "RUN":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.run_r\n")
                            elif top_port == "Vg[0:1]" or top_port == "VG[0:1]":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.Vg\n")
                            elif top_port == "Vg" or top_port == "VG":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.Vg[0]\n")
                            elif top_port == "PROG":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.prog_r\n")
                            elif top_port == "VTUN":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VTUN\n")
                            elif top_port == "GND":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.GND[0]\n")
                            elif top_port == "VPWR":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VDD[1]\n")
                    else:
                        for top_port in lib[block.split("__")[0]]["N"]:
                            if top_port == "Vs" and "4WTA_IndirectProg" in block:
                                f.write(block+"."+top_port+" += CABElements_GateSwitch.VDD[1]\n")
                            elif top_port == "Vsel[0:1]":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B\n")
                                else:
                                    if "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B\n")
                            elif top_port == "Vsel":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vsel_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    elif "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b[0]\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0]\n")
                                else:
                                    if "Vsel_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    elif "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b[0]\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0]\n")
                            elif top_port == "VINJ":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "VINJ_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VINJ += "+block_list[block_list.index(block)-1]+".VINJ_b\n")
                                    else:
                                        f.write(block+".VINJ += CABElements_GateSwitch.VINJ\n")
                                else:
                                    if "VINJ_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VINJ += "+block_list[block_list.index(block)-1]+".VINJ_b\n")
                                    else:
                                        f.write(block+".VINJ += CABElements_GateSwitch.VINJ\n")
                            elif top_port == "RUN":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "RUN_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".RUN += "+block_list[block_list.index(block)-1]+".RUN_b\n")
                                    else:
                                        f.write(block+".RUN += CABElements_GateSwitch.run_r\n")
                                else:
                                    if "RUN_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".RUN += "+block_list[block_list.index(block)-1]+".RUN_b\n")
                                    else:
                                        f.write(block+".RUN += CABElements_GateSwitch.run_r\n")
                            elif top_port == "Vg[0:1]":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg\n")
                                else:
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg\n")
                            elif top_port == "VG[0:1]":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".VG += CABElements_GateSwitch.Vg\n")
                                else:
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".VG += CABElements_GateSwitch.Vg\n")
                            elif top_port == "Vg":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg[0]\n")
                                else:
                                    if "Vg_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg[0]\n")
                            elif top_port == "VG":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                    else:
                                        f.write(block+".VG += CABElements_GateSwitch.Vg[0]\n")
                            elif top_port == "PROG":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "PROG_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".PROG += "+block_list[block_list.index(block)-1]+".PROG_b\n")
                                    else:
                                        f.write(block+".PROG += CABElements_GateSwitch.prog_r\n")
                                else:
                                    if "PROG_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".PROG += "+block_list[block_list.index(block)-1]+".PROG_b\n")
                                    else:
                                        f.write(block+".PROG += CABElements_GateSwitch.prog_r\n")
                            elif top_port == "VTUN":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "VTUN_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VTUN += "+block_list[block_list.index(block)-1]+".VTUN_b\n")
                                    else:
                                        f.write(block+".VTUN += CABElements_GateSwitch.VTUN\n")
                                else:
                                    if "VTUN_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VTUN += "+block_list[block_list.index(block)-1]+".VTUN_b\n")
                                    else:
                                        f.write(block+".VTUN += CABElements_GateSwitch.VTUN\n")
                            elif top_port == "GND":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "GND_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".GND += "+block_list[block_list.index(block)-1]+".GND_b\n")
                                    else:
                                        f.write(block+".GND += CABElements_GateSwitch.GND[0]\n")
                                else:
                                    if "GND_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".GND += "+block_list[block_list.index(block)-1]+".GND_b\n")
                                    else:
                                        f.write(block+".GND += CABElements_GateSwitch.GND[0]\n")
                            elif top_port == "VPWR":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "VPWR_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VPWR += "+block_list[block_list.index(block)-1]+".VPWR_b\n")
                                    else:
                                        f.write(block+".VPWR += CABElements_GateSwitch.VDD[1]\n")
                                else:
                                    if "VPWR_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VPWR += "+block_list[block_list.index(block)-1]+".VPWR_b\n")
                                    else:
                                        f.write(block+".VPWR += CABElements_GateSwitch.VDD[1]\n")
                                    
                                
            else:
                if block == lib_block:
                    port_counter=0
                    for port in lib[block]["W"]:
                        if port == "VD_P":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P\n")
                        elif port == "VD_P[0:1]":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P[0:2]\n")
                        elif port == "VD_P[0:2]":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P[0:3]\n")
                        elif port == "VD_P[0:3]":
                            f.write(block+".VD_P += Bswitch"+str(CAB_net_counter)+".P[0:4]\n")
                        else:
                            if "[0:1]" in port:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+":"+str(port_counter+2)+"]\n")
                                port_counter += 2
                            elif "[0:2]" in port:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+":"+str(port_counter+3)+"]\n")
                                port_counter += 3
                            elif "[0:3]" in port:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+":"+str(port_counter+4)+"]\n")
                                port_counter += 4
                            else:
                                f.write(block+"."+port.split("[")[0]+" += Bswitch"+str(CAB_net_counter)+".A["+str(port_counter)+"]\n")
                                port_counter += 1
                    for feedback_port in lib[block]["E"]:
                        if "[0:1]" in feedback_port:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+":"+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter+2)+"]\n")
                            feedback_counter += 2
                        elif "[0:2]" in feedback_port:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+":"+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter+3)+"]\n")  
                            feedback_counter += 3
                        elif "[0:3]" in feedback_port:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+":"+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter+4)+"]\n")  
                            feedback_counter += 4
                        else:
                            f.write(block+"."+feedback_port.split("[")[0]+" += CAB_GateSwitch.Input["+str(Amatrix_col*2+Bmatrix_feedback_offset+feedback_counter)+"]\n")  
                            feedback_counter += 1
                    if block_list.index(block) == 0:
                        for top_port in lib[block]["N"]:
                            if top_port == "Vs" and "4WTA_IndirectProg" in block:
                                f.write(block+"."+top_port+" += CABElements_GateSwitch.VDD[1]\n")
                            elif top_port == "Vsel[0:1]":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B\n")
                            elif top_port == "Vsel":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B[0]\n")
                            elif top_port == "VINJ":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VINJ\n")
                            elif top_port == "RUN":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.run_r\n")
                            elif top_port == "Vg[0:1]" or top_port == "VG[0:1]":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.Vg\n")
                            elif top_port == "Vg" or top_port == "VG":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.Vg[0]\n")
                            elif top_port == "PROG":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.prog_r\n")
                            elif top_port == "VTUN":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VTUN\n")
                            elif top_port == "GND":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.GND[0]\n")
                            elif top_port == "VPWR":
                                f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VDD[1]\n")
                    else:
                        for top_port in lib[block]["N"]:
                            if top_port == "Vs" and "4WTA_IndirectProg" in block:
                                f.write(block+"."+top_port+" += CABElements_GateSwitch.VDD[1]\n")
                            elif top_port == "Vsel[0:1]":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B\n")
                                else:
                                    if "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B\n")
                            elif top_port == "Vsel":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vsel_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0]\n")
                                else:
                                    if "Vsel_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b\n")
                                    else:
                                        f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0]\n")
                            elif top_port == "VINJ":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "VINJ_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VINJ += "+block_list[block_list.index(block)-1]+".VINJ_b\n")
                                    else:
                                        f.write(block+".VINJ += CABElements_GateSwitch.VINJ\n")
                                else:
                                    if "VINJ_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VINJ += "+block_list[block_list.index(block)-1]+".VINJ_b\n")
                                    else:
                                        f.write(block+".VINJ += CABElements_GateSwitch.VINJ\n")
                            elif top_port == "RUN":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "RUN_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".RUN += "+block_list[block_list.index(block)-1]+".RUN_b\n")
                                    else:
                                        f.write(block+".RUN += CABElements_GateSwitch.run_r\n")
                                else:
                                    if "RUN_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".RUN += "+block_list[block_list.index(block)-1]+".RUN_b\n")
                                    else:
                                        f.write(block+".RUN += CABElements_GateSwitch.run_r\n")
                            elif top_port == "Vg[0:1]":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg\n")
                                else:
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg\n")
                            elif top_port == "VG[0:1]":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".VG += CABElements_GateSwitch.Vg\n")
                                else:
                                    if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    else:
                                        f.write(block+".VG += CABElements_GateSwitch.Vg\n")
                            elif top_port == "Vg":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg[0]\n")
                                else:
                                    if "Vg_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                    else:
                                        f.write(block+".Vg += CABElements_GateSwitch.Vg[0]\n")
                            elif top_port == "VG":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "Vg_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                    else:
                                        f.write(block+".VG += CABElements_GateSwitch.Vg[0]\n")
                                else:
                                    if "Vg_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                    elif "VG_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                    elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                    elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                    else:
                                        f.write(block+".VG += CABElements_GateSwitch.Vg[0]\n")
                            elif top_port == "PROG":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "PROG_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".PROG += "+block_list[block_list.index(block)-1]+".PROG_b\n")
                                    else:
                                        f.write(block+".PROG += CABElements_GateSwitch.prog_r\n")
                                else:
                                    if "PROG_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".PROG += "+block_list[block_list.index(block)-1]+".PROG_b\n")
                                    else:
                                        f.write(block+".PROG += CABElements_GateSwitch.prog_r\n")
                            elif top_port == "VTUN":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "VTUN_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VTUN += "+block_list[block_list.index(block)-1]+".VTUN_b\n")
                                    else:
                                        f.write(block+".VTUN += CABElements_GateSwitch.VTUN\n")
                                else:
                                    if "VTUN_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VTUN += "+block_list[block_list.index(block)-1]+".VTUN_b\n")
                                    else:
                                        f.write(block+".VTUN += CABElements_GateSwitch.VTUN\n")
                            elif top_port == "GND":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "GND_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".GND += "+block_list[block_list.index(block)-1]+".GND_b\n")
                                    else:
                                        f.write(block+".GND += CABElements_GateSwitch.GND[0]\n")
                                else:
                                    if "GND_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".GND += "+block_list[block_list.index(block)-1]+".GND_b\n")
                                    else:
                                        f.write(block+".GND += CABElements_GateSwitch.GND[0]\n")
                            elif top_port == "VPWR":
                                if block_list[block_list.index(block)-1][-1].isnumeric():
                                    if "VPWR_b" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                        f.write(block+".VPWR += "+block_list[block_list.index(block)-1]+".VPWR_b\n")
                                    else:
                                        f.write(block+".VPWR += CABElements_GateSwitch.VDD[1]\n")
                                else:
                                    if "VPWR_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                        f.write(block+".VPWR += "+block_list[block_list.index(block)-1]+".VPWR_b\n")
                                    else:
                                        f.write(block+".VPWR += CABElements_GateSwitch.VDD[1]\n")
    
            
    #C to cab connections
    f.write("\n")
    #First column of Amatrix = VDD+GND
    f.write("CAB_GateSwitch.Input[0] += CABElements_GateSwitch.VPWR[0]\n")
    f.write("CABElements_GateSwitch.VPWR[1] += CABElements_GateSwitch.VPWR[0]\n")
    
    #CEW -> A switch
    f.write("C_EW.Vsel_b += CAB_GateSwitch.Vsel[0:"+str(CEW_col)+"]\n")
    f.write("C_EW.Vg_b += CAB_GateSwitch.Vg_global[0:"+str(CEW_col)+"]\n")
    f.write("C_EW.VTUN_b += CAB_GateSwitch.VTUN[0:"+str(CEW_col_inst)+"]\n")
    for i in range(CEW_col):
        if i%2==1:    
            f.write("C_EW.GND_b["+str(i)+"] += CAB_GateSwitch.GND["+str(int((i-1)/2))+"]\n")
    f.write("CAB_GateSwitch.GND[0] += CAB_GateSwitch.Input[1]\n")
    for i in range(CEW_col):
        if i%2==1:    
            f.write("C_EW.VINJ_b["+str(i)+"] += CAB_GateSwitch.VINJ["+str(int((i-1)/2))+"]\n")
            
    #CEW -> A Input
    for i in range(2,CEW_col-6):
        f.write("C_EW.Vs_b["+str(i)+"] += CAB_GateSwitch.Input["+str(i)+"]\n")
        
    #SEC connections
    f.write("SEC1.VINJ_b += CAB_GateSwitch.VINJ["+str(CEW_col_inst)+"]\n")
    f.write("SEC1.VTUN_b += CAB_GateSwitch.VTUN["+str(CEW_col_inst)+"]\n")
    f.write("SEC1.GND_b[1] += CAB_GateSwitch.GND["+str(CEW_col_inst)+"]\n")
    f.write("SEC1.Vsel_b[0] += CAB_GateSwitch.Vsel["+str(CEW_col+1)+"]\n")
    f.write("SEC1.Vsel_b[1] += CAB_GateSwitch.Vsel["+str(CEW_col)+"]\n")
    f.write("SEC1.Vg_b[0] += CAB_GateSwitch.Vg_global["+str(CEW_col+1)+"]\n")
    f.write("SEC1.Vg_b[1] += CAB_GateSwitch.Vg_global["+str(CEW_col)+"]\n")
    
    f.write("SEC2.VINJ_b += CAB_GateSwitch.VINJ["+str(CEW_col_inst+1)+"]\n")
    f.write("SEC2.VTUN_b += CAB_GateSwitch.VTUN["+str(CEW_col_inst+1)+"]\n")
    f.write("SEC2.GND_b[1] += CAB_GateSwitch.GND["+str(CEW_col_inst+1)+"]\n")
    f.write("SEC2.Vsel_b[0] += CAB_GateSwitch.Vsel["+str(CEW_col+3)+"]\n")
    f.write("SEC2.Vsel_b[1] += CAB_GateSwitch.Vsel["+str(CEW_col+2)+"]\n")
    f.write("SEC2.Vg_b[0] += CAB_GateSwitch.Vg_global["+str(CEW_col+3)+"]\n")
    f.write("SEC2.Vg_b[1] += CAB_GateSwitch.Vg_global["+str(CEW_col+2)+"]\n")
    
    f.write("SEC3.VINJ_b += CAB_GateSwitch.VINJ["+str(CEW_col_inst+2)+"]\n")
    f.write("SEC3.VTUN_b += CAB_GateSwitch.VTUN["+str(CEW_col_inst+2)+"]\n")
    f.write("SEC3.GND_b[1] += CAB_GateSwitch.GND["+str(CEW_col_inst+2)+"]\n")
    f.write("SEC3.Vsel_b[0] += CAB_GateSwitch.Vsel["+str(CEW_col+5)+"]\n")
    f.write("SEC3.Vsel_b[1] += CAB_GateSwitch.Vsel["+str(CEW_col+4)+"]\n")
    f.write("SEC3.Vg_b[0] += CAB_GateSwitch.Vg_global["+str(CEW_col+5)+"]\n")
    f.write("SEC3.Vg_b[1] += CAB_GateSwitch.Vg_global["+str(CEW_col+4)+"]\n")
    
    
    #CNS -> CAB Gate Switch
    for i in range(int(CNS_col/2)):
        f.write("C_NS.VTUN_b["+str(i)+"] += CAB_GateSwitch.VTUN["+str(CEW_col_inst+3+i)+"]\n")
        f.write("C_NS.VINJ_b["+str(i*2+1)+"] += CAB_GateSwitch.VINJ["+str(CEW_col_inst+3+i)+"]\n")
        f.write("C_NS.GND_b["+str(i*2+1)+"] += CAB_GateSwitch.GND["+str(CEW_col_inst+3+i)+"]\n")
        f.write("C_NS.Vsel_b["+str(2*i)+"] += CAB_GateSwitch.Vsel["+str(2*i+CEW_col+6)+"]\n")
        f.write("C_NS.Vg_b["+str(2*i)+"] += CAB_GateSwitch.Vg_global["+str(2*i+CEW_col+6)+"]\n")
        f.write("C_NS.Vsel_b["+str(2*i+1)+"] += CAB_GateSwitch.Vsel["+str(2*i+1+CEW_col+6)+"]\n")
        f.write("C_NS.Vg_b["+str(2*i+1)+"] += CAB_GateSwitch.Vg_global["+str(2*i+1+CEW_col+6)+"]\n")
    
    #CNS -> A matrix Input
    #for i in range(8):
    #    f.write("C_NS.Vs_b["+str(i)+"] += CAB_GateSwitch.Input["+str(CEW_col-6+i)+"]\n")
    if cab_output_num%2 ==1:
        for i in range(CNS_col-10):
            f.write("C_NS.Vs_b["+str(i)+"] += CAB_GateSwitch.Input["+str(CEW_col-6+i)+"]\n")
    else:
        for i in range(CNS_col-11):
            f.write("C_NS.Vs_b["+str(i)+"] += CAB_GateSwitch.Input["+str(CEW_col-6+i)+"]\n")
        
        
    #Last column of CNS -> CAB gate switch
    f.write("C_NS.Vsel_b["+str(CNS_col-2)+"] += CABElements_GateSwitch.decode[0]\n")
    f.write("C_NS.VTUN_b["+str(CNS_col_inst-1)+"] += CABElements_GateSwitch.VTUN_T\n")
    f.write("C_NS.GND_b["+str(CNS_col-1)+"] += CABElements_GateSwitch.GND_T\n")
    f.write("C_NS.Vsel_b["+str(CNS_col-1)+"] += CABElements_GateSwitch.decode[1]\n")
    f.write("C_NS.VINJ_b["+str(CNS_col-1)+"] += CABElements_GateSwitch.VINJ_T\n")
    
    
    #CSC Decoder -> CSC
    for i in range(CEW_col_inst+1):
        f.write("Block_GateDecode.VINJ_b["+str(i)+"] += Block_GateSwitch.VINJ_T["+str(i)+"]\n")
        f.write("Block_GateDecode.GND_b["+str(i)+"] += Block_GateSwitch.GND_T["+str(i)+"]\n")
        f.write("Block_GateDecode.OUT["+str(i*2)+"] += Block_GateSwitch.decode["+str(i*2)+"]\n")
        f.write("Block_GateDecode.OUT["+str(i*2+1)+"] += Block_GateSwitch.decode["+str(i*2+1)+"]\n")
        #f.write("Block_GateDecode.RUN_OUT["+str(i*2)+"] += Block_GateSwitch.VPWR["+str(i*2)+"]\n")
        #f.write("Block_GateDecode.RUN_OUT["+str(i*2+1)+"] += Block_GateSwitch.VPWR["+str(i*2+1)+"]\n")
    if CNS_col_inst%2==1:
        f.write("Block_GateDecode.VINJ_b["+str(CEW_col_inst+1)+"] += Block_GateSwitch.VINJ_T["+str(CEW_col_inst+Cblock_row_inst+2)+"]\n")
        f.write("Block_GateDecode.GND_b["+str(CEW_col_inst+1)+"] += Block_GateSwitch.GND_T["+str(CEW_col_inst+Cblock_row_inst+2)+"]\n")
        f.write("Block_GateDecode.OUT["+str((CEW_col_inst+1)*2)+"] += Block_GateSwitch.decode["+str((CEW_col_inst+Cblock_row_inst+2)*2)+"]\n")
        f.write("Block_GateDecode.OUT["+str((CEW_col_inst+1)*2+1)+"] += Block_GateSwitch.decode["+str((CEW_col_inst+Cblock_row_inst+2)*2+1)+"]\n")
        #f.write("Block_GateDecode.RUN_OUT["+str((CEW_col_inst+1)*2)+"] += Block_GateSwitch.VPWR["+str((CEW_col_inst+Cblock_row_inst+2)*2)+"]\n")
        #f.write("Block_GateDecode.RUN_OUT["+str((CEW_col_inst+1)*2+1)+"] += Block_GateSwitch.VPWR["+str((CEW_col_inst+Cblock_row_inst+2)*2+1)+"]\n")
        for i in range(CEW_col_inst+3,CEW_col_inst+3+CNS_col_inst+1):
            f.write("Block_GateDecode.VINJ_b["+str(i)+"] += Block_GateSwitch.VINJ_T["+str(Cblock_row_inst+1+i)+"]\n")
            f.write("Block_GateDecode.GND_b["+str(i)+"] += Block_GateSwitch.GND_T["+str(Cblock_row_inst+1+i)+"]\n")
            f.write("Block_GateDecode.OUT["+str(i*2)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2)+"]\n")
            f.write("Block_GateDecode.OUT["+str(i*2+1)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2+1)+"]\n")
            #f.write("Block_GateDecode.RUN_OUT["+str(i*2)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2)+"]\n")
            #f.write("Block_GateDecode.RUN_OUT["+str(i*2+1)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2+1)+"]\n")
    else:
        for i in range(CEW_col_inst+2,CEW_col_inst+2+CNS_col_inst+1):
            f.write("Block_GateDecode.VINJ_b["+str(i)+"] += Block_GateSwitch.VINJ_T["+str(Cblock_row_inst+1+i)+"]\n")
            f.write("Block_GateDecode.GND_b["+str(i)+"] += Block_GateSwitch.GND_T["+str(Cblock_row_inst+1+i)+"]\n")
            f.write("Block_GateDecode.OUT["+str(i*2)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2)+"]\n")
            f.write("Block_GateDecode.OUT["+str(i*2+1)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2+1)+"]\n")
            #f.write("Block_GateDecode.RUN_OUT["+str(i*2)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2)+"]\n")
            #f.write("Block_GateDecode.RUN_OUT["+str(i*2+1)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2+1)+"]\n")
            
    for i in range(CEW_col-6,CEW_col-2):
        f.write("Block_GateSwitch.VPWR["+str(i)+"] += Block_GateDecode.RUN_OUT["+str(i)+"]\n")
    #for i in range((CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2-8,(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2-4)
    for i in range(4):
        f.write("Block_GateDecode.RUN_OUT["+str((CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2-8+i)+"] += Block_GateSwitch.VPWR["+str((CEW_col_inst+Cblock_row_inst+5+CNS_col_inst)*2-10+i)+"]\n")
            
    f.write("Block_DrainCutoff.PR += C_EW.Vd_Pl\n")
    f.write("Block_DrainCutoff.In += C_EW.Vd_Rl\n")
    
            
    '''for i in range(CEW_col_inst+1):
        f.write("Block_GateDecode.VINJ_b["+str(i)+"] += CABElements_GateSwitch.VINJ_T\n")
        f.write("Block_GateDecode.GND_b["+str(i)+"] += CABElements_GateSwitch.GND_T\n")
        f.write("Block_GateDecode.OUT["+str(i*2)+"] += Block_GateSwitch.decode["+str(i*2)+"]\n")
        f.write("Block_GateDecode.OUT["+str(i*2+1)+"] += Block_GateSwitch.decode["+str(i*2+1)+"]\n")
        f.write("Block_GateDecode.RUN_OUT["+str(i*2)+"] += Block_GateSwitch.VPWR["+str(i*2)+"]\n")
        f.write("Block_GateDecode.RUN_OUT["+str(i*2+1)+"] += Block_GateSwitch.VPWR["+str(i*2+1)+"]\n")
    if CNS_col_inst%2==1:
        f.write("Block_GateDecode.VINJ_b["+str(CEW_col_inst+2)+"] += CABElements_GateSwitch.VINJ_T\n")
        f.write("Block_GateDecode.GND_b["+str(CEW_col_inst+2)+"] += CABElements_GateSwitch.GND_T\n")
        f.write("Block_GateDecode.OUT["+str((CEW_col_inst+2)*2)+"] += Block_GateSwitch.decode["+str((CEW_col_inst+Cblock_row_inst+2)*2)+"]\n")
        f.write("Block_GateDecode.OUT["+str((CEW_col_inst+2)*2+1)+"] += Block_GateSwitch.decode["+str((CEW_col_inst+Cblock_row_inst+2)*2+1)+"]\n")
        f.write("Block_GateDecode.RUN_OUT["+str((CEW_col_inst+2)*2)+"] += Block_GateSwitch.VPWR["+str((CEW_col_inst+Cblock_row_inst+2)*2)+"]\n")
        f.write("Block_GateDecode.RUN_OUT["+str((CEW_col_inst+2)*2+1)+"] += Block_GateSwitch.VPWR["+str((CEW_col_inst+Cblock_row_inst+2)*2+1)+"]\n")
        for i in range(CEW_col_inst+3,CEW_col_inst+3+CNS_col_inst+1):
            f.write("Block_GateDecode.VINJ_b["+str(i)+"] += CABElements_GateSwitch.VINJ_T\n")
            f.write("Block_GateDecode.GND_b["+str(i)+"] += CABElements_GateSwitch.GND_T\n")
            f.write("Block_GateDecode.OUT["+str(i*2)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2)+"]\n")
            f.write("Block_GateDecode.OUT["+str(i*2+1)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2+1)+"]\n")
            f.write("Block_GateDecode.RUN_OUT["+str(i*2)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2)+"]\n")
            f.write("Block_GateDecode.RUN_OUT["+str(i*2+1)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2+1)+"]\n")
    else:
        for i in range(CEW_col_inst+2,CEW_col_inst+2+CNS_col_inst+1):
            f.write("Block_GateDecode.VINJ_b["+str(i)+"] += CABElements_GateSwitch.VINJ_T\n")
            f.write("Block_GateDecode.GND_b["+str(i)+"] += CABElements_GateSwitch.GND_T\n")
            f.write("Block_GateDecode.OUT["+str(i*2)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2)+"]\n")
            f.write("Block_GateDecode.OUT["+str(i*2+1)+"] += Block_GateSwitch.decode["+str((Cblock_row_inst+1+i)*2+1)+"]\n")
            f.write("Block_GateDecode.RUN_OUT["+str(i*2)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2)+"]\n")
            f.write("Block_GateDecode.RUN_OUT["+str(i*2+1)+"] += Block_GateSwitch.VPWR["+str((Cblock_row_inst+1+i)*2+1)+"]\n")'''
    
    #Volatile Switch
    f.write("\nVolSwitch.out += Amatrix.Vs_b[0:12]\n")
    f.write("VolSwitch.VINJ += Amatrix.VINJ_b[0:12]\n")
    f.write("VolSwitch.Vsel += Amatrix.Vsel_b[0:12]\n")
    f.write("VolSwitch.Vg += Amatrix.Vg_b[0:12]\n")
    f.write("VolSwitch.GND += Amatrix.GND_b[0:6]\n")
    f.write("VolSwitch.VTUN += Amatrix.VTUN_b[0:6]\n")
    f.write("VolSwitch.D += C_EW.Vs_b["+str((CEW_col_inst-1)*2)+"]\n")
    f.write("VolSwitch.CLK += C_EW.Vs_b["+str((CEW_col_inst-1)*2+1)+"]\n")
    f.write("VolSwitch.Q += C_NS.Vs_b["+str(CNS_col-5)+"]\n")
    if cab_output_num%2 ==1:
        f.write("VolSwitch.com += CAB_GateSwitch.Input["+str(Amatrix_col*2)+"]\n")
    else:
        f.write("VolSwitch.com += CAB_GateSwitch.Input["+str(Amatrix_col*2-1)+"]\n")
    f.write("CABElements_GateSwitch.VDD[1] += VolSwitch.VDD\n")
    f.write("VolSwitch.Vd_P += CAB_DrainSwitch.PR["+str((Amatrix_row+1)*4+3)+"]\n")
    for i in range(4):
        f.write("VolSwitch.Vd_in["+str(i)+"] += CAB_DrainSwitch.In["+str((Amatrix_row+1)*4+i)+"]\n")
        f.write("VolSwitch.Vd_in["+str(i+4)+"] += CAB_DrainSwitch.PR["+str((Amatrix_row+1)*4+i)+"]\n")
        f.write("VolSwitch.Vd_o["+str(i)+"] += Outmatrix.Vd_Rl["+str(i)+"]\n")
        f.write("VolSwitch.Vd_o["+str(i+4)+"] += Outmatrix.Vd_Pl["+str(i)+"]\n")
        
        
    #-------------------------------f.write("BtoOut.Vgrun_r += CAB_GateSwitch.Vgrun_r\n")
    #------------------------------------f.write("CABElements_GateSwitch.VDD[1] += BtoOut.AVDD_r\n")
    #------------------------------f.write("CABElements_GateSwitch.RUN += BtoOut.run_r\n")
    #-----------------------------------f.write("CABElements_GateSwitch.PROG += BtoOut.prog_r\n")
    f.write("CABElements_GateSwitch.VDD[1] += CAB_GateSwitch.AVDD_r\n")
    f.write("CABElements_GateSwitch.PROG += CAB_GateSwitch.prog_r\n")
    f.write("CABElements_GateSwitch.RUN += CAB_GateSwitch.run_r\n")
    f.write("CABElements_GateSwitch.prog_r += Block_Switch.Prog_b\n")
    f.write("Block_Switch.GND_b += CABElements_GateSwitch.GND_T\n")
    f.write("Block_Switch.VDD_b += CABElements_GateSwitch.VPWR[1]\n")
    f.write("Bswitch"+str(Bmatrix_row+1)+".GND_b += CABElements_GateSwitch.GND_T\n")
    f.write("Bswitch"+str(Bmatrix_row+1)+".VDD_b += CABElements_GateSwitch.VPWR[1]\n")
    f.write("Bswitch"+str(Bmatrix_row+1)+".Prog_b += CABElements_GateSwitch.PROG\n")
    f.write("Oswitch.GND_b += CABElements_GateSwitch.GND_T\n")
    f.write("Oswitch.VDD_b += CABElements_GateSwitch.VPWR[1]\n")
    f.write("Oswitch.Prog_b += CABElements_GateSwitch.PROG\n")
    f.write("CABElements_GateSwitch.RUN_IN[1] += CAB_GateSwitch.Vgrun_r\n")
    f.write("CABElements_GateSwitch.RUN_IN[0] += CAB_GateSwitch.Vgrun_r\n")
    for i in range(CEW_col+2):
        f.write("Block_GateSwitch.RUN_IN["+str(i)+"] += CAB_GateSwitch.Vgrun_r\n")
    f.write("Block_GateSwitch.RUN_IN["+str(CEW_col+2+Cblock_row_inst*2+2)+"] += CAB_GateSwitch.Vgrun_r\n")
    f.write("Block_GateSwitch.RUN_IN["+str(CEW_col+2+Cblock_row_inst*2+3)+"] += CAB_GateSwitch.Vgrun_r\n")
    for i in range(CEW_col+2+Cblock_row_inst*2+2+2+2,CEW_col+2+Cblock_row_inst*2+2+2+CNS_col+4):
        f.write("Block_GateSwitch.RUN_IN["+str(i)+"] += CAB_GateSwitch.Vgrun_r\n")
    
        
        
    #Frame
    f.write("\nouterFrame = frame(Top)\n")
    
    #N ports
    f.write('outerFrame.createPort("N","gateEN",connection = Block_GateDecode.ENABLE)\n')
    #--------------------------------------------------wait for pranav update on decoder IN-----------------------------------------------
    f.write('outerFrame.createPort("N","programdrain",connection = Block_DrainSelect.prog_drainrail)\n')
    f.write("Block_DrainSelect.prog_drainrail += CAB_DrainSelect.prog_drainrail\n")
    f.write('outerFrame.createPort("N","rundrain",connection = Block_DrainSelect.run_drainrail)\n')
    f.write("Block_DrainSelect.run_drainrail += CAB_DrainSelect.run_drainrail\n")
    f.write('outerFrame.createPort("N","cew0",connection = Block_GateDecode.VGRUN['+str(CEW_col-6)+'])\n')
    f.write('outerFrame.createPort("N","cew1",connection = Block_GateDecode.VGRUN['+str(CEW_col-5)+'])\n')
    f.write('outerFrame.createPort("N","cew2",connection = Block_GateDecode.VGRUN['+str(CEW_col-4)+'])\n')
    f.write('outerFrame.createPort("N","cew3",connection = Block_GateDecode.VGRUN['+str(CEW_col-3)+'])\n')
    f.write('outerFrame.createPort("N","vtun",connection = Block_GateSwitch.VTUN_T[0])\n')
    f.write('VINJN = outerFrame.createPort("N","vinj",dimension=3)\n')
    f.write('VINJN[0] += Block_GateDecode.VINJV\n')
    f.write('VINJN[1] += Block_DrainSelect.VINJ\n')
    f.write('Block_DrainSelect.VINJ += Block_DrainCutoff.VDD\n')
    f.write('VINJN[2] += CABElements_GateSwitch.VINJ_T\n')
    f.write('GNDN = outerFrame.createPort("N","gnd",dimension=3)\n')
    f.write('GNDN[0] += Block_GateDecode.GNDV\n')
    f.write('GNDN[1] += Block_DrainSelect.GND\n')
    f.write('Block_DrainSelect.GND += Block_DrainCutoff.GND\n')
    f.write('GNDN[2] += CABElements_GateSwitch.GND_T\n')
    f.write('outerFrame.createPort("N","avdd",connection = CAB_GateSwitch.Input[0])\n')
    for i in range(Cblock_row_inst-1):
        f.write('outerFrame.createPort("N","s'+str(i*4)+'",connection = SpaceUp_'+str(i)+'.n[0])\n')
        f.write('outerFrame.createPort("N","s'+str(i*4+1)+'",connection = SpaceUp_'+str(i)+'.n[1])\n')
        f.write('outerFrame.createPort("N","s'+str(i*4+2)+'",connection = SpaceUp_'+str(i)+'.n[2])\n')
        f.write('outerFrame.createPort("N","s'+str(i*4+3)+'",connection = SpaceUp_'+str(i)+'.n[3])\n')
    f.write('outerFrame.createPort("N","s'+str(Cblock_row_inst*4-4)+'",connection = Conn_'+str(Cblock_row_inst-1)+'.n[0])\n')
    f.write('outerFrame.createPort("N","s'+str(Cblock_row_inst*4-3)+'",connection = Conn_'+str(Cblock_row_inst-1)+'.n[1])\n')
    f.write('outerFrame.createPort("N","s'+str(Cblock_row_inst*4-2)+'",connection = Conn_'+str(Cblock_row_inst-1)+'.n[2])\n')
    f.write('outerFrame.createPort("N","s'+str(Cblock_row_inst*4-1)+'",connection = Conn_'+str(Cblock_row_inst-1)+'.n[3])\n')
    f.write('outerFrame.createPort("N","prog",connection = CABElements_GateSwitch.prog_r)\n')
    f.write('CABElements_GateSwitch.prog_r += Block_Switch.Prog\n')
    f.write('outerFrame.createPort("N","run",connection = Block_GateSwitch.RUN)\n')
    f.write('Block_GateSwitch.RUN += Block_DrainCutoff.RUN\n')
    f.write('Block_GateSwitch.RUN += CAB_GateSwitch.run\n')
    f.write('CAB_GateSwitch.run += CAB_DrainSwitch.RUN\n')
    f.write('outerFrame.createPort("N","vgsel",connection = CABElements_GateSwitch.Vgsel)\n')
    f.write("CABElements_GateSwitch.Vgsel += Block_GateSwitch.vgsel_r\n")
    
    #S ports
    f.write('outerFrame.createPort("S","gateEN",connection = Block_GateDecode.ENABLE)\n')
    #--------------------------------------------------wait for pranav update on decoder IN-----------------------------------------------
    
    f.write('outerFrame.createPort("S","programdrain",connection = Block_DrainSelect.prog_drainrail)\n')
    f.write('outerFrame.createPort("S","rundrain",connection = Block_DrainSelect.run_drainrail)\n')
    for i in range(4):
        f.write('outerFrame.createPort("S","cew'+str(i)+'",connection = Oswitch.A['+str(i)+'])\n')
    f.write('outerFrame.createPort("S","vtun",connection = Block_GateSwitch.VTUN_T[0])\n')
    f.write('VINJS = outerFrame.createPort("S","vinj",dimension=3)\n')
    f.write('VINJS[0] += Block_GateDecode.VINJV\n')
    f.write('VINJS[1] += Block_DrainSelect.VINJ\n')
    f.write('VINJS[2] += CABElements_GateSwitch.VINJ_T\n')
    f.write('GNDS = outerFrame.createPort("S","gnd",dimension=3)\n')
    f.write('GNDS[0] += Block_GateDecode.GNDV\n')
    f.write('GNDS[1] += Block_DrainSelect.GND\n')
    f.write('GNDS[2] += CABElements_GateSwitch.GND_T\n')
    f.write('outerFrame.createPort("S","avdd",connection = CAB_GateSwitch.Input[0])\n')
    f.write('outerFrame.createPort("S","s'+str(0)+'",connection = Conn_'+str(0)+'.s[0])\n')
    f.write('outerFrame.createPort("S","s'+str(1)+'",connection = Conn_'+str(0)+'.s[1])\n')
    f.write('outerFrame.createPort("S","s'+str(2)+'",connection = Conn_'+str(0)+'.s[2])\n')
    f.write('outerFrame.createPort("S","s'+str(3)+'",connection = Conn_'+str(0)+'.s[3])\n')
    for i in range(1,Cblock_row_inst):
        f.write('outerFrame.createPort("S","s'+str(i*4)+'",connection = SpaceDown_'+str(i)+'.s[0])\n')
        f.write('outerFrame.createPort("S","s'+str(i*4+1)+'",connection = SpaceDown_'+str(i)+'.s[1])\n')
        f.write('outerFrame.createPort("S","s'+str(i*4+2)+'",connection = SpaceDown_'+str(i)+'.s[2])\n')
        f.write('outerFrame.createPort("S","s'+str(i*4+3)+'",connection = SpaceDown_'+str(i)+'.s[3])\n')
    f.write('outerFrame.createPort("S","prog",connection = CABElements_GateSwitch.prog_r)\n')
    f.write('outerFrame.createPort("S","run",connection = Block_GateSwitch.RUN)\n')
    f.write('outerFrame.createPort("S","vgsel",connection = CABElements_GateSwitch.Vgsel)\n')
        
    #W ports
    for i in range(4):
        f.write('outerFrame.createPort("W","cns'+str(i)+'",connection = Oswitch.A['+str(i+4)+'])\n')
    f.write('outerFrame.createPort("W","vgrun",connection = CABElements_GateSwitch.RUN_IN[0])\n')
    f.write('outerFrame.createPort("W","vtun",connection = Block_GateSwitch.VTUN_T[0])\n')
    f.write('outerFrame.createPort("W","vinj",connection = CABElements_GateSwitch.VINJ_T)\n')
    f.write('outerFrame.createPort("W","gnd",connection = CABElements_GateSwitch.GND_T)\n')
    f.write('outerFrame.createPort("W","avdd",connection = CABElements_GateSwitch.VDD[1])\n')
    for i in range(C_drain_bit):
        f.write('outerFrame.createPort("W","drainbit'+str(C_drain_bit-1-i)+'",connection = Block_DrainDecode.IN['+str(C_drain_bit-1-i)+'])\n')
    for i in range(Cblock_row):
        f.write('outerFrame.createPort("W","s'+str(i)+'",connection = Block_DrainCutoff.In['+str(i)+'])\n')
    for i in range(C_gate_bit):
        f.write('outerFrame.createPort("W","drainbit'+str(C_gate_bit+C_drain_bit-1-i)+'",connection = CAB_DrainDecoder.IN['+str(C_gate_bit-1-i)+'])\n')
    f.write('outerFrame.createPort("W","drainEN",connection = CAB_DrainDecoder.ENABLE)\n')
    
    
    
    #E ports
    f.write('outerFrame.createPort("E","cns0",connection = Block_GateDecode.VGRUN['+str((CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2-8)+'])\n')
    f.write('outerFrame.createPort("E","cns1",connection = Block_GateDecode.VGRUN['+str((CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2-7)+'])\n')
    f.write('outerFrame.createPort("E","cns2",connection = Block_GateDecode.VGRUN['+str((CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2-6)+'])\n')
    f.write('outerFrame.createPort("E","cns3",connection = Block_GateDecode.VGRUN['+str((CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2-5)+'])\n')
    f.write('outerFrame.createPort("E","vgrun",connection = CABElements_GateSwitch.RUN_IN[0])\n')
    f.write('outerFrame.createPort("E","vtun",connection = Block_GateSwitch.VTUN_T[0])\n')
    f.write('outerFrame.createPort("E","vinj",connection = CABElements_GateSwitch.VINJ_T)\n')
    f.write('outerFrame.createPort("E","gnd",connection = CABElements_GateSwitch.GND_T)\n')
    f.write('outerFrame.createPort("E","avdd",connection = CABElements_GateSwitch.VDD[1])\n')
    for i in range(C_drain_bit):
        f.write('outerFrame.createPort("E","drainbit'+str(C_drain_bit-1-i)+'",connection = Block_DrainDecode.IN['+str(C_drain_bit-1-i)+'])\n')
    for i in range(Cblock_row):
        f.write('outerFrame.createPort("E","s'+str(i)+'",connection = Block_Switch.A['+str(i)+'])\n')
    for i in range(C_gate_bit):
        f.write('outerFrame.createPort("E","drainbit'+str(C_gate_bit+C_drain_bit-1-i)+'",connection = CAB_DrainDecoder.IN['+str(C_gate_bit-1-i)+'])\n')
    f.write('outerFrame.createPort("E","drainEN",connection = CAB_DrainDecoder.ENABLE)\n')
    f.write('CAB_DrainDecoder.ENABLE += Block_DrainDecode.ENABLE\n')
    
    f.write("\n# Compilation\n")
    f.write("design_limits = [1e6, 6.1e5]\n")
    f.write("location_islands = ((20600, 363500), (20600, 20000), (162500,20000))\n")
    f.write('compile_asic(Top,process="TSMC350nm",fileName="'+cab+'",p_and_r = True,design_limits = design_limits, location_islands = location_islands)\n')
    
    
    f.close()
    
    with open('cab.py',"r") as temp:
        content = temp.readlines()
        
    final = open(cab+'.py',"w")
    for line in content:
        if line[0]=="4" and "+= 4" in line:
            new_line = line.replace("+= 4","+= ")
            final.write(new_line[1:])
        elif line[0]=="4":
            final.write(line[1:])
        elif "+= 4" in line:
            final.write(line.replace("+= 4","+= "))
        else:
            final.write(line)
    
    final.close()
    os.remove('cab.py')
    
        

