import json
import math
import os

with open('cell2cell_350nm.json','r') as file:
    data = json.load(file)
    
with open('analog_std_cells.json','r') as lib:
    lib = json.load(lib)
    
f = open('full_cab_python_temp.py','w')



for general_info in data:
    foundry=data["foundry"]
    process_node=data["process_node"]
    block_list=data["cab"]
    if "cab2" in data:
        block_list2=data["cab2"]
        
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
Cblock_row = data["Cblock_rows"]
CEW_col = data["CEW_cols"]
CNS_col = data["CNS_cols"]
Cblock_row_inst = int(Cblock_row/4)
CEW_col_inst = int(CEW_col/2)
CNS_col_inst = int(CNS_col/2)
   
Amatrix_row = len(data["cab"])
Amatrix_col = data["Amatrix_cols"]
Bmatrix_row = len(data["cab"])-1
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
    f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=6)\n")
elif 16<(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2<33:
    f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=5)\n")
elif 64<(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2<129:
    f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=7)\n")
elif 8<(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst-Cblock_row_inst-2)*2<17:
    f.write("Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=4)\n")
    
f.write("Block_GateSwitch = STD_IndirectGateSwitch(Top,island=BlockIsland,num="+str(CEW_col_inst+Cblock_row_inst+5+CNS_col_inst)+")\n\n")

if 16<Cblock_row_inst*4<33:
    f.write("Block_DrainDecode = STD_DrainDecoder(Top,island=BlockIsland,bits=5)\n")
    f.write("Block_DrainSelect = RunDrainSwitch(Top,island=BlockIsland,num="+str(Cblock_row_inst)+")\n")
    f.write("Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num="+str(Cblock_row_inst)+")\n")
elif 32<Cblock_row_inst*4<65:
    f.write("Block_DrainDecode = STD_DrainDecoder(Top,island=BlockIsland,bits=6)\n")
    f.write("Block_DrainSelect = RunDrainSwitch(Top,island=BlockIsland,num="+str(Cblock_row_inst)+")\n")
    f.write("Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num="+str(Cblock_row_inst)+")\n") 
elif 8<Cblock_row_inst*4<17:
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
    f.write("CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=6)\n")
    f.write("CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n")
    f.write("CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n\n")
elif 16<(Bmatrix_row+6)*4<33:
    f.write("CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=5)\n")
    f.write("CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n")
    f.write("CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num="+str(Bmatrix_row+6)+")\n\n")
elif 64<(Bmatrix_row+6)*4<129:
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
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B[0:2]\n")
                        elif top_port == "Vsel":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B[0]\n")
                        elif top_port == "VINJ":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VINJ\n")
                        elif top_port == "RUN":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.run_r\n")
                        elif top_port == "Vg[0:1]" or top_port == "VG[0:1]":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.Vg[0:2]\n")
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
                                    f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b[0:2]\n")
                                else:
                                    f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0:1]\n")
                            else:
                                if "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b[0:2]\n")
                                else:
                                    f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0:1]\n")
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
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".Vg += CABElements_GateSwitch.Vg[0:1]\n")
                            else:
                                if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".Vg += CABElements_GateSwitch.Vg[0:1]\n")
                        elif top_port == "VG[0:1]":
                            if block_list[block_list.index(block)-1][-1].isnumeric():
                                if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".VG += CABElements_GateSwitch.Vg[0:1]\n")
                            else:
                                if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".VG += CABElements_GateSwitch.Vg[0:1]\n")
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
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B[0:2]\n")
                        elif top_port == "Vsel":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.CTRL_B[0]\n")
                        elif top_port == "VINJ":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.VINJ\n")
                        elif top_port == "RUN":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.run_r\n")
                        elif top_port == "Vg[0:1]" or top_port == "VG[0:1]":
                            f.write(block+"."+top_port.split("[")[0]+" += CABElements_GateSwitch.Vg[0:2]\n")
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
                                    f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b[0:2]\n")
                                else:
                                    f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0:2]\n")
                            else:
                                if "Vsel_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vsel += "+block_list[block_list.index(block)-1]+".Vsel_b[0:2]\n")
                                else:
                                    f.write(block+".Vsel += CABElements_GateSwitch.CTRL_B[0:2]\n")
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
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".Vg += CABElements_GateSwitch.Vg[0:2]\n")
                            else:
                                if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".Vg += CABElements_GateSwitch.Vg[0:2]\n")
                        elif top_port == "VG[0:1]":
                            if block_list[block_list.index(block)-1][-1].isnumeric():
                                if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1].split("__")[0]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".VG += CABElements_GateSwitch.Vg[0:2]\n")
                            else:
                                if "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".Vg_b[0:2]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".VG += "+block_list[block_list.index(block)-1]+".VG_b[0:2]\n")
                                else:
                                    f.write(block+".VG += CABElements_GateSwitch.Vg[0:2]\n")
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
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b\n")
                                elif "VG_b" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b\n")
                                elif "Vg_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".Vg_b[0]\n")
                                elif "VG_b[0:1]" in lib[block_list[block_list.index(block)-1]]["S"]:
                                    f.write(block+".Vg += "+block_list[block_list.index(block)-1]+".VG_b[0]\n")
                                else:
                                    f.write(block+".Vg += CABElements_GateSwitch.Vg[0]\n")
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
f.write("C_EW.GND_b[0] += CAB_GateSwitch.Input[1]\n")
f.write("CAB_GateSwitch.Input[0] += CABElements_GateSwitch.VDD[1]\n")








f.write("# Compilation\n")
f.write("design_limits = [1e6, 6.1e5]\n")
f.write("location_islands = ((20600, 363500), (20600, 20000), (160000,20000))\n")
f.write('compile_asic(Top,process="TSMC350nm",fileName="full_cab_python",p_and_r = True,design_limits = design_limits, location_islands = location_islands)\n')











































f.close()

with open('full_cab_python_temp.py',"r") as temp:
    content = temp.readlines()
    
final = open('full_cab_python.py',"w")
for line in content:
    if line[0]=="4":
        final.write(line[1:])
    elif "+= 4" in line:
        final.write(line.replace("+= 4","+= "))
    else:
        final.write(line)

final.close()
os.remove('full_cab_python_temp.py')
    
        

