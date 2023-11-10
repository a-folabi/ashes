from ashes_fg.asic.py_to_verilog import asic_compiler
from ashes_fg.asic.verilog_to_gds import gds_synthesis
import os
import subprocess

def compile(system, project_name=None, tech_process='privA_65', dbu=1000, track_spacing=250, x_offset=None, y_offset=None, design_area=(0,0,1,1)):
	asic_compiler(system, project_name)
	# All units in nanometers
	tech_process = 'privA_65'
	dbu = 1000
	track_spacing = 250
	# placement offset to make space for pin routing
	x_offset = 500*2*track_spacing 
	y_offset = 15*2*track_spacing
	design_area = (20.5e4, 21.76e4, 120e4, 34e4, x_offset, y_offset)
	gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, project_name)
	detailed_router = os.path.exists(os.path.join('TritonRoute','build','TritonRoute'))
	if detailed_router:
		tr_executable = os.path.join('TritonRoute','build','TritonRoute')
		lef_file = os.path.join(project_name, project_name + '.lef')
		def_file = os.path.join(project_name, project_name + '.def')
		guide_file = os.path.join(project_name, project_name + '.guide')
		out_file = os.path.join(project_name, project_name + '_routed.def')
		command = [tr_executable, '-lef', lef_file, '-def', def_file, '-guide', guide_file, '-output', out_file]
		#routing_result = subprocess.run(command, capture_output=True, text=True)
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# Read the output in real-time
		while True:      
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				print(output.strip())
		gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, project_name, routed_def=True)
    
