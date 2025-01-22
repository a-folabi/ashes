import os, sys, subprocess

def main():
	#os.chdir(path)
	#performs tunnel_revtun_ver00_gui.sce functionality
	# subprocess.run(["/usr/local/bin/python", "-c", "print('This is a subprocess')"])
	print("run subprocess 1:\n")
	#a1=subprocess.run(["/usr/bin/python", "-c", "os.system('tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 tunnel_revtun_SWC_CAB.elf')"])
	#cmd_path = "%s:%s" % ("/home/ubuntu/rasp30/prog_assembly/libs/tcl/", os.environ["PATH"])
	#cmd_env = os.environ.copy().update(PATH=cmd_path)
	returncode = -1
	#returncode != 0
	while True:
		try:
			a1=subprocess.Popen(["tclsh", "program.tcl", "-speed", "115200", "/home/ubuntu/ashes/ors_buffer/tunnel_revtun_SWC_CAB.elf"], cwd="/home/ubuntu/rasp30/prog_assembly/libs/tcl")
			returncode = a1.wait()
			print(returncode)
			if returncode != 0:
				raise subprocess.CalledProcessError(returncode=a1.returncode, cmd=a1.args)
				#print("failed: trying again")
		except subprocess.CalledProcessError:
			print("failed: trying again")
		#except KeyboardInterrupt:
		# 	print("keyboard interrupt triggered")
		#	a1.send_signal(9)
		#	a1.wait()
		#	print("process killed")
			#os.killpg(os.getpgid(a1.pid), signal.SIGKILL)
			
	print("Ran subprocess 1")
	#return()
	#performs switch_program_ver05_gui.sce functionality
	while True: 
		try:
			print("run subprocess 2:\n")
			subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "start_address", "0x5500", "-input_file_name switch_info"])
			#cwd="/home/ubuntu/rasp30/prog_assembly/libs/tcl"
			print("ran subprocess 2")
			break
		except:
			print("failed: trying again")
	while True: 
		try:
			subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -" ,"start_address", "0x7000", "-input_file_name switch_info"])
			print("ran subprocess 3")
			break
		except:
			print("failed: trying again")
	while True: 
		try:
			subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl", "-speed", "115200", "switch_program.elf"])
			break
		except:
			print("failed: trying again")

	#performs target_program_ver02_gui.sce functionality
	TL = open('target_list', 'r') # open target_list
	n_target_tunnel_revtun=TL.readline() # store values in variables
	n_target_highaboveVt_swc=TL.readline()
	n_target_highaboveVt_ota=TL.readline()
	n_target_aboveVt_swc=TL.readline()
	n_target_aboveVt_ota=TL.readline()
	n_target_aboveVt_otaref=TL.readline()
	n_target_aboveVt_mite=TL.readline()
	n_target_aboveVt_dirswc=TL.readline()
	n_target_subVt_swc=TL.readline()
	n_target_subVt_ota=TL.readline()
	n_target_subVt_otaref=TL.readline()
	n_target_subVt_mite=TL.readline()
	n_target_subVt_dirswc=TL.readline()
	n_target_lowsubVt_swc=TL.readline()
	n_target_lowsubVt_ota=TL.readline()
	n_target_lowsubVt_otaref=TL.readline()
	n_target_lowsubVt_mite=TL.readline()
	n_target_lowsubVt_dirswc=TL.readline()
	if n_target_highaboveVt_swc != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name target_info_highaboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tc", "-start_address", "0x6800", "-input_file_name pulse_width_table_highaboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_highaboveVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000", "-length", "7000". "-output_file_name", "data_highaboveVt_swc_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name target_info_highaboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", "115200", "first_coarse_program_highaboveVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "" 0x5000 -length 7000 -output_file_name data_highaboveVt_swc_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name", "target_info_highaboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl ",  "-speed", "115200", "measured_coarse_program_highaboveVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_highaboveVt_swc_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl" ,"-start_address", "0x7000", "-input_file_name target_info_highaboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input_file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl" ,  "-speed", "115200", "fine_program_highaboveVt_m_ave_04_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_highaboveVt_swc_5.hex"])
	if n_target_aboveVt_swc != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name", "target_info_aboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl","-start_address", "0x6800", "-input_file_name pulse_width_table_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl" ,  "-speed", "115200", "recover_inject_aboveVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_swc_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name target_info_aboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl" ,  "-speed", "115200", "first_coarse_program_aboveVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_swc_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl","-start_address","0x7000", "-input_file_name target_info_aboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl" ,  "-speed", "115200", "measured_coarse_program_aboveVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_swc_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name target_info_aboveVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input_file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", "115200", "fine_program_aboveVt_m_ave_04_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_swc_5.hex"])
	if n_target_subVt_swc != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl","-start_address", "0x7000", "-input_file_name target_info_subVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl" , "-start_address", "0x6800", "-input_file_name pulse_width_table_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl" ,  "-speed", "115200", "recover_inject_subVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_swc_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl","-start_address", "0x7000", "-input_file_name target_info_subVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", "115200", "first_coarse_program_subVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_swc_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name target_info_subVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", "115200", "measured_coarse_program_subVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_swc_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name target_info_subVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl" , "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", "115200", "fine_program_subVt_m_ave_04_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_swc_5.hex"])
	if n_target_lowsubVt_swc != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl","-start_address", "0x7000", "-input_file_name target_info_lowsubVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -" , "" , "start_address", "0x6800", "-input_file_name pulse_width_table_lowsubVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", "115200", "recover_inject_lowsubVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_swc_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input_file_name target_info_lowsubVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_lowsubVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_swc_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_lowsubVt_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_swc_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_swc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_lowsubVt_m_ave_04_SWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_swc_5.hex"])
	if n_target_highaboveVt_ota != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_highaboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_highaboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_highaboveVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_highaboveVt_ota_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_highaboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_highaboveVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_highaboveVt_ota_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_highaboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_highaboveVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_highaboveVt_ota_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_highaboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_highaboveVt_m_ave_04_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_highaboveVt_ota_5.hex"])
	if n_target_aboveVt_ota != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_aboveVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_ota_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_aboveVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_ota_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_aboveVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_ota_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_aboveVt_m_ave_04_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_ota_5.hex"])
	if n_target_subVt_ota != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_subVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_ota_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_subVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_ota_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_subVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_ota_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_subVt_m_ave_04_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_ota_5.hex"])
	if n_target_lowsubVt_ota != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_lowsubVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_lowsubVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_ota_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_lowsubVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_ota_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_lowsubVt_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_ota_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_ota"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_lowsubVt_m_ave_04_CAB_ota.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_ota_5.hex"])
	if n_target_aboveVt_otaref != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_aboveVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_otaref_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_aboveVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_otaref_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_aboveVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_otaref_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_aboveVt_m_ave_04_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_otaref_5.hex"])
	if n_target_subVt_otaref != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_subVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_otaref_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_subVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_otaref_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_subVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_otaref_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_subVt_m_ave_04_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_otaref_5.hex"])
	if n_target_lowsubVt_otaref != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_lowsubVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_lowsubVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_lowsubVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_lowsubVt_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_otaref"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_lowsubVt_m_ave_04_CAB_ota_ref.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_5.hex"])
	if n_target_aboveVt_mite != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_aboveVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_mite_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_aboveVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_mite_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_aboveVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_mite_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_aboveVt_m_ave_04_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_mite_5.hex"])
	if n_target_subVt_mite != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_subVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_mite_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_subVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_mite_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_subVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_mite_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_subVt_m_ave_04_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_mite_5.hex"])
	if n_target_lowsubVt_mite != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_lowsubVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_lowsubVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_mite_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_lowsubVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_mite_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_lowsubVt_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_mite_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_mite"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_lowsubVt_m_ave_04_CAB_mite.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_mite_5.hex"])
	if n_target_aboveVt_dirswc != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_aboveVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_aboveVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_aboveVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_aboveVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_aboveVt_m_ave_04_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_5.hex"])
	if n_target_subVt_dirswc != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_subVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_dirswc_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_subVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_dirswc_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_subVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_dirswc_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_subVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_subVt_m_ave_04_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_subVt_dirswc_5.hex"])
	if n_target_lowsubVt_dirswc != "0.000000000000000\n":
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name pulse_width_table_lowsubVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 recover_inject_lowsubVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_2.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 first_coarse_program_lowsubVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_3.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 measured_coarse_program_lowsubVt_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_4.hex"])
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x7000", "-input _file_name target_info_lowsubVt_dirswc"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x6800", "-input _file_name Vd_table_30mV"])
				break
			except:
				print("failed: trying again")
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl " ,  "-speed", " 115200 fine_program_lowsubVt_m_ave_04_DIRSWC.elf"])
				break
			except:
				print("failed: trying again")
		#subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_5.hex"])
	TL.close()
	while True: 
		try:
			subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x4300", "-input _file_name input_vector"])
			break
		except:
			print("failed: trying again")
	while True: 
		try:
			subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x4200", "-input _file_name output_info"])
			break
		except:
			print("failed: trying again")
	if os.path.exists('./gpin_vector'):
		while True: 
			try:
				subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl", "-start_address", "0x5500", "-input _file_name gpin_vector"])
				break
			except:
				print("failed: trying again")
	while True: 
		try:
			subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/run_new.tcl " ,  "-speed", " 115200 voltage_meas.elf"])
			break
		except:
			print("failed: trying again")
	os.system("sleep 30")
	while True: 
		try:
			subprocess.run(["tclsh", "/home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl", "-start_address", "0x6000 -length 1000 -output_file_name output_vector"])
			break
		except:
			print("failed: trying again")
	os.system("sleep 30")
