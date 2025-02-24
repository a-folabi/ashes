import os
import numpy as np

def compile(project_name, board_type, chip_num):

	path = os.path.join("/home/ubuntu/ashes/",project_name)
	extension = ".swcs"
	
	if      board_type == '3.0a': brdtype = '_30a';
	elif board_type == '3.0n': brdtype = '_30n';
	elif board_type == '3.0h': brdtype = '_30h';
	elif board_type == '':     brdtype = '';
	else:                         
		print("Please select the FPAA board that you are using. \nNo Selected FPAA Board \nerror")
		exit()
	print(path)
	
	os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/chip_para/chip_para_debug.asm {path}/chip_para_debug.asm");
	os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/chip_para/chip_para_TR_chip{chip_num}{brdtype}.asm {path}/chip_para_TR.asm");
	os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/chip_para/chip_para_SP_chip{chip_num}{brdtype}.asm {path}/chip_para_SP.asm");
	os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/chip_para/chip_para_RI_chip{chip_num}{brdtype}.asm {path}/chip_para_RI.asm");
	os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/chip_para/chip_para_CP_chip{chip_num}{brdtype}.asm {path}/chip_para_CP.asm");
	os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/chip_para/chip_para_FP_chip{chip_num}{brdtype}.asm {path}/chip_para_FP.asm");
	os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/Vd_table/Vd_table_30mV_chip{chip_num}{brdtype} {path}/Vd_table_30mV");
	
	#//exec("~/rasp30/prog_assembly/libs/scilab_code/characterization/char_diodeADC.sce",-1);
	
	
	zip_list = ' ';

	#########################################
	## Make programm reverse program files ##
	#########################################
	os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh tunnel_revtun_SWC_CAB ~/rasp30/prog_assembly/libs/asm_code/tunnel_revtun_SWC_CAB_ver00.s43 16384 16384 16384 {path}")
	zip_list = zip_list + "tunnel_revtun_SWC_CAB.elf ";
	
	###############################
	## Make switch program files ##
	###############################
	switch_list_temp = np.loadtxt(f"{path}/{project_name}.swcs");
	#print (switch_list_temp)
	
	## Make switch list (dec) which includes the information how many switches are. 
	n = len(switch_list_temp)
	switch_list=[]
	for i in range(n):
	    if switch_list_temp[i][3] == 0: 
	    	switch_list.append([switch_list_temp[i][0],switch_list_temp[i][1],switch_list_temp[i][2]]); 
	np.savetxt(f"{path}/switch_list", switch_list, "%5.15f", ' ')

	
	# Make switch info (hex) which will be uploaed to the sram. 
	n=len(switch_list)

	temp = f"0x{n:04x} "
	for i in range(n):
		if switch_list[i][2] == 2:
			temp = temp + f"0x{int(switch_list[i][0]):04x} " + f"0x{int(switch_list[i][1]):04x} " + f"0x{0:04x} "
		else:
			temp = temp + f"0x{int(switch_list[i][0]):04x} " + f"0x{int(switch_list[i][1]):04x} " + f"0x{int(switch_list[i][2]):04x} "
	
	fd = open(f"{path}/switch_info", "w") 
	fd.write(temp)
	fd.close()
	
	
	os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh switch_program ~/rasp30/prog_assembly/libs/asm_code/switch_program_ver04.s43 16384 16384 16384 {path}")
	zip_list = zip_list + "switch_program.elf "
	
	hid_dir = f"{path}/hid_dir"
	if not os.path.isdir(hid_dir):
		os.mkdir(hid_dir)
	
	
	
	os.system(f"rm {path}/{hid_dir}/switch_list_ble") 
	os.system(f"rm {path}/{hid_dir}/switch_info_ble")
	# Make switch list (dec) for ble switches.
	n = len(switch_list_temp)
	switch_list_ble=[]
	for i in range(n):
	    if switch_list_temp[i][3] == 0 and switch_list_temp[i][2] == 2: 
	    	switch_list_ble.append([switch_list_temp[i][0],switch_list_temp[i][1],switch_list_temp[i][2]])

	
	# Make switch info for ble (hex) which will be uploaed to the sram. 
	n = len(switch_list_ble)
	temp = f"0x{n:04x} "
	for i in range(n):
	    temp = temp + f"0x{int(switch_list_ble[i][0]):04x} " + f"0x{int(switch_list_ble[i][1]):04x} " + f"0x{int(switch_list_ble[i][2]):04x} "


	if switch_list_ble:
	#maybe add the {hid_dir} to the path
	    np.savetxt(f"{path}/switch_list_ble", switch_list_ble, "%5.15f", ' ')
	    fd = open(f"{path}/switch_info_ble", "w") 
	    fd.write(temp)
	    fd.close()
	    os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh tunnel_clb ~/rasp30/prog_assembly/libs/asm_code/tunnel_revtun_CLB_ver00.s43 16384 16384 16384 {path}")
	    os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh switch_program_ble ~/rasp30/prog_assembly/libs/asm_code/switch_program_ble_ver00.s43 16384 16384 16384 {path}")
	    os.system(f"mv switch_list_ble switch_info_ble {hid_dir}");
	

	
	###############################
	## Make target program files ##
	###############################
	target_list = np.loadtxt(f"{path}/{project_name}.swcs");
	#print(target_list)
	
	n = len(target_list)
	print(n)
	for i in range(n):
	    if target_list[i][3] == 0:
	    	target_list[i][2] = 100e-09 # 100nA doesn't mean anything. I just put it since switches with 0 caused error. 
	print(target_list)
	
	# Mismatch map compensation
	b1 = os.system(f"ls ~/rasp30/prog_assembly/libs/chip_parameters/mismatch_map/mismatch_map_chip{chip_num}{brdtype}")
	
	if b1 == 0: # 0 if no error occurred, 1 if error.
		mismatch_map = np.loadtxt(fname = f"/home/ubuntu/rasp30/prog_assembly/libs/chip_parameters/mismatch_map/mismatch_map_chip{chip_num}{brdtype}", delimiter = ',', ndmin = 2)
		#print(mismatch_map)
		
		r_size_mmap = len(mismatch_map)
		#print(r_size_mmap)
		
		for i in range(n):
			if target_list[i][3] != 0:   # Switch programming:0 , Target programming:1 ~ 6
				for j in range(r_size_mmap):
					if target_list[i][0] == mismatch_map[j][0]:
						if target_list[i][1] == mismatch_map[j][1]:
								target_list[i][2] = diodeADC_v2i(diodeADC_i2v(target_list[i][2],chip_num,brdtype) + mismatch_map[j][2],chip_num,brdtype)
		np.savetxt(f"{path}/mismatch_mapped_swc_list", switch_list_ble, "%5.15f", ' ')
	
	
	k=1; 
	mmap_cal_list=[]; # Mismatch map calibration list.
	for i in range(n):
		if target_list[i][3] == 11 or target_list[i][3] == 12 or target_list[i][3] == 13 or target_list[i][3] == 14 or target_list[i][3] == 15: # Generate calibration list.
			mmap_cal_list.append(target_list[i])
			target_list[i][3].append(target_list[i][3]-10)
			k=k+1;
	
	if mmap_cal_list:
		np.savetxt(f"{path}/mmap_cal_list", mmap_cal_list, "%5.15f", ' ')
		print(mmap_cal_list)

	target_list_copy = np.array(target_list).copy()

	#ADC_Current_copy = ADC_Current;
	temp_size = len(target_list);
	#temp_size2=size(ADC_Current_copy); n2=temp_size2(1,1);
	kappa_constant = 30; # relationship of target current between subVt and lowsubVt range.
	
	
	for i in range(n):
		if target_list_copy[i][2] < 1*10**(-9):
			target_list_copy[i][2] = target_list_copy[i][2]*kappa_constant
		if target_list_copy[i][2] > 10*10**(-6):
			target_list_copy[i][2] = target_list_copy[i][2]/kappa_constant
	#print(target_list_copy)
	
	#disp(target_list_copy)

	#for i=1:n
	#    if target_list(i,4) ~= 0 then   // Switch programming:0 , Target programming:1 ~ 6
	#        ADC_Current_copy(:,3)=abs(ADC_Current_copy(:,2)-target_list_copy(i,3));
	#        min_value = min(ADC_Current_copy(:,3));
	#        for j=1:n2
	#            if ADC_Current_copy(j,3) == min_value then
	#                target_list(i,5) = ADC_Current_copy(j,1);
	#            end
	#        end
	#    end
	#end
	
	
	
	target_listArray = np.array(target_list)
	
	target_list_copyArray = np.array(target_list_copy)
	temp_array1 = np.array(diodeADC_v2h(diodeADC_i2v(target_list_copyArray[:,2],chip_num,brdtype),chip_num,brdtype))
	temp_array2 = np.concatenate((target_listArray, temp_array1.reshape(-1, 1)), axis = 1)
	target_listArray = temp_array2
	#print(target_listArray);
	
	
	temp2_tunnel_revtun=' '; 
	temp2_highaboveVt_swc=' '
	temp2_highaboveVt_ota=' '
	temp2_aboveVt_swc=' '; temp2_aboveVt_ota=' '; temp2_aboveVt_otaref=' '; temp2_aboveVt_mite=' '; temp2_aboveVt_dirswc=' ';
	temp2_subVt_swc=' '; temp2_subVt_ota=' '; temp2_subVt_otaref=' '; temp2_subVt_mite=' '; temp2_subVt_dirswc=' ';
	temp2_lowsubVt_swc=' ';temp2_lowsubVt_ota=' ';temp2_lowsubVt_otaref=' ';temp2_lowsubVt_mite=' ';temp2_lowsubVt_dirswc=' ';
	n_target_tunnel_revtun=0;
	n_target_highaboveVt_swc=0;n_target_highaboveVt_ota=0;
	n_target_aboveVt_swc=0;n_target_aboveVt_ota=0;n_target_aboveVt_otaref=0;n_target_aboveVt_mite=0;n_target_aboveVt_dirswc=0;
	n_target_subVt_swc=0;n_target_subVt_ota=0;n_target_subVt_otaref=0;n_target_subVt_mite=0;n_target_subVt_dirswc=0;
	n_target_lowsubVt_swc=0;n_target_lowsubVt_ota=0;n_target_lowsubVt_otaref=0;n_target_lowsubVt_mite=0;n_target_lowsubVt_dirswc=0;
	target_l_highaboveVt_swc=np.empty(shape=(2, 3));target_l_highaboveVt_ota=np.empty(shape=(2, 3));
	target_l_aboveVt_swc=np.empty(shape=(2, 3));target_l_aboveVt_ota=np.empty(shape=(2, 3));target_l_aboveVt_otaref=np.empty(shape=(2, 3));target_l_aboveVt_mite=np.empty(shape=(2, 3));target_l_aboveVt_dirswc=np.empty(shape=(2, 3));
	target_l_subVt_swc=np.empty(shape=(2, 3));target_l_subVt_ota=np.empty(shape=(2, 3));target_l_subVt_otaref=np.empty(shape=(2, 3));target_l_subVt_mite=np.empty(shape=(2, 3));target_l_subVt_dirswc=np.empty(shape=(2, 3));
	target_l_lowsubVt_swc=np.empty(shape=(2, 3));target_l_lowsubVt_ota=np.empty(shape=(2, 3));target_l_lowsubVt_otaref=np.empty(shape=(2, 3));target_l_lowsubVt_mite=np.empty(shape=(2, 3));target_l_lowsubVt_dirswc=np.empty(shape=(2, 3));
	print(n)
	print(target_listArray)
	
	for i in range(n):
		# Switch programming <0>, Target programming <1> 
		# 1:Switch FGs, 2:OTA_ref FGs(Bias), 3:OTA FGs, 4:MITE, 5:BLE, 6:Direct SWC FGs
		if target_listArray[i][3] == 1 or target_listArray[i][3] == 5:
			if target_listArray[i][2] > 10E-6:
				temp2_highaboveVt_swc = temp2_highaboveVt_swc + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000 " + "0xffff " + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_highaboveVt_swc = np.append(target_l_highaboveVt_swc, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_highaboveVt_swc=n_target_highaboveVt_swc+1
		
			if target_listArray[i][2] <= 10E-6 and target_listArray[i][2] > 1E-7:
				temp2_aboveVt_swc = temp2_aboveVt_swc + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000 " + "0xffff " + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_aboveVt_swc = np.append(target_l_aboveVt_swc, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_aboveVt_swc=n_target_aboveVt_swc+1

			if target_listArray[i][2] <= 1E-7 and target_listArray[i][2] >= 1E-9:
				temp2_subVt_swc = temp2_subVt_swc + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_subVt_swc = np.append(target_l_subVt_swc, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_subVt_swc=n_target_subVt_swc+1
		    		
			if target_listArray[i][2] < 1E-9:
				temp2_lowsubVt_swc = temp2_lowsubVt_swc + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff " + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_lowsubVt_swc = np.append(target_l_lowsubVt_swc, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_lowsubVt_swc = n_target_lowsubVt_swc+1
		if target_listArray[i][3] == 3:
			if target_listArray[i][2] > 10E-6:
				temp2_highaboveVt_ota = temp2_highaboveVt_ota + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_highaboveVt_ota = np.append(target_l_highaboveVt_ota, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_highaboveVt_ota = n_target_highaboveVt_ota + 1

			if target_listArray[i][2] <= 10E-6 and target_listArray[i][2] > 1E-7:
				temp2_aboveVt_ota = temp2_aboveVt_ota + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_aboveVt_ota = np.append(target_l_aboveVt_ota, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_aboveVt_ota = n_target_aboveVt_ota + 1

			if target_listArray[i][2] <= 1E-7 and target_listArray[i][2] >= 1E-9:
				temp2_subVt_ota = temp2_subVt_ota + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_subVt_ota = np.append(target_l_subVt_ota, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_subVt_ota = n_target_subVt_ota+1
		    
			if target_listArray[i][2] < 1E-9:
				temp2_lowsubVt_ota = temp2_lowsubVt_ota + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_lowsubVt_ota = np.append(target_l_lowsubVt_ota, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_lowsubVt_ota= n_target_lowsubVt_ota+1
		if target_listArray[i][3] == 2:
			if target_listArray[i][2] > 1E-7:
				temp2_aboveVt_otaref = temp2_aboveVt_otaref + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_aboveVt_otaref = np.append(target_l_aboveVt_otaref, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0)
				n_target_aboveVt_otaref=n_target_aboveVt_otaref+1
			if target_listArray[i][2] <= 1E-7 and target_listArray[i][2] >= 1E-9:
				temp2_subVt_otaref = temp2_subVt_otaref + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_subVt_otaref = np.append(target_l_subVt_otaref, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_subVt_otaref = n_target_subVt_otaref +1
		    
			if target_listArray[i][2] < 1E-9:
				temp2_lowsubVt_otaref = temp2_lowsubVt_otaref + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_lowsubVt_otaref = np.append(target_l_lowsubVt_otaref, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_lowsubVt_otaref = n_target_lowsubVt_otaref + 1
			
		if target_listArray[i][3] == 4:
			if target_listArray[i][2] > 1E-7:
				temp2_aboveVt_mite = temp2_aboveVt_mite + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_aboveVt_mite = np.append(target_l_aboveVt_mite, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_aboveVt_mite = n_target_aboveVt_mite +1
				
			if target_listArray[i][2] <= 1E-7 and target_listArray[i][2] >= 1E-9:
				temp2_subVt_mite = temp2_subVt_mite + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				#target_l_subVt_mite[n_target_subVt_mite] = [target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]];
				target_l_subVt_mite = np.append(target_l_subVt_mite, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_subVt_mite = n_target_subVt_mite +1
			if target_listArray[i][2] < 1E-9:
				temp2_lowsubVt_mite = temp2_lowsubVt_mite + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				#target_l_lowsubVt_mite[n_target_lowsubVt_mite] = [target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]];
				target_l_lowsubVt_mite = np.append(target_l_lowsubVt_mite, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_lowsubVt_mite = n_target_lowsubVt_mite +1
		if target_listArray[i][3] == 6:
			if target_listArray[i][2] > 1E-7:
				temp2_aboveVt_dirswc = temp2_aboveVt_dirswc + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				target_l_aboveVt_dirswc = np.append(target_l_aboveVt_dirswc, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_aboveVt_dirswc = n_target_aboveVt_dirswc + 1

			if target_listArray[i][2] <= 1E-7 and target_listArray[i][2] >= 1E-9:
				temp2_subVt_dirswc = temp2_subVt_dirswc + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				#target_l_subVt_dirswc[n_target_subVt_dirswc] = [target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]];
				target_l_subVt_dirswc = np.append(target_l_subVt_dirswc, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_subVt_dirswc = n_target_subVt_dirswc + 1
			if target_listArray[i][2] < 1E-9:
				temp2_lowsubVt_dirswc = temp2_lowsubVt_dirswc + f"0x{(int(target_listArray[i][0])):04x}" + f"0x{(int(target_listArray[i][1])):04x}"  + f"0x{(int(target_listArray[i][4])):04x}" + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
				#target_l_lowsubVt_dirswc[n_target_lowsubVt_dirswc] = [target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]];
				target_l_lowsubVt_dirswc = np.append(target_l_lowsubVt_dirswc, np.array([[target_listArray[i][0], target_listArray[i][1], target_listArray[i][2]]]), axis=0);
				n_target_lowsubVt_dirswc = n_target_lowsubVt_dirswc + 1
		if target_listArray[i][3] != 0:
			temp2_tunnel_revtun = temp2_tunnel_revtun + f"0x{(int(target_listArray[i][0])):04x} " + f"0x{(int(target_listArray[i][1])):04x} "  + f"0x{(int(target_listArray[i][4])):04x} " + "0x0000" + " 0xffff" + " "; # Row, Col, target, diff, # of pulses (Start values should be 0xffff. 0x0000 means the coarse program is over)
			n_target_tunnel_revtun=n_target_tunnel_revtun+1;



	target_list_info=[n_target_tunnel_revtun,n_target_highaboveVt_swc,n_target_highaboveVt_ota,n_target_aboveVt_swc,n_target_aboveVt_ota,n_target_aboveVt_otaref,n_target_aboveVt_mite,n_target_aboveVt_dirswc,n_target_subVt_swc,n_target_subVt_ota,n_target_subVt_otaref,n_target_subVt_mite,n_target_subVt_dirswc,n_target_lowsubVt_swc,n_target_lowsubVt_ota,n_target_lowsubVt_otaref,n_target_lowsubVt_mite,n_target_lowsubVt_dirswc,kappa_constant]
	#print(n_target_tunnel_revtun)
	np.savetxt(f"{path}/target_list", target_list_info, "%5.15f", ' ')

	if n_target_tunnel_revtun != 0:
		temp1 = f"0x{(n_target_tunnel_revtun):04x}"
		temp = temp1 + temp2_tunnel_revtun;
		fd = open(f"{path}/target_info_tunnel_revtun", "w") 
		fd.write(temp)
		fd.close()
		zip_list = zip_list + "target_list Vd_table_30mV ";

	#print(n_target_highaboveVt_swc)
	if n_target_highaboveVt_swc != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_swc_chip{chip_num}{brdtype} {path}/pulse_width_table_swc");
		np.savetxt(f"{path}/target_list_highaboveVt_swc", target_l_highaboveVt_swc, "%5.15f", ' ')
		temp1 = f"0x{(n_target_highaboveVt_swc):04x}"
		temp = temp1 + temp2_highaboveVt_swc; 
		fd = open(f"{path}/target_info_highaboveVt_swc", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_highaboveVt_SWC ~/rasp30/prog_assembly/libs/asm_code/recover_inject_highaboveVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_highaboveVt_SWC ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_highaboveVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_highaboveVt_SWC ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_highaboveVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_highaboveVt_m_ave_04_SWC ~/rasp30/prog_assembly/libs/asm_code/fine_program_highaboveVt_m_ave_04_SWC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_highaboveVt_swc pulse_width_table_swc recover_inject_highaboveVt_SWC.elf first_coarse_program_highaboveVt_SWC.elf measured_coarse_program_highaboveVt_SWC.elf fine_program_highaboveVt_m_ave_04_SWC.elf ";
	
	#print(n_target_aboveVt_swc)
	if n_target_aboveVt_swc != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_swc_chip{chip_num}{brdtype} {path}/pulse_width_table_swc");
		np.savetxt(f"{path}/target_list_aboveVt_swc", target_l_aboveVt_swc, "%5.15f", ' ')
		temp1 = f"0x{(n_target_aboveVt_swc):04x}"
		temp = temp1 + temp2_aboveVt_swc; 
		fd = open(f"{path}/target_info_aboveVt_swc", "w") 
		fd.write(temp)
		fd.close()
		
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_aboveVt_SWC ~/rasp30/prog_assembly/libs/asm_code/recover_inject_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_aboveVt_SWC ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_aboveVt_SWC ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_aboveVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_aboveVt_m_ave_04_SWC ~/rasp30/prog_assembly/libs/asm_code/fine_program_aboveVt_m_ave_04_SWC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_aboveVt_swc pulse_width_table_swc recover_inject_aboveVt_SWC.elf first_coarse_program_aboveVt_SWC.elf measured_coarse_program_aboveVt_SWC.elf fine_program_aboveVt_m_ave_04_SWC.elf ";


	if n_target_subVt_swc != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_swc_chip{chip_num}{brdtype} {path}/pulse_width_table_swc");
		np.savetxt(f"{path}/target_list_subVt_swc", target_l_subVt_swc, "%5.15f", ' ')
		temp1 = f"0x{(n_target_subVt_swc):04x}"
		temp = temp1 + temp2_subVt_swc; 
		fd = open(f"{path}/target_info_subVt_swc", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_subVt_SWC ~/rasp30/prog_assembly/libs/asm_code/recover_inject_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_subVt_SWC ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_subVt_SWC ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_subVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_subVt_m_ave_04_SWC ~/rasp30/prog_assembly/libs/asm_code/fine_program_subVt_m_ave_04_SWC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_subVt_swc pulse_width_table_swc recover_inject_subVt_SWC.elf first_coarse_program_subVt_SWC.elf measured_coarse_program_subVt_SWC.elf fine_program_subVt_m_ave_04_SWC.elf ";
		

	if n_target_lowsubVt_swc != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_lowsubVt_swc_chip{chip_num}{brdtype} {path}/pulse_width_table_lowsubVt_swc");
		np.savetxt(f"{path}/target_list_lowsubVt_swc", target_l_lowsubVt_swc, "%5.15f", ' ')
		temp1 = f"0x{(n_target_lowsubVt_swc):04x}"
		temp = temp1 + temp2_lowsubVt_swc; 
		fd = open(f"{path}/target_info_lowsubVt_swc", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_lowsubVt_SWC ~/rasp30/prog_assembly/libs/asm_code/recover_inject_lowsubVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_lowsubVt_SWC ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_lowsubVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_lowsubVt_SWC ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_lowsubVt_SWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_lowsubVt_m_ave_04_SWC ~/rasp30/prog_assembly/libs/asm_code/fine_program_lowsubVt_m_ave_04_SWC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_lowsubVt_swc pulse_width_table_lowsubVt_swc recover_inject_lowsubVt_SWC.elf first_coarse_program_lowsubVt_SWC.elf measured_coarse_program_lowsubVt_SWC.elf fine_program_lowsubVt_m_ave_04_SWC.elf ";
	

	if n_target_highaboveVt_ota != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_ota_chip{chip_num}{brdtype} {path}/pulse_width_table_ota");
		np.savetxt(f"{path}/target_list_highaboveVt_ota", target_l_highaboveVt_ota, "%5.15f", ' ')
		temp1 = f"0x{(n_target_highaboveVt_ota):04x}"
		temp = temp1 + temp2_highaboveVt_ota; 
		fd = open(f"{path}/target_info_highaboveVt_ota", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_highaboveVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/recover_inject_highaboveVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_highaboveVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_highaboveVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_highaboveVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_highaboveVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_highaboveVt_m_ave_04_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/fine_program_highaboveVt_m_ave_04_CAB_ota.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_highaboveVt_ota recover_inject_highaboveVt_CAB_ota.elf first_coarse_program_highaboveVt_CAB_ota.elf measured_coarse_program_highaboveVt_CAB_ota.elf fine_program_highaboveVt_m_ave_04_CAB_ota.elf ";
	

	if n_target_aboveVt_ota != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_ota_chip{chip_num}{brdtype} {path}/pulse_width_table_ota");
		np.savetxt(f"{path}/target_list_aboveVt_ota", target_l_aboveVt_ota, "%5.15f", ' ')
		temp1 = f"0x{(n_target_aboveVt_ota):04x}"
		temp = temp1 + temp2_aboveVt_ota; 
		fd = open(f"{path}/target_info_aboveVt_ota", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_aboveVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/recover_inject_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_aboveVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_aboveVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_aboveVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_aboveVt_m_ave_04_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/fine_program_aboveVt_m_ave_04_CAB_ota.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_aboveVt_ota pulse_width_table_ota recover_inject_aboveVt_CAB_ota.elf first_coarse_program_aboveVt_CAB_ota.elf measured_coarse_program_aboveVt_CAB_ota.elf fine_program_aboveVt_m_ave_04_CAB_ota.elf ";


	if n_target_subVt_ota != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_ota_chip{chip_num}{brdtype} {path}/pulse_width_table_ota");
		np.savetxt(f"{path}/target_list_subVt_ota", target_l_subVt_ota, "%5.15f", ' ')
		temp1 = f"0x{(n_target_subVt_ota):04x}"
		temp = temp1 + temp2_subVt_ota; 
		fd = open(f"{path}/target_info_subVt_ota", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_subVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/recover_inject_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_subVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_subVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_subVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_subVt_m_ave_04_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/fine_program_subVt_m_ave_04_CAB_ota.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_subVt_ota pulse_width_table_ota recover_inject_subVt_CAB_ota.elf first_coarse_program_subVt_CAB_ota.elf measured_coarse_program_subVt_CAB_ota.elf fine_program_subVt_m_ave_04_CAB_ota.elf ";


	if n_target_lowsubVt_ota != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_lowsubVt_ota_chip{chip_num}{brdtype} {path}/pulse_width_table_lowsubVt_ota");
		np.savetxt(f"{path}/target_list_lowsubVt_ota", target_l_lowsubVt_ota, "%5.15f", ' ')
		temp1 = f"0x{(n_target_lowsubVt_ota):04x}"
		temp = temp1 + temp2_lowsubVt_ota; 
		fd = open(f"{path}/target_info_lowsubVt_ota", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_lowsubVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/recover_inject_lowsubVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_lowsubVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_lowsubVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_lowsubVt_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_lowsubVt_CAB_ota.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_lowsubVt_m_ave_04_CAB_ota ~/rasp30/prog_assembly/libs/asm_code/fine_program_lowsubVt_m_ave_04_CAB_ota.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_lowsubVt_ota pulse_width_table_lowsubVt_ota recover_inject_lowsubVt_CAB_ota.elf first_coarse_program_lowsubVt_CAB_ota.elf measured_coarse_program_lowsubVt_CAB_ota.elf fine_program_lowsubVt_m_ave_04_CAB_ota.elf ";


	if n_target_aboveVt_otaref != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_otaref_chip{chip_num}{brdtype} {path}/pulse_width_table_otaref");
		np.savetxt(f"{path}/target_list_aboveVt_otaref", target_l_aboveVt_otaref, "%5.15f", ' ')
		temp1 = f"0x{(n_target_aboveVt_otaref):04x}"
		temp = temp1 + temp2_aboveVt_otaref; 
		fd = open(f"{path}/target_info_aboveVt_otaref", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_aboveVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/recover_inject_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_aboveVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_aboveVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_aboveVt_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_aboveVt_m_ave_04_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/fine_program_aboveVt_m_ave_04_CAB_ota_ref.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_aboveVt_otaref pulse_width_table_otaref recover_inject_aboveVt_CAB_ota_ref.elf first_coarse_program_aboveVt_CAB_ota_ref.elf measured_coarse_program_aboveVt_CAB_ota_ref.elf fine_program_aboveVt_m_ave_04_CAB_ota_ref.elf ";

	if n_target_subVt_otaref != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_otaref_chip{chip_num}{brdtype} {path}/pulse_width_table_otaref");
		np.savetxt(f"{path}/target_list_subVt_otaref", target_l_subVt_otaref, "%5.15f", ' ')
		temp1 = f"0x{(n_target_subVt_otaref):04x}"
		temp = temp1 + temp2_subVt_otaref; 
		fd = open(f"{path}/target_info_subVt_otaref", "w") 
		fd.write(temp)
		fd.close()  
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_subVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/recover_inject_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_subVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_subVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_subVt_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_subVt_m_ave_04_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/fine_program_subVt_m_ave_04_CAB_ota_ref.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_subVt_otaref pulse_width_table_otaref recover_inject_subVt_CAB_ota_ref.elf first_coarse_program_subVt_CAB_ota_ref.elf measured_coarse_program_subVt_CAB_ota_ref.elf fine_program_subVt_m_ave_04_CAB_ota_ref.elf ";


	if n_target_lowsubVt_otaref != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_lowsubVt_otaref_chip{chip_num}{brdtype} {path}/pulse_width_table_lowsubVt_otaref");
		np.savetxt(f"{path}/target_list_lowsubVt_otaref", target_l_lowsubVt_otaref, "%5.15f", ' ')
		temp1 = f"0x{(n_target_lowsubVt_otaref):04x}"
		temp = temp1 + temp2_lowsubVt_otaref; 
		fd = open(f"{path}/target_info_lowsubVt_otaref", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_lowsubVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/recover_inject_lowsubVt_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_lowsubVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_lowsubVt_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_lowsubVt_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_lowsubVt_CAB_ota_ref.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_lowsubVt_m_ave_04_CAB_ota_ref ~/rasp30/prog_assembly/libs/asm_code/fine_program_lowsubVt_m_ave_04_CAB_ota_ref.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_lowsubVt_otaref pulse_width_table_lowsubVt_otaref recover_inject_lowsubVt_CAB_ota_ref.elf first_coarse_program_lowsubVt_CAB_ota_ref.elf measured_coarse_program_lowsubVt_CAB_ota_ref.elf fine_program_lowsubVt_m_ave_04_CAB_ota_ref.elf ";


	if n_target_aboveVt_mite != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_mite_chip{chip_num}{brdtype} {path}/pulse_width_table_mite");
		fprintfMat('target_list_aboveVt_mite', target_l_aboveVt_mite, "%5.15f");
		np.savetxt(f"{path}/target_list_aboveVt_mite", target_l_aboveVt_mite, "%5.15f", ' ')
		temp1 = f"0x{(n_target_aboveVt_mite):04x}"
		temp = temp1 + temp2_aboveVt_mite; 
		fd = open(f"{path}/target_info_aboveVt_mite", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_aboveVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/recover_inject_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_aboveVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_aboveVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_aboveVt_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_aboveVt_m_ave_04_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/fine_program_aboveVt_m_ave_04_CAB_mite.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_aboveVt_mite pulse_width_table_mite recover_inject_aboveVt_CAB_mite.elf first_coarse_program_aboveVt_CAB_mite.elf measured_coarse_program_aboveVt_CAB_mite.elf fine_program_aboveVt_m_ave_04_CAB_mite.elf ";


	if n_target_subVt_mite != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_mite_chip{chip_num}{brdtype} {path}/pulse_width_table_mite");
		np.savetxt(f"{path}/target_list_subVt_mite", target_l_subVt_mite, "%5.15f", ' ')
		temp1 = f"0x{(n_target_aboveVt_swc):04x}"
		temp = temp1 + temp2_subVt_mite; 
		fd = open(f"{path}/target_info_subVt_mite", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_subVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/recover_inject_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_subVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_subVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_subVt_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_subVt_m_ave_04_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/fine_program_subVt_m_ave_04_CAB_mite.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_subVt_mite pulse_width_table_mite recover_inject_subVt_CAB_mite.elf first_coarse_program_subVt_CAB_mite.elf measured_coarse_program_subVt_CAB_mite.elf fine_program_subVt_m_ave_04_CAB_mite.elf ";


	if n_target_lowsubVt_mite != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_lowsubVt_mite_chip{chip_num}{brdtype} {path}/pulse_width_table_lowsubVt_mite");
		np.savetxt(f"{path}/target_list_lowsubVt_mite", target_l_lowsubVt_mite, "%5.15f", ' ')
		temp1 = f"0x{(n_target_lowsubVt_mite):04x}"
		temp = temp1 + temp2_lowsubVt_mite; 
		fd = open(f"{path}/target_info_lowsubVt_mite", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_lowsubVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/recover_inject_lowsubVt_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_lowsubVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_lowsubVt_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_lowsubVt_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_lowsubVt_CAB_mite.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_lowsubVt_m_ave_04_CAB_mite ~/rasp30/prog_assembly/libs/asm_code/fine_program_lowsubVt_m_ave_04_CAB_mite.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_lowsubVt_mite pulse_width_table_lowsubVt_mite recover_inject_lowsubVt_CAB_mite.elf first_coarse_program_lowsubVt_CAB_mite.elf measured_coarse_program_lowsubVt_CAB_mite.elf fine_program_lowsubVt_m_ave_04_CAB_mite.elf ";


	if n_target_aboveVt_dirswc != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_dirswc_chip{chip_num}{brdtype} {path}/pulse_width_table_dirswc");
		np.savetxt(f"{path}/target_list_aboveVt_dirswc", target_l_aboveVt_dirswc, "%5.15f", ' ')
		temp1 = f"0x{(n_target_aboveVt_dirswc):04x}"
		temp = temp1 + temp2_aboveVt_dirswc; 
		fd = open(f"{path}/target_info_aboveVt_dirswc", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_aboveVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/recover_inject_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_aboveVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_aboveVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_aboveVt_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_aboveVt_m_ave_04_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/fine_program_aboveVt_m_ave_04_DIRSWC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_aboveVt_dirswc pulse_width_table_dirswc recover_inject_aboveVt_DIRSWC.elf first_coarse_program_aboveVt_DIRSWC.elf measured_coarse_program_aboveVt_DIRSWC.elf fine_program_aboveVt_m_ave_04_DIRSWC.elf ";


	if n_target_subVt_dirswc != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_dirswc_chip{chip_num}{brdtype} {path}/pulse_width_table_dirswc");
		np.savetxt(f"{path}/target_list_subVt_dirswc", target_l_subVt_dirswc, "%5.15f", ' ')
		temp1 = f"0x{(n_target_subVt_dirswc):04x}"
		temp = temp1 + temp2_subVt_dirswc; 
		fd = open(f"{path}/target_info_subVt_dirswc", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_subVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/recover_inject_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_subVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_subVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_subVt_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_subVt_m_ave_04_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/fine_program_subVt_m_ave_04_DIRSWC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_subVt_dirswc pulse_width_table_dirswc recover_inject_subVt_DIRSWC.elf first_coarse_program_subVt_DIRSWC.elf measured_coarse_program_subVt_DIRSWC.elf fine_program_subVt_m_ave_04_DIRSWC.elf ";


	if n_target_lowsubVt_dirswc != 0:
		os.system(f"cp ~/rasp30/prog_assembly/libs/chip_parameters/pulse_width_table/pulse_width_table_lowsubVt_dirswc_chip{chip_num}{brdtype} {path}/pulse_width_table_lowsubVt_dirswc");
		np.savetxt(f"{path}/target_list_lowsubVt_dirswc", target_l_lowsubVt_dirswc, "%5.15f", ' ')
		temp1 = f"0x{(n_target_lowsubVt_dirswc):04x}"
		temp = temp1 + temp2_lowsubVt_dirswc; 
		fd = open(f"{path}/target_info_lowsubVt_dirswc", "w") 
		fd.write(temp)
		fd.close()
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh recover_inject_lowsubVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/recover_inject_lowsubVt_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh first_coarse_program_lowsubVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/first_coarse_program_lowsubVt_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh measured_coarse_program_lowsubVt_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/measured_coarse_program_lowsubVt_DIRSWC.s43 16384 16384 16384 {path}");
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh fine_program_lowsubVt_m_ave_04_DIRSWC ~/rasp30/prog_assembly/libs/asm_code/fine_program_lowsubVt_m_ave_04_DIRSWC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "target_info_lowsubVt_dirswc pulse_width_table_lowsubVt_dirswc recover_inject_lowsubVt_DIRSWC.elf first_coarse_program_lowsubVt_DIRSWC.elf measured_coarse_program_lowsubVt_DIRSWC.elf fine_program_lowsubVt_m_ave_04_DIRSWC.elf ";


	os.system(f"mv {path}/chip_para_debug.asm {path}/chip_para_TR.asm {path}/chip_para_SP.asm {path}/chip_para_RI.asm {path}/chip_para_CP.asm {path}/chip_para_FP.asm *.l43 *.o pmem.x pmem_defs.asm {hid_dir}");

	###########################
	## Make output_info file ##
	###########################
	temp_mite=' '; n_target_mite=0; target_list_mite=[0,0]; temp1=0;

	for i in range(n):
	    # Switch programming - 0 : Switch FGs, Target programming - 1 : Switch FGs , 2 : OTA_ref FGs (Bias), 3 : OTA FGs, 4 : MITE, 5 : BLE
		if target_listArray[i][3] == 4:
			temp_mite = f"0x{(target_listArray[i][0]):04x} 0x{(target_listArray[i][1]):04x}"  # Row, Col
			n_target_mite = n_target_mite + 1;
			
	temp1 = f"0x{(n_target_mite):04x}"
	temp = temp1 + temp_mite; 
	fd = open(f"{path}/output_info", "w") 
	fd.write(temp)
	fd.close()

	os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh run_mode_after_program ~/rasp30/prog_assembly/libs/asm_code/voltage_measurement_ver01_afterprogram.s43 16384 16384 16384 {path}");

	#global RAMP_ADC_check sftreg_check Signal_DAC_check GPIO_IN_check MITE_ADC_check ONchip_ADC Counter_class;
	if n_target_mite != 0:
		MITE_ADC_check = 1

	if(extension == '.swcs'):    # When it uses swcs for programming, this is default set.
		RAMP_ADC_check=0; sftreg_check=0; Signal_DAC_check=0; GPIO_IN_check=0; MITE_ADC_check=0;
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/voltage_measurement_ver01_withoutMITE.s43 16384 16384 16384 {path}");
		zip_list = zip_list + "voltage_meas.elf ";

	if (Signal_DAC_check==1) and (GPIO_IN_check==0) and (MITE_ADC_check==0):
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/voltage_measurement_ver01_withoutMITE.s43 16384 16384 16384 {path}");
		zip_list = zip_list + 'voltage_meas.elf ';

	if (Signal_DAC_check==1) and (GPIO_IN_check==0) and (MITE_ADC_check==1):
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/voltage_measurement_ver01_withMITE.s43 16384 16384 16384 {path}");
		zip_list = zip_list + 'output_info voltage_meas.elf ';

	if (Signal_DAC_check==1) and (GPIO_IN_check==1) and (MITE_ADC_check==1):
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/runmode_signalDAC_gpin_miteADC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + 'gpin_vector output_info voltage_meas.elf ';

	if (Signal_DAC_check==1) and (GPIO_IN_check==0) and (RAMP_ADC_check==1):
		if sftreg_check==1: 
			os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/sftreg_adc.s43 16384 16384 16384 {path}"); 
			print("shift here");
		#else os.system("~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/Ramp_ADC_DAC.s43 16384 16384 16384 {path}"); print
		#print("RAMP here");
		else:
			os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/Ramp_ADC_DAC.s43 16384 16384 16384 {path}");#please use this it creates issues in remote
		print("RAMP here");
		zip_list = zip_list + 'output_info voltage_meas.elf ';

	if (Signal_DAC_check==1) and (GPIO_IN_check==1) and (RAMP_ADC_check==1):
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/runmode_signalDAC_gpin_rampADC.s43 16384 16384 16384 {path}");
		zip_list = zip_list + 'gpin_vector output_info output_info voltage_meas.elf ';
		
	if (Signal_DAC_check==1) and (ONchip_ADC==1):
		unix_g(f"echo ashes1234 | sudo -S ~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/ADC_onchip.s43 16384 16384 16384 {path}")
		zip_list = zip_list + 'output_info output_info voltage_meas.elf ';
		
	if (Signal_DAC_check==1) and (Counter_class==1):
		unix_g(f"echo ashes1234 | sudo -S ~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/Counter.s43 16384 16384 16384 {path}")
		zip_list = zip_list + 'output_info output_info voltage_meas.elf ';
		print("here")

	if (Signal_DAC_check==1) and (Counter_class==1) and (GPIO_IN_check==1):
		unix_g(f"echo ashes1234 | sudo -S ~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/Counter.s43 16384 16384 16384 {path}")
		zip_list = zip_list + 'output_info output_info voltage_meas.elf ';
		print("here1")


	input_vector_temp = np.loadtxt(f"{path}/input_vector", converters={_:lambda s: int(s, 16) for _ in range(4)})
	if input_vector_temp[1] == 0:
		os.system(f"~/rasp30/prog_assembly/libs/sh/asm2ihex2.sh voltage_meas ~/rasp30/prog_assembly/libs/asm_code/voltage_measurement_ver01_just_runmode.s43 16384 16384 16384 {path}")
	zip_list = zip_list + "input_vector "
'''
	os.system(f"rm {project_name}.zip");
	os.system(f"zip {project_name}.zip {zip_list}");
	#input_vector input_vector_for_graph insert into below
	os.system(f"mv DAC_mapping_info output_info pulse_width_table_swc pulse_width_table_ota pulse_width_table_otaref pulse_width_table_mite pulse_width_table_dirswc pulse_width_table_lowsubVt_swc pulse_width_table_lowsubVt_ota pulse_width_table_lowsubVt_otaref pulse_width_table_lowsubVt_mite pulse_width_table_lowsubVt_dirswc switch_info switch_list Vd_table_30mV *.elf target_info* target_list* mismatch_mapped_swc_list gpin_vector gpin_mapping_info {hid_dir}");
	os.system(f"mv *.l43 *.o pmem.x pmem_defs.asm {hid_dir}");

'''
def diodeADC_v2i(Vfg, chip_num, brdtype):
	vdd=2.5;
	EKV_diodeADC_para = np.loadtxt(f"/home/ubuntu/rasp30/prog_assembly/libs/chip_parameters/EKV_diodeADC/EKV_diodeADC_chip{chip_num}{brdtype}", delimiter = ',')
	Is=EKV_diodeADC_para[0]
	VT=EKV_diodeADC_para[1]
	kappa=EKV_diodeADC_para[2]
	Slope_v2h=EKV_diodeADC_para[3]	
	Offset_v2h=EKV_diodeADC_para[4]
	Isat=Is*np.power((np.log(1+np.exp(kappa*((vdd-Vfg)-VT)/(2*0.0258)))),2)
	return Isat
def diodeADC_i2v(Isat, chip_num, brdtype):
	vdd=2.5;
	EKV_diodeADC_para = np.loadtxt(f"/home/ubuntu/rasp30/prog_assembly/libs/chip_parameters/EKV_diodeADC/EKV_diodeADC_chip{chip_num}{brdtype}", delimiter = ',')
	Is=EKV_diodeADC_para[0]
	VT=EKV_diodeADC_para[1]
	kappa=EKV_diodeADC_para[2]
	Slope_v2h=EKV_diodeADC_para[3]	
	Offset_v2h=EKV_diodeADC_para[4]
	Vfg=vdd-(((np.log(np.exp(np.sqrt(Isat/Is))-1)*(2*0.0258)/kappa)+VT)*2)/2;
	return Vfg
def diodeADC_v2h(Vfg, chip_num, brdtype):
	vdd=2.5;
	EKV_diodeADC_para = np.loadtxt(f"/home/ubuntu/rasp30/prog_assembly/libs/chip_parameters/EKV_diodeADC/EKV_diodeADC_chip{chip_num}{brdtype}", delimiter = ',')
	Is=EKV_diodeADC_para[0]
	VT=EKV_diodeADC_para[1]
	kappa=EKV_diodeADC_para[2]
	Slope_v2h=EKV_diodeADC_para[3]	
	Offset_v2h=EKV_diodeADC_para[4]
	hex=Slope_v2h*2*(vdd-Vfg) + Offset_v2h;
	return hex
def diodeADC_h2v(hex, chip_num, brdtype):
	vdd=2.5;
	EKV_diodeADC_para = np.loadtxt(f"/home/ubuntu/rasp30/prog_assembly/libs/chip_parameters/EKV_diodeADC/EKV_diodeADC_chip{chip_num}{brdtype}", delimiter = ',')
	Is=EKV_diodeADC_para[0]
	VT=EKV_diodeADC_para[1]
	kappa=EKV_diodeADC_para[2]
	Slope_v2h=EKV_diodeADC_para[3]	
	Offset_v2h=EKV_diodeADC_para[4]
	Vfg=vdd-((hex-Offset_v2h)/Slope_v2h)/2;
	return Vfg
	

