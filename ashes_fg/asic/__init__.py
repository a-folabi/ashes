from ashes_fg.asic.py_to_verilog import asic_compiler
from ashes_fg.asic.verilog_to_gds import gds_synthesis
import os
import subprocess
import re

def compile(system, project_name=None, tech_process='privA_65', dbu=1000, track_spacing=250, x_offset=None, y_offset=None, design_area=(0,0,1,1)):
	#asic_compiler(system, project_name)
	project_name = 'cell2cell_350nm'
	# All units in nanometers
	tech_process = 'vis350'
	dbu = 1000
	track_spacing = 250
	# placement offset to make space for pin routing
	x_offset, y_offset = 400*track_spacing, 2000*track_spacing 
	design_area = (152e3, 152e3, 1258e3, 1258e3, x_offset, y_offset)
	gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, project_name)
	# Pick the detailed router and default to qrouter. If not available, check for Triton.
	qrouter = True if os.system('command -v qrouter') == 0 else False
	triton_route = os.path.exists(os.path.join('TritonRoute','build','TritonRoute'))
	lef_file = os.path.join(project_name, project_name + '.lef')
	def_file = os.path.join(project_name, project_name + '.def')
	if qrouter:
		out_file = os.path.join(project_name, project_name + '_qroute.def')
		param_file = os.path.join(project_name, "qrouter_params.tcl")
		q_params = open(param_file, "w")
		q_params.write(f"read_lef {lef_file}\n")
		q_params.write(f"read_def {def_file}\n")
		q_params.write("passes 50\n")
		q_params.write("stage1\n")
		q_params.write("stage2\n")
		q_params.write("stage3\n")
		q_params.write(f"write_def {out_file}\n")
		q_params.write("quit\n")
		q_params.close()
		command = ['qrouter', '-nog', '-s', param_file]
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# Read the output in real-time
		while True:      
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				print(output.strip())
		gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, project_name, routed_def=True, router_tool='qrouter')
	elif triton_route:
		tr_executable = os.path.join('TritonRoute','build','TritonRoute')
		guide_file = os.path.join(project_name, project_name + '.guide')
		out_file = os.path.join(project_name, project_name + '_routed.def')
		num_threads = '8'
		command = [tr_executable, '-lef', lef_file, '-def', def_file, '-guide', guide_file, '-output', out_file, '-threads', num_threads]		
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# Read the output in real-time
		while True:      
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				print(output.strip())
		gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, project_name, routed_def=True, router_tool='triton')
		