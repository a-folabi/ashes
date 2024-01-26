import os

def b2swcs(project_name, board_type):
	
	vpr_path = "/home/ubuntu/rasp30/vtr_release/vpr"
	arch_path = "/home/ubuntu/rasp30/vpr2swcs/arch"
	genswcs_path = "/home/ubuntu/rasp30/vpr2swcs"
	
	path = os.path.join("/home/ubuntu/ashes/",project_name)

	if board_type == '3.0a': 
		arch = "rasp3a"
		brd_param = f" -{arch}"
	elif board_type == '3.0': 
		arch = "rasp3"
		brd_param = ""
		
	os.system(f"{vpr_path}/vpr {arch_path}/{arch}_arch.xml {path}/{project_name} -route_chan_width 17 -timing_analysis off -fix_pins {path}/{project_name}.pads -nodisp")
	
	
	os.system(f"python {genswcs_path}/genswcs.py -c {path}/{project_name} -d {path} -route {brd_param}")


