import os
import sys
import ashes_fg.fpaa.genswcs as gs

def blif2swcs(sys_name, project_name, board_type, out_path):
    '''
    Generates the switch list from input .blif netlist and pads files
    '''
    if board_type == '3.0a':
        arch = 'rasp3a'
        brdtype = ' -'+arch
    elif board_type == '3.0':
        arch = 'rasp3'
        brdtype = ''
    elif board_type == '3.0n':
        arch = 'rasp3n'
        brdtype = ' -'+arch
    elif board_type == '3.0h':
        arch = 'rasp3h'
        brdtype = ' -'+arch
    fname = project_name
    path = str(out_path)


	## create input vector file
	with open(path + "/input_vector", "w") as f:
		f.write("0x0000 0x0000 0x03e8 0xffff")
    
	fix_loc = True
    if fix_loc:
        # TODO: make this system call os independent
    	os.system('/home/ubuntu/rasp30/vtr_release/vpr/vpr /home/ubuntu/ashes/ashes_fg/fpaa/./arch/'+arch+'_arch.xml ' + path + '/' + fname + '  -route_chan_width 17 -timing_analysis off -fix_pins ' + path + '/' + fname + '.pads -nodisp')
    	input("Hit enter when you have modified the place file")
    	gs.main(path + '/' + fname, path, arch, bs_vpr_disp='-route')
    else:
    	# changed genswcs.py call from command line call to function call
    	gs.main(path + '/' + fname, path, arch)
