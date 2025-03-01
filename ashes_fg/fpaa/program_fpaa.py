import os, sys, subprocess

def main():

	#os.chdir(path)
	#performs tunnel_revtun_ver00_gui.sce functionality
	#os.system("sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 tunnel_revtun_SWC_CAB.elf")
	returncode = -1
	while True:
		try:
			a1=subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 tunnel_revtun_SWC_CAB.elf"], shell=True, capture_output=True, text=True)
			output = a1.stdout
			print(output)
			success_message = "Program completed."
			failure_message = "failed"
			if success_message in output and a1.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(a1.stderr)
				raise subprocess.CalledProcessError(returncode=a1.returncode, cmd=a1.args)
		except subprocess.CalledProcessError:
			print("failed: trying again")

	#performs switch_program_ver05_gui.sce functionality
	while True: 
		try:
			proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x5500 -input_file_name switch_info"], shell=True, capture_output=True, text=True)
			output = proc.stdout
			print(output)
			success_message = "Writing file: "
			if success_message in output and proc.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(proc.stderr)
				raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
		except subprocess.CalledProcessError:
			print("failed: trying again")
	while True: 
		try:
			proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name switch_info"], shell=True, capture_output=True, text=True)
			output = proc.stdout
			print(output)
			success_message = "Writing file: "
			if success_message in output and proc.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(proc.stderr)
				raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
		except subprocess.CalledProcessError:
			print("failed: trying again")
	while True: 
		try:
			#os.system("sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 switch_program.elf")
			proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 switch_program.elf"], shell=True, capture_output=True, text=True)
			output = proc.stdout
			print(output)
			success_message = "Program completed."
			if success_message in output and proc.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(proc.stderr)
				raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
		except subprocess.CalledProcessError:
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
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_highaboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_highaboveVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length", "7000". "-output_file_name data_highaboveVt_swc_2.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_highaboveVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address", "" 0x5000 -length 7000 -output_file_name data_highaboveVt_swc_3.hex"], shell=True, capture_output=True, text=True)
	
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_highaboveVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_highaboveVt_swc_4.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_highaboveVt_m_ave_04_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_highaboveVt_swc_5.hex"], shell=True, capture_output=True, text=True)
				
	if n_target_aboveVt_swc != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_aboveVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_swc_2.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_aboveVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_swc_3.hex"], shell=True, capture_output=True, text=True)
			
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_aboveVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_swc_4.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_aboveVt_m_ave_04_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_swc_5.hex"], shell=True, capture_output=True, text=True)
				
	if n_target_subVt_swc != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_subVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_swc_2.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_subVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_swc_3.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_subVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_swc_4.hex"], shell=True, capture_output=True, text=True)
			
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_subVt_m_ave_04_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_swc_5.hex"], shell=True, capture_output=True, text=True)
				
	if n_target_lowsubVt_swc != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_lowsubVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_lowsubVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_swc_2.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_lowsubVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_swc_3.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_lowsubVt_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_swc_4.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_swc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_lowsubVt_m_ave_04_SWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_swc_5.hex"], shell=True, capture_output=True, text=True)
				
	if n_target_highaboveVt_ota != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(proc.stderr)
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					#print(err)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError as e:
				#print(proc.stderr)
				#print("e.message: ", e.message)
				print("e: ", e)
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_highaboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError as e:
				#print("e: ", e)
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_highaboveVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_highaboveVt_ota_2.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_highaboveVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_highaboveVt_ota_3.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_highaboveVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_highaboveVt_ota_4.hex"], shell=True, capture_output=True, text=True)
		
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_highaboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_highaboveVt_m_ave_04_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_highaboveVt_ota_5.hex"], shell=True, capture_output=True, text=True)
				
	if n_target_aboveVt_ota != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_aboveVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_ota_2.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_aboveVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_ota_3.hex"], shell=True, capture_output=True, text=True)
				
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_aboveVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_ota_4.hex"], shell=True, capture_output=True, text=True)
			
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_aboveVt_m_ave_04_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_ota_5.hex"], shell=True, capture_output=True, text=True)
				
	if n_target_subVt_ota != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_subVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_ota_2.hex"], shell=True, capture_output=True, text=True)
			
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_subVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_ota_3.hex"], shell=True, capture_output=True, text=True)
			
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_subVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_ota_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_subVt_m_ave_04_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_ota_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_lowsubVt_ota != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_lowsubVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_lowsubVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_ota_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_lowsubVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_ota_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_lowsubVt_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_ota_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_ota"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_lowsubVt_m_ave_04_CAB_ota.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_ota_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_aboveVt_otaref != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_aboveVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_otaref_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_aboveVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_otaref_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_aboveVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_otaref_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_aboveVt_m_ave_04_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_otaref_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_subVt_otaref != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_subVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_otaref_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_subVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_otaref_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_subVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_otaref_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_subVt_m_ave_04_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_otaref_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_lowsubVt_otaref != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_lowsubVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_lowsubVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_lowsubVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_lowsubVt_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_otaref"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_lowsubVt_m_ave_04_CAB_ota_ref.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_otaref_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_aboveVt_mite != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_aboveVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_mite_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_aboveVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_mite_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_aboveVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_mite_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_aboveVt_m_ave_04_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_mite_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_subVt_mite != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_subVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_mite_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_subVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_mite_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_subVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_mite_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_subVt_m_ave_04_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_mite_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_lowsubVt_mite != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_lowsubVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_lowsubVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_mite_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_lowsubVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_mite_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_lowsubVt_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_mite_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_mite"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_lowsubVt_m_ave_04_CAB_mite.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_mite_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_aboveVt_dirswc != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_aboveVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_aboveVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_aboveVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_aboveVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_aboveVt_m_ave_04_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_aboveVt_dirswc_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_subVt_dirswc != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_subVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_dirswc_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_subVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_dirswc_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_subVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_dirswc_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_subVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_subVt_m_ave_04_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_subVt_dirswc_5.hex"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
	if n_target_lowsubVt_dirswc != "0.000000000000000\n":
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name pulse_width_table_lowsubVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 recover_inject_lowsubVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_2.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 first_coarse_program_lowsubVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_3.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 measured_coarse_program_lowsubVt_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_4.hex"], shell=True, capture_output=True, text=True)
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x7000 -input_file_name target_info_lowsubVt_dirswc"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x6800 -input_file_name Vd_table_30mV"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/program.tcl -speed 115200 fine_program_lowsubVt_m_ave_04_DIRSWC.elf"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Program completed."
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
		#subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x5000 -length 7000 -output_file_name data_lowsubVt_dirswc_5.hex"], shell=True, capture_output=True, text=True)
	TL.close()
	while True: 
		try:
			proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x4300 -input_file_name input_vector"], shell=True, capture_output=True, text=True)
			output = proc.stdout
			print(output)
			success_message = "Writing file: "
			if success_message in output and proc.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(proc.stderr)
				raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
		except subprocess.CalledProcessError:
			print("failed: trying again")
	while True: 
		try:
			proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x4200 -input_file_name output_info"], shell=True, capture_output=True, text=True)
			output = proc.stdout
			print(output)
			success_message = "Writing file: "
			if success_message in output and proc.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(proc.stderr)
				raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
		except subprocess.CalledProcessError:
			print("failed: trying again")
	if os.path.exists('./gpin_vector'):
		while True: 
			try:
				proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/write_mem2_NoRelease.tcl -start_address 0x5500 -input_file_name gpin_vector"], shell=True, capture_output=True, text=True)
				output = proc.stdout
				print(output)
				success_message = "Writing file: "
				if success_message in output and proc.returncode == 0:
					print("Ran subprocess: success")
					break
				else:
					print(proc.stderr)
					raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
			except subprocess.CalledProcessError:
				print("failed: trying again")
	while True: 
		try:
			proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/run_new.tcl -speed 115200 voltage_meas.elf"], shell=True, capture_output=True, text=True)
			output = proc.stdout
			print(output)
			success_message = "Run-mode."
			if success_message in output and proc.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(proc.stderr)
				raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
		except subprocess.CalledProcessError:
			print("failed: trying again")
	os.system("sleep 30")
	while True: 
		try:
			proc = subprocess.run(["sudo tclsh /home/ubuntu/rasp30/prog_assembly/libs/tcl/read_mem2_NoRelease.tcl -start_address 0x6000 -length 1000 -output_file_name output_vector"], shell=True, capture_output=True, text=True)
			output = proc.stdout
			print(output)
			success_message = "Writing to file: "
			if success_message in output and proc.returncode == 0:
				print("Ran subprocess: success")
				break
			else:
				print(proc.stderr)
				raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)
		except subprocess.CalledProcessError:
			print("failed: trying again")
	os.system("sleep 30")
