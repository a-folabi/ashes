from ashes_fg.asic.py_to_verilog import asic_compiler
from ashes_fg.asic.verilog_to_gds import gds_synthesis
import os
import subprocess
import re
import time

def compile(system, project_name=None, tech_process='privA_65', dbu=1000, track_spacing=250, cell_pitch=22000, x_offset=None, y_offset=None, design_area=(0,0,1,1), location_islands=None):
	process_params = (tech_process, dbu, track_spacing, x_offset, y_offset, cell_pitch)
	pl_start = time.time()
	gds_synthesis(process_params, design_area, project_name, isle_loc=location_islands)
	pl_end = time.time()
	
	# Pick the detailed router and default to qrouter. If not available, check for Triton.
	qrouter = True if os.system('command -v qrouter') == 0 else False
	triton_route = os.path.exists(os.path.join('TritonRoute','build','TritonRoute'))
	lef_file = os.path.join(project_name, project_name + '.lef')
	def_file = os.path.join(project_name, project_name + '.def')
	if qrouter:
		base_cost = 10
		out_file = os.path.join(project_name, project_name + '_qroute.def')
		param_file = os.path.join(project_name, "qrouter_params.tcl")
		q_params = open(param_file, "w")
		q_params.write(f"read_lef {lef_file}\n")
		q_params.write(f"read_def {def_file}\n")
		q_params.write("passes 70\n")
		q_params.write(f"cost via {10*base_cost}\n")
		q_params.write("cost jog 10\n")
		q_params.write("layers 3\n")
		q_params.write("stage1 mask none\n")
		q_params.write("stage2 mask none limit 100\n")
		q_params.write("stage3 mask none\n")
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
		rt_end = time.time()
		gds_synthesis(process_params, design_area, project_name, routed_def=True, router_tool='qrouter')
		fin_end = time.time()
		pl_time = round(pl_end - pl_start, 3)
		rt_time = round(rt_end - pl_end, 3)
		merge_time = round(fin_end - rt_end, 3)
		total_time = round(fin_end - pl_start, 3)
		print(f"placement took {pl_time} s, routing took {rt_time} s, merging took {merge_time} s, total time {total_time} s")

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
		gds_synthesis(process_params, design_area, project_name, routed_def=True, router_tool='triton')
		
