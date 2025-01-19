from lxml import etree
import sys
import os
dirx = os.path.dirname(__file__) + '/'
sys.path.append(dirx + '/arch') 
import pdb
from subprocess import call
from os.path import isfile
import copy
import re


from ashes_fg.fpaa.rasp30 import *
from ashes_fg.fpaa.rasp30 import rasp30 as chipStats_30
from ashes_fg.fpaa.rasp30 import arrayStats as arrayStats_used_rasp30

from ashes_fg.fpaa.rasp30a import *
from ashes_fg.fpaa.rasp30a import rasp30a as chipStats_30a
from ashes_fg.fpaa.rasp30a import arrayStats as arrayStats_used_rasp30a

def main(bs_circuit_loc, bs_run_dir, bs_board_arch, bs_vpr_disp=None, bs_pins_file=None):

	#Change: moved initialization variables inside main function and made them global
	#intialization
	global rasp3a
	rasp3a = 0
	global ff_custom
	ff_custom=1
	global fix_cab
	fix_cab=0
	global cap_nams
	cap_nams = ['0dum_nam0']
	global cap_vals
	cap_vals = [0]
	global cap_seq
	cap_seq = []
	global c_outin
	c_outin = []
	global chipStats
	global arrayStats_used
	# Change: Moved imports into main function and set chipStats and arrayStats_used according to board_arch input
	if bs_board_arch == 'rasp3a': 
		chipStats = chipStats_30a
		arrayStats_used = arrayStats_used_rasp30a
	else:
		chipStats = chipStats_30
		arrayStats_used = arrayStats_used_rasp30
	if bs_board_arch == 'rasp3a': rasp3a=rasp3a+1
	if bs_vpr_disp == '-route': fix_cab=fix_cab+1
	
	global swcs
	swcs = list()
	global groutes
	global nblocks
	global luts
	global xarray
	global ex_fgs_dict
	ex_fgs_dict = dict() #extra floating-gates
	nblocks = dict()
	luts = dict()

	#---- input arguments / defaults ---- for calling VPR
	circuit_loc = './benchmarks/mad7' #default input

	run_dir = dirx + 'temp' # stores all intermediate files in VPR
	vpr_disp = 0 # TURN DISPLAY ON 1 else 0
	arch_file = []
	pins_file = []
	# Change: circuit_loc, run_dir, vpr_disp, arch_file, pins_file now set from main function inputs instead of command line call
	if bs_circuit_loc != None: circuit_loc = bs_circuit_loc
	if bs_run_dir != None: run_dir = bs_run_dir
	if bs_vpr_disp != None: vpr_disp = 1
	if bs_pins_file != None: pins_file = bs_pins_file     

	circuit_name = circuit_loc.split('/')[-1]
	if not pins_file and isfile(circuit_loc + '.pads'): pins_file = circuit_loc + '.pads'        
	print(run_dir)
	#--- main functions ---  
	
	# FIRST THING: get fixed locations from blif file and repair blif file (remove fixed locations) before other fucntions use it. 
	
	## Go through blif and find fixed locations
	fixed_locations = extract_fixed_locations(circuit_loc + '.blif') # fixed_locations stores [subblock name, x location, y location]
	print("Fixed Locations: ")
	print(fixed_locations)
	  
	## remove fixed location information from blif as to not interfere with other functions. 
	removeFixedLocationFromBlif(circuit_loc + '.blif')
	
	if not arch_file: arch_file = dirx + parseBlif(circuit_loc + '.blif')
	xarray = pbarray(len(chipStats().array.pattern),len(chipStats().array.pattern[0])) #initial import

	## Call first pass VTR
	print('/home/ubuntu/rasp30/vtr_release/vpr/vpr /home/ubuntu/ashes/ashes_fg/fpaa/arch/'+bs_board_arch+'_arch.xml ' + bs_circuit_loc  +'  -route_chan_width 17 -timing_analysis off -fix_pins ' + bs_circuit_loc + '.pads -nodisp')
	os.system('/home/ubuntu/rasp30/vtr_release/vpr/vpr /home/ubuntu/ashes/ashes_fg/fpaa/arch/'+bs_board_arch+'_arch.xml ' + bs_circuit_loc + '  -route_chan_width 17 -timing_analysis off -fix_pins ' + bs_circuit_loc + '.pads -nodisp')
		
	## Go through net and pair name - net using fixed_locations block names
	fixed_locations = extract_net_values('%s/%s.net'%(run_dir, circuit_name), fixed_locations)
	print(fixed_locations)
	
	## go through place and modify place file accordingly
	modifyPlaceFile('%s/%s.place'%(run_dir, circuit_name), fixed_locations)
	
	
	runVTR(arch_file, circuit_loc, pins_file, run_dir, vpr_disp)   

	parseNet('%s/%s.net'%(run_dir, circuit_name))
	parsePlace('%s/%s.place'%(run_dir, circuit_name))
	if (pins_file): parsePads(pins_file)
	parseRoute('%s/%s.route'%(run_dir, circuit_name))  #also generates global interconnect switch list
	genLISwcs()
	printSwcs('%s/%s.swcs'%(run_dir, circuit_name))
	saveCaps('%s/%s.caps'%(run_dir, circuit_name))
    
def extract_fixed_locations(blif_file):
	fixed_modules = []
	
	f = open(blif_file ,'r')	
	for line in f:
		words = line.split()
		if len(words):
			if words[0] == '.subckt':
				subckt = words[1] # on a block
				line_no_spaces = re.sub(r"\s+", "", line)
				fix_loc_x = re.search(r'fix_loc_x=(-?\d+)', line_no_spaces)
				fix_loc_y = re.search(r'fix_loc_y=(-?\d+)', line_no_spaces)
				fix_loc_enable = re.search(r'fix_loc_enabled\s*=\s*1', line)
				print("Fixed Loc Enable Result")
				print(fix_loc_enable)
				#print(fix_loc_enable.group(1))
				if fix_loc_enable:
					fixed_modules.append([subckt, fix_loc_x.group(1), fix_loc_y.group(1)])
	return fixed_modules
	
	
def extract_net_values(net_file, name_loc_array):
	new_array = []
	for block in name_loc_array:
		name = block[0]
		f = open(net_file ,'r')	
		for line in f:
			if name in line and not("open" in line): # check the block is present and not open
				# found the netx_x line
				net = re.search(r'name\s*=\s*"([^"]+)"', line)
				if not(net): print("NO NET FOUND FOR " + name)
				new_array.append([block[0], block[1], block[2], net.group(1)])
	return new_array

def modifyPlaceFile(place_file, locations_list):
	# store place file into lines
	with open(place_file, 'r') as f:
		lines = f.readlines()
	
	# go through modifications
	for mod in locations_list:
		net_name = mod[3]
		for i, line in enumerate(lines):
			if line.startswith(net_name):
				parts = line.split()
				# new x and new y
				parts[1] = str(mod[1])
				parts[2] = str(mod[2])
				lines[i] = ' '.join(parts) + '\n' # place line back together
	
	with open(place_file, 'w') as f:
		f.writelines(lines)		

def removeFixedLocationFromBlif(blif_file):

	with open(blif_file, 'r') as f:
		lines = f.readlines()
		
	for i in range(len(lines)):
		lines[i] = re.sub(r'&\s*fix_loc_[a-zA-Z0-9_]*\s*=\s*[^&]*', '', lines[i])
		print(lines[i])
	
	with open(blif_file, 'w') as file:
		file.writelines(lines)
		

def runVTR(arch_file, circuit, pins_file, run_dir, vpr_disp):
	DEBUG = 0
	vpr_loc = '/home/ubuntu/rasp30/vtr_release/vpr/vpr'
	chan_width = 17

	circuit_name = circuit.split('/')[-1]
	
	net_file   = '%s/%s.net'%(run_dir, circuit_name)
	place_file = '%s/%s.place'%(run_dir, circuit_name)
	route_file = '%s/%s.route'%(run_dir, circuit_name)


	exec_str = '%s %s -route %s '\
	%(vpr_loc, arch_file, circuit)


	'''
	if fixed_location>0:
		exec_str = '%s %s -route %s '\
		%(vpr_loc, arch_file, circuit)
	else:
		exec_str = '%s %s %s -net_file %s -place_file %s -route_file %s '\
		%(vpr_loc, arch_file, circuit, net_file, place_file, route_file )
	'''	
	if chan_width > 0: exec_str = exec_str + ' -route_chan_width %g'%(chan_width)
	if pins_file and fix_cab==0: exec_str = exec_str + ' -fix_pins %s'%(pins_file)   
	if vpr_disp == 0: exec_str = exec_str + ' -nodisp'
	if ff_custom >0: exec_str= exec_str + ' -timing_analysis off' #Michelle added on
	#exec_str= exec_str + ' -place_algorithm net_timing_driven -seed 20' #Michelle added this line

	print("genswcs - Call VRT: ")
	print(exec_str)
	if not DEBUG: call(exec_str.split())

def genLISwcs():
	for i in range(len(xarray.array)):
		for j in range(len(xarray.array[0])):
			csub = xarray.getSub(i,j)
			a=5
			if csub.type in ['CAB','CLB','CAB2']:
				csub.genLI()
				csub.genDevFgs()
				swcs.extend(csub.swcs)
			if csub.type in ['ioblock']:
				csub.genLI()
				csub.genDevFgs()  
				swcs.extend(csub.swcs)  
   
def genLocalInterconnectSwcs():
	# these two passes are for IO BLOCKS, not sure how to do this in one pass
	pin_types = dict()
	for block_name in pblocks.keys():
		block = pblocks[block_name]
		grid_loc  = block['grid_loc']
		tile_type = getTileType('CHANX', grid_loc)        
		if tile_type[:2] == 'io': 
			pin_types[block_name] = block['io type']

	for block_name in pblocks.keys():
		block = pblocks[block_name]        
		grid_loc  = block['grid_loc']
		tile_type = getTileType('CHANX', grid_loc)
		tile_loc  = getTileLoc('CHANX', grid_loc)
		print('~~~~~ LI for BLOCK: %s %s (%s %s) ~~~~~~'%(block_name, tile_type, grid_loc[0], grid_loc[1]))
		if tile_type[:2] == 'io':
			pin_nums = block['pin reorder']
			if pin_nums.keys() != []:
				for pin_block_name in pin_nums.keys():
					if pin_block_name in pin_types.keys(): pin_type = pin_types[pin_block_name]
					else: pin_type = pin_types['out:'+pin_block_name]
					pin_num = pin_nums[pin_block_name]
					#just have to connect pin_type to pin_num on tile_loc
					print(tile_type, tile_loc, pin_block_name, pin_num, pin_type,     
					pin_name = array[tile_type]['pin names'][int(pin_num)])                
					if 'buffer interconnect' in array[tile_type].keys():
						cur_swcs = array[tile_type]['buffer interconnect'][pin_type]
						for i in range(len(cur_swcs)):
							swc = getTileOffset(cur_swcs[i], tile_loc)
							swcs.append(swc)
							print(swc)        
					if 'local interconnect' in array[tile_type].keys():
						if pin_type in array[tile_type]['local interconnect']:
							sub_swc1 = array[tile_type]['local interconnect'][pin_type]
							sub_swc2 = array[tile_type]['local interconnect'][pin_name]
							swc = [sub_swc1[0]+sub_swc2[0], sub_swc1[1]+sub_swc2[1]]
							swc = getTileOffset(swc, tile_loc)
							swcs.append(swc)
							print(swc)
					print()
		if tile_type == 'cab':
			#local interconnect for cab device inputs and cab outputs
			for subblock in block['subblocks']:
				dev_name = subblock['instance']                
				inputs = subblock['rinputs'] #inputs = subblock['inputs']
				outputs = subblock['outputs'].strip()

				#input local interconnect switches for current dev
				input_num = 0
				for inputx in inputs:
					swc0_name = inputx                                #dev input name
					swc1_name = "%s.in[%s]"%(dev_name,input_num)    #dev input number
					input_num = input_num + 1
					swc0 = array[tile_type]['local interconnect'][swc0_name]
					swc1 = array[tile_type]['local interconnect'][swc1_name]
					swc = [swc0[0] + swc1[0], swc0[1] + swc1[1]] 
					print('%s --> %s (%g %g)'%(swc0_name, swc1_name, swc[0], swc[1]))

				#output local interconnect switches for current dev
				swc0_name = "%s.out[0]"%(dev_name)
				swc1_name = 'cab.O[%s]'%(block['outputs'].index(outputs))
				swc0 = array[tile_type]['local interconnect'][swc0_name]
				swc1 = array[tile_type]['local interconnect'][swc1_name]
				print('%s --> %s (%g %g)'%(swc0_name, swc1_name, swc[0], swc[1]))
	print(' ')       
                                                                
def printSwcs(file_name):
	f = open(file_name, 'w')  
	for i in range(-1,len(swcs)-1): 
		if swcs[i+1][1] in list(range(0x281,0x28F))+list(range(0x291,0x29F))+list(range(0x2A1,0x2AF))+list(range(0x2B1,0x2BF))+list(range(0x2C1,0x2CF))+list(range(0x2D1,0x2DF))+list(range(0x2E1,0x2EF))+list(range(0x2F1,0x2FF))+list(range(0x301,0x30F))+list(range(0x311,0x31F))+list(range(0x321,0x32F))+list(range(0x331,0x33F))+list(range(0x341,0x34F))+list(range(0x351,0x35F))+list(range(0x361,0x36F))+list(range(0x371,0x37F)):
			swcs[i+1].append(1);
			swcs[i+1].append(0);
		if swcs[i+1][0] in [22,25,26,29,30,33,102+22,102+25,102+26,102+29,102+30,102+33,136+22,136+25,136+26,136+29,136+30,136+33,238+22,238+25,238+26,238+29,238+30,238+33,272+22,272+25,272+26,272+29,272+30,272+33,374+22,374+25,374+26,374+29,374+30,374+33,408+22,408+25,408+26,408+29,408+30,408+33] and swcs[i+1][1] not in [272,288,304,320,336,352,368,384,400,416,432,448]:
			swcs[i+1].append(2); 
			swcs[i+1].append(0);
		else:
			swcs[i+1].append(0); 
			swcs[i+1].append(0);
		print('%s'%swcs[i+1])  
		f.write('%s %s %s %s'%(swcs[i+1][0],swcs[i+1][1],swcs[i+1][2],swcs[i+1][3] ) + '\n')
    
##########################
# USE IF USING C-CODE
##########################
def printSwcs2(file_name):
      
    row_str =  'unsigned int row[] = {%s'%swcs[0][0]
    for i in range(len(swcs)-1):        
        row_str = row_str + ',%s'%swcs[i+1][0]
    row_str = row_str + '};'

    col_str =  'unsigned int col[] = {%s'%swcs[0][1]
    for i in range(len(swcs)-1):        
        col_str = col_str + ',%s'%swcs[i+1][1]
    col_str = col_str + '};'
    
    num_str = 'unsigned int prog_list_size = %s;'%len(swcs) 
    
    rev_cols = []
    for i in range(len(swcs)):
        rev_cols.append(swcs[i][1])
    rev_cols = list(set(rev_cols))
    
    rev_str = 'unsigned int col_revtun[] = {%s'%rev_cols[0]
    for i in range(len(rev_cols)-1):
        rev_str = rev_str + ',%s'%rev_cols[i+1]
    rev_str = rev_str + '};'
    
    rev_num = 'unsigned int revtun_list_size = %s;'%len(rev_cols)
    
    print(row_str)
    print(col_str)
    print(num_str)
    print(rev_str)
    print(rev_num)
    
    f = open(file_name, 'w')
    f.write(row_str + '\n')
    f.write(col_str + '\n')
    f.write(num_str + '\n')
    f.write(rev_str + '\n')
    f.write(rev_num + '\n')
    
def saveCaps(file_name):
	
	cap_nams.pop(0)
	cap_vals.pop(0)
	f = open(file_name, 'w')
	
	for i in range(0,len(cap_nams)):
		f.write('%s, %.3e'%(cap_nams[i].strip('()'), cap_vals[i]) + '\n')

def getTileOffset(swc, block):
	#block = tile_loc
	DEBUG = 0
	if DEBUG:
		return swc
	else:
		return arrayStats_used().getTileOffset(swc, block)

def getSwcSswitch(direction, track, grid_loc, net_name):
	VERBOSE = 1
	if cap_nams[-1] != net_name:
		cap_nams.append(net_name)
		cap_vals.append(38e-15)
	else:
		cap_vals[-1] = cap_vals[-1]+38e-15
	if cap_seq[-1] == 2:
		cap_vals[-1] = cap_vals[-1]+160e-15
	cap_seq.append(2)
	tile_type = getTileType('SBLOCK', grid_loc)
	tile_loc  = getTileLoc('SBLOCK', grid_loc)

	#get direction partial switch
	#sub_swc1 = array[tile_type]['SBLOCK'][direction]
	sub_swc1 = chipStats().get(tile_type).get('sblock')[direction]

	#get track partial switch
	track_name = 'T' + track
	#sub_swc2 = array[tile_type]['SBLOCK'][track_name]
	sub_swc2 = chipStats().get(tile_type).get('sblock')[track_name]

	#switch address based on direction then adding a track based offset
	swc = [sub_swc1[0] + sub_swc2[0], sub_swc1[1] + sub_swc2[1]]

	#add block offset
	swc = getTileOffset(swc, tile_loc)

	if VERBOSE==1 or VERBOSE>1:        
		print('%s [%s,%s] SBLOCK %s (%s %s)' % (tile_type, str(tile_loc[0]).rjust(2), str(tile_loc[1]).rjust(2), direction, str(swc[0]), str(swc[1])))
	if VERBOSE>1 :
		print('%s %s %s' % (tile_loc,grid_loc,tile_type))
	return swc
    
#&&&&&&&&&&&&&&&&&
# C-block switch generation
#&&&&&&&&&&&&&&&&&
def getSwcCblock(pin_num, pin_grid_loc, cblock_type, track, cblock_grid_loc, net_name, c_outin):
	if cap_nams[-1] != net_name:
		cap_nams.append(net_name)
		cap_vals.append(160e-15)
	elif cap_nams[-1] == net_name and c_outin == 0:
		cap_vals[-1] = cap_vals[-1]+160e-15
	cap_seq.append(1)
	VERBOSE = 1 #0,1,2
	VERBOSE2=1
	#cblock location and tile type
	cblock_tile_type = getTileType(cblock_type, cblock_grid_loc)  #where the CBLOCK is
	cblock_tile_loc  =  getTileLoc(cblock_type, cblock_grid_loc)  #where the CBLOCK is

	#pin location and tile type -- pin loc independent of block type
	pin_tile_type = getTileType('CHANX', pin_grid_loc) #where the pin (source or sink) is WAS HARDCODED TO CHANX before::
	pin_tile_loc  =  getTileLoc(cblock_type, pin_grid_loc)

	if VERBOSE2>1 :
		print("@@***********")
		print("pin_tile_loc :%s"  %(pin_tile_loc))
		print("pin_tile_type :%s"  %(pin_tile_type))
		print("cblock_tile_loc: %s" %(cblock_tile_loc))
		print("cblock_grid_loc:"+str(cblock_grid_loc))
		print(("cblock_tile_type:"+str(cblock_tile_type)))
	pin_num = int(pin_num)  
	pin_name = chipStats().get(pin_tile_type).pin_order[pin_num]

	if rasp3a == 0:
		if cblock_tile_type == 'io_e':
			print("**")
		# A-A and D-D case
		elif cblock_grid_loc[0] in [3,5,7,9,11] and cblock_tile_loc != pin_tile_loc and (pin_tile_loc[0]-cblock_tile_loc[0] !=1) and cblock_type=='CHANY':
			if pin_name[0] != 'X':
				print("lala-land")
		elif cblock_tile_type != pin_tile_type: 
			pin_name = 'X' + pin_name
			if pin_tile_type=='clb' and cblock_tile_type in ['cab','cab2']:
				pin_name='D'+pin_name
			elif pin_tile_type in ['cab','cab2'] and cblock_tile_type in ['clb']:
				pin_name='A'+pin_name
		elif cblock_tile_loc != pin_tile_loc:
			pin_name = 'X' + pin_name
		##we need to add X for C-blocks in ## super--kludge$$ might not need it anymore
		elif cblock_grid_loc[0] in [5,9,12] and cblock_tile_type in ['cab','cab2'] :
			if pin_name[0] != 'X':
			   pin_name ='X' + pin_name
			print("lala-land")
		elif cblock_grid_loc[0] in [0,3,7,11] and cblock_tile_type== 'clb' :
			if pin_name[0] != 'X':
				pin_name = 'X' + pin_name
			print("lala-land2")
	elif rasp3a == 1:
		if cblock_tile_type == 'io_e':
			print("yeehaaa!")
		elif cblock_tile_type != pin_tile_type: 
			pin_name = 'X' + pin_name
			if pin_tile_type=='clb' and cblock_tile_type in ['cab','cab2']:
				pin_name='D'+pin_name
			elif pin_tile_type in ['cab','cab2'] and cblock_tile_type in ['clb']:
				pin_name='A'+pin_name
		elif cblock_grid_loc[0] in [0,2,4,6] and cblock_tile_type in ['cab','cab2'] :
			if pin_name[0] != 'X':
			   pin_name ='X' + pin_name
			print("lala-land")
		elif cblock_tile_loc != pin_tile_loc:
			pin_name = 'X' + pin_name
		elif cblock_grid_loc[0] in [1,3,5] and cblock_tile_type== 'clb' :
			if pin_name[0] != 'X':
				pin_name = 'X' + pin_name
			print("lala-land2")
	track_name = 'T' + track
    
	#switch address is bassed on a crossbar network, pick location that
	# corresponds to net1 on one side and net2 on the other
	#sub_swc1 = array[cblock_tile_type][cblock_type][track_name]
	try:
		sub_swc1 = chipStats().get(cblock_tile_type).get(cblock_type)[track_name]
	except:
		pdb.set_trace()
	#sub_swc2 = array[cblock_tile_type][cblock_type][pin_name]
	if VERBOSE2>1 :print("!!***********")
	if VERBOSE2>1 :print(pin_name)
	if VERBOSE2>1 :print(cblock_type) 
	if VERBOSE2>1 :print(cblock_tile_type)
	try:
		sub_swc2 = chipStats().get(cblock_tile_type).get(cblock_type)[pin_name]
	except:
		pdb.set_trace()
	swc = [sub_swc1[0] + sub_swc2[0], sub_swc1[1] + sub_swc2[1]]

	#add block offset
	swc = getTileOffset(swc, cblock_tile_loc)

	if VERBOSE:
		print("%s [%s,%s] %s  (%s,%s) %s %s" % (cblock_tile_type.rjust(4), str(cblock_tile_loc[0]).rjust(2), str(cblock_tile_loc[1]).rjust(2), cblock_type, str(swc[0]), str(swc[1]), track_name, pin_name)) 
	if VERBOSE > 1:
		print("CBLOCK swc: ")
		print(cblock_type + ' <--> ' + pin_tile_type + ' ')
		print(cblock_type + ' in ' + str(cblock_grid_loc[0]) + ' ' + str(cblock_grid_loc[1]))
		print('on TRACK ' + str(track) + ' to pin ' + str(pin_num))
		print('in block ' + str(pin_grid_loc[0]) + ' ' + str(pin_grid_loc[1]))
	return swc
    
def getBlockName(grid_loc):
	for block_name in pblocks.keys():
		block = pblocks[block_name]
		if block['grid_loc'] == grid_loc or block['grid_loc'] == [str(grid_loc[0]), str(grid_loc[1])]:
			return block_name
	return 'not found'

def getTileType(block_type, grid_loc):
	#returns: cab, cab2, clb, io_w, io_e, io_n, io_s, or tile_se
	tile_loc = getTileLoc(block_type, grid_loc) #&&&
	#return array['pattern'][int(tile_loc[0])][int(tile_loc[1])]
	return arrayStats_used.pattern[int(tile_loc[0])][int(tile_loc[1])]

def getTileLoc(block_type, grid_loc):
	#this translates the vpr grid location to a physical schematic tile location
	#returns tile_loc [x,y]
	#ex. getTileLoc('CHANY',[1,1]) -> [0,1]
	#ex. getTileLoc('CHANX',[1,1]) -> [1,1]

	#tile_loc = list(grid_loc)	
	tile_loc = [int(grid_loc[0]), int(grid_loc[1])]
	if block_type in ['CHANY','SBLOCK']: #and tile_loc[0] != 0: ## removed CHANY and SBLOCK as option
		tile_loc[0] = tile_loc[0] + 1 #&&& should be +1 dodo ...hmmm
	return tile_loc

def parseNet(file_name):
	xmlData = etree.parse(file_name)
	blocks = xmlData.findall("block") #first level
	verbose=0

	for block in blocks:        
		block_name = block.attrib["name"]
		block_type = block.attrib['mode']

		input_str = block.findall('inputs')[0].findall('port')[0].text
		inputs = input_str.split()

		output_str = block.findall('outputs')[0].findall('port')[0].text
		outputs = output_str.replace('->crossbar', ' ').split()
        
		#        nb = complexBlock(block_name, block_type)
		if block_type == 'cab':
			nb = cab(block_name)
		elif block_type == 'clb':
			nb = clb(block_name)
		elif block_type == 'cab2':
			nb = cab2(block_name)
		else:
			nb = complexBlock(block_name, block_type)
		nb.inputs = inputs      
		if block_type in ['cab', 'clb', 'cab2']:  
			# add if counter8
			# make ble[0] then variable containing ble[1-7]
			# for each ble make a kk list of clb.dev_fgs for counter support
			# run through similar switch generation as normal lut/ff
			#start adding subblocks to block
			#only getting subblock type, position, and output name
			#will update input names later
			counter_flag = 0
			subblocks = block.findall("block")
			for subblock in subblocks:                
				sub_outputs = subblock.attrib["name"]
				sub_inst = subblock.attrib["instance"]  
				if (sub_inst[:-3] == 'counter8') & (sub_outputs != 'open'):
					counter_flag = 1
					for blenum in range(8):
						sub_output = subblock.findall("outputs")[0].findall("port")[0].text
						sub_output = sub_output.split(" ")
						sub_output = sub_output[blenum]
						sub_inst = 'ble['
						sub_inst += str(blenum)
						sub_inst += ']'
						print(sub_output)
						print(sub_inst)
						if blenum == 0:
							cover = ['ff_in', 'ff_out','res_g']
						else:
							cover = ['ff_in', 'clk_a', 'ff_out','res_g']
						nsb = pblock(sub_inst, 'lut')
						nsb.ex_fgs = cover	
						nsb.inputs_orig = ['temp']
						nsb.inputs = ['temp']
						nsb.outputs = ['temp']
						nb.addSub(nsb, sub_inst)
				elif sub_outputs != "open": 
					sub_input_str  = subblock.findall("inputs")[0].findall("port")[0].text
					sub_inputs = sub_input_str.replace('->crossbar', ' ').split()
					#special handling for BLEs / LUTs.  grabbing cover
					if sub_inst[:3] == 'ble':
						sub3blks=subblock.findall('block')
						for sub3blk in sub3blks:
							sub3_inst = sub3blk.attrib["instance"] 
							sub3_outputs = sub3blk.attrib["name"]                        
							if sub3_inst[:-3] =='soft_logic': ##can't use the latch standalone
								cover = luts[sub3_outputs].cover     #index luts by name == output
								nsb = pblock(sub_inst, 'lut')
								nsb.ex_fgs = cover                   #LUT cover comes from blif parsing
								nsb.inputs_orig = luts[sub3_outputs].inputs
						mux_use = subblock.findall('outputs')[0].findall('port')[0].text[0:2]
						if mux_use == 'ff':
							nsb.ex_fgs.append('res_g')
							nsb.ex_fgs.append('ff_out') # add flip flop covers
							sub_outputs = subblock.findall('block')[2].attrib["name"]						
					else:
						nsb = pblock(sub_inst, '%s_dev'%block_type)
						if sub_outputs in ex_fgs_dict.keys(): 
							nsb.ex_fgs = ex_fgs_dict[sub_outputs]
					if nsb.name =="SR4[0]":
						sub_outputs=subblock.findall("outputs")[0].findall("port")[0].text.split()
					if nsb.name =="vmm4x4[0]":
						sub_outputs=subblock.findall("outputs")[0].findall("port")[0].text.split()
					if nsb.name in ["mite2[0]", "signalmult[0]","hhneuron[0]",'ramp_fe[0]','hhn_debug[0]','SubbandArray[0]','HH_RG[0]','HH_RG_2s[0]','HH_RG_3s[0]','vmm_offc[0]']:
						sub_outputs=subblock.findall("outputs")[0].findall("port")[0].text.split()
					nsb.inputs = sub_inputs	
					nsb.outputs = sub_outputs
					print(nsb.outputs)
					nb.addSub(nsb, sub_inst)
					if verbose: print(nb.inputs)
					print(nb.outputs)
			#now that we have all subblocks, with all of their output names
			# we can go and update the input names 
			if counter_flag == 0:
				for i in range(len(nb.subblocks)):
					cur_sub = nb.getSub(i)
					sub_inputs = cur_sub.inputs
					sub_input_names = []
					for i in range(len(sub_inputs)):
						cur_input = sub_inputs[i]                        
						if cur_input.split('.')[0] == block_type:           #input from complex block input
							in_num = int(cur_input.split('[')[-1].split(']')[0]) #cab.I[13] -> 13
							sub_input_names.append(nb.inputs[in_num])                          
						elif cur_input == 'open':                                  
							sub_input_names.append('open')
						else:     
							sub_input_names.append(nb.getSub(cur_input.split('.')[0]).outputs)
					cur_sub.inputs = sub_input_names
					if verbose: print(cur_sub.inputs)        
				output_net_names = outputs
				net_num=0
				for i in range(len(outputs)):
					if outputs[i] != 'open':
						from_sub_name = outputs[i].split('.')[0] #ota[0].out[0] -> ota[0]
						if from_sub_name ==['SR4[0]']:
							try:
								if i<4:
									output_net_names[i]=nb.getSub(from_sub_name).outputs[i]
								else:
									output_net_names[i]=nb.getSub(from_sub_name).outputs[i]
							except:
								pdb.set_trace()
						elif from_sub_name =='vmm4x4[0]':
							try:
								if i<5:
									output_net_names[i]=nb.getSub(from_sub_name).outputs[i]
								else:
									pdb.set_trace()
									output_net_names[i]=nb.getSub(from_sub_name).outputs[i]
							except:
								pdb.set_trace()
						elif from_sub_name in ['mite2[0]','signalmult[0]','hhneuron[0]','ramp_fe[0]','hhn_debug[0]','SubbandArray[0]','HH_RG[0]','HH_RG_2s[0]','HH_RG_3s[0]','vmm_offc[0]']:
							try:
								output_net_names[i]=nb.getSub(from_sub_name).outputs[net_num]
								net_num=net_num+1 # omcrement net number
								if net_num == len(sub_outputs):
									net_num=0
							except:
								pdb.set_trace()
						else:
							output_net_names[i] = nb.getSub(from_sub_name).outputs
				nb.outputs = output_net_names
				if verbose: print(nb.outputs)    
		elif block_type in ['inpad', 'outpad']:
			nb.type = 'ioslice_%s'%block_type    #global pblocksblock_type
			nb.outputs = block_name
			nb.inputs[0] = block_name
		nb.portorder = range(len(nb.inputs)+len(nb.outputs))
		nblocks[nb.name] = nb
                              
def parsePlace(file_name):
	global xarray
	f = open(file_name, 'r')
	go = False
	for line in f:
		words = line.split()
		if go:
			grid_loc = [int(words[1]), int(words[2])]
			sub_num = int(words[3])
			block_name = words[0]
			new_block = nblocks[block_name]
			new_block.grid_loc = grid_loc
			#if tile is empty: xarray.addSub(grid_loc, new_block
			#if tile is not empty: xarray.getSub(grid_loc).addSub(new_block)
			if xarray.getSub(grid_loc).type == []:
				if new_block.type[:7] == 'ioslice':
					xarray.addSub(ioblock(block_name), grid_loc)
				else:
					xarray.addSub(new_block, grid_loc)
			if new_block.type[:7] == 'ioslice':
				xarray.getSub(grid_loc).addSub(new_block, sub_num)
				# $$PROBLEM: setting port numbers for ioblocks is super hardcoded here! i blame VPR!
				if new_block.type[8:] == 'inpad':
					xarray.getSub(grid_loc).setPort(sub_num*3+1, block_name) #setting output port
				else:
					xarray.getSub(grid_loc).setPort(sub_num*3+0, block_name) #setting input port
		if len(words) and words[0] == "#----------":
			go = True
            
def parsePads(file_name):
	f = open(file_name, 'r')
	for line in f:
		words = line.split()        
		if len(words) !=0:
			grid_loc = [int(words[1]), int(words[2])]
			sub_num = int(words[3])
			io_type = words[-1]
			try:
				xarray.getSub(grid_loc).getSub(sub_num).type = io_type
			except:
				print('oops')
				print(words)
				pdb.set_trace()
  
#***********************************
# Pre-parse blif file for different architecture types
#***********************************      
def parseBlif(file_name):
	f = open(file_name ,'r')
	get_cover = 0
	new_lut = 0
	macroblk=0
	for line in f:
		words = line.split()
		if len(words):
			if words[0] == '.subckt':
				subckt = words[1]
				print('%s %s'%(words[0], subckt))


				#count vmm type and num
				if subckt in ['hyst_diff']: macroblk=macroblk+1
				#a = '.subckt ota in[1] = i4  out=o3 # ota_bias 0.9 ota_p_bias 0.5 ota_n_bias 0.5'
				dev_type = line.split(' ')[1]

				if len(line.split('#')) > 1:
					ex_fgs = line.split('#')[1].rstrip() # parameters after # in .blif file. 
				else:
					ex_fgs = 0

				ports = []
				for i in line.split('=')[1:]:
					port = i.lstrip().split(' ')[0].rstrip()
					ports.append(port)
				print("Ports: ")
				print(ports)               
                #key = dev_type + ' ' + ' '.join(ports) # this key is type + port list
				if subckt in ['lpf_2','meas_volt_mite','cap','ota_buf','ota_buffer','lpf','nfet_i2v','pfet_i2v','i2v_pfet_gatefgota','nmirror','TIA_blk']: ## single i/ps
					key = ports[1] #this key is just output port name ## for all cases with a single i/p- o/p
				elif subckt in ['DAC_sftreg','latch_custom','sftreg2','mmap_local_swc','in2in_x1','mismatch_meas','mite']: #3 i/ps
					key=ports[3]
				elif subckt in ['gnd_out','vdd_out','ichar_nfet','ramp_fe']: #2 i/ps
					key=ports[2]
				elif subckt in ['SR4','vmm4x4','signalmult','hhneuron','sftreg3','sftreg4']: #4 i/ps
					key=ports[4]
				elif subckt in ['vmm4x4_SR']: #7 i/ps
					key=ports[7]
				elif subckt in ['vmm4x4_SR2','tgate_so']: #8 i/ps
					key=ports[8]
				elif subckt in ['vmm8inx8in']: #17 i/ps
					key=ports[17]
				elif subckt in ['vmm8x4_SR']: #11 i/ps ,
					key=ports[11]
				elif subckt in ['vmm12x1_wowta']: #12 i/ps ,
					key=ports[12]
				elif subckt in ['vmm8x4','vmm8x4_in','in2in_x6','vmm12x1']: #13 i/ps ,
					key=ports[13]
				elif subckt in ['sftreg']: #19 i/ps ,'sftreg'
					key=ports[19]
				elif subckt in ['Hyst_diff']:
					key=ports[1]
				elif subckt in ['Max_detect']:
					key=ports[1]
				elif subckt in ['Min_detect']:
					key=ports[1]
				elif subckt in ['hhn']:
					key=ports[4]
				elif subckt in ['fgswitch']:
					key=ports[1]
				elif subckt in ['common_drain']:
					key=ports[1]
				elif subckt in ['common_drain_nfet']:
					key=ports[1]
				elif subckt in ['hhn_debug']:
					key=ports[4]
				elif subckt in ['wta_new']:
					key=ports[3]
				elif subckt in ['common_source']:
					key=ports[1]
				elif subckt in ['VolDivide1']:
					key=ports[1]
				elif subckt in ['I_SenseAmp']:
					key=ports[2]
				elif subckt in ['nmirror_w_bias']:
					key=ports[2]
				elif subckt in ['SubbandArray']:
					key=ports[2]
				elif subckt in ['HH_RG']:
					key=ports[5]
				elif subckt in ['HH_RG_2s']:
					key=ports[6]
				elif subckt in ['HH_RG_3s']:
					key=ports[7]
				elif subckt in ['SOSLPF']:
					key=ports[1]
				elif subckt in ['MSOS02']:
					key=ports[1]
				elif subckt in ['vmm_offc']:
					key=ports[13]
				elif subckt in ['C4_BPF']:
					key=ports[2]
				else:
					key = ports[2] #this key is just output port name
				if ex_fgs:
					ex_fgs_dict[key] = ex_fgs 
				print(subckt)           
                
			elif words[0] == '.names':
				ff_custom=1
				get_cover = 1       
				new_lut = 1
				lut_outputs = words[-1]
				lut_inputs = words[1:-1]
				#cl = lut(lut_outputs) #yah, it's name is defined by it's single output net name. deal with it.
				cl = pblock(lut_outputs, 'lut')
				cl.inputs = lut_inputs
				cl.outputs = lut_outputs
				cl.cover = []
                
			elif get_cover:
				cl.cover.append(words[0])
		else:                               #blank line  
			if new_lut:
				luts[cl.name] = cl
				get_cover = 0
				new_lut = 0
	# print 'vmm types: 4x4, 8x8, 12x12, 16x16: %g %g %g %g'%(num_4x4, num_8x8, num_12x12, num_16x16)
            
	arch_file = './arch/rasp3_arch.xml'
	#if rasp3a > 0:   arch_file = '/home/ubuntu/rasp30/vpr2swcs/arch/rasp3a_arch.xml'
	if rasp3a > 0:   arch_file = 'arch/rasp3a_arch.xml'
	return arch_file  
            
            
def parseRoute(file_name):
	global groutes
	global xarray

	VERBOSE = 1
	groutes = list()
	f = open(file_name, 'r')

	for line in f:
		words = line.split()
		cur = words
		if len(cur):
			if cur[0] == "Net" and cur[2]!="(gnd):":
				del cap_seq[:]
				if 'new_route' in locals():
					groutes.append(new_route)
				net_name = words[2]
				new_route = dict()
				new_route['name'] = net_name
				new_route['num'] = words[1]
				new_route['connections'] = list()
				last = []
				lastlast = []
				if VERBOSE: print(" ------------- " + words[2] + " ------------- ")
			elif cur[0] in ['SOURCE']:
				source=cur
				source[0]='CHANX'
				source_pin=int(cur[3])
			elif cur[0] in ['SINK']:
				continue
			elif cur[0] in ['OPIN','CHANX','CHANY','IPIN']:
				try:
					tile_t=int(cur[3])
				except:
					tile_t=int(cur[5])
				if last:
					cgl = [int(i) for i in cur[1][1:-1].split(',')] #current grid location
					lgl = [int(i) for i in last[1][1:-1].split(',')] #last grid location
					if lastlast != []:
						if lastlast[0] == 'OPIN' and last[0] == 'CHANX' and cur[0] == 'IPIN':
							if lastlast[1] == last[1] and last[1] == cur[1]:
								c_outin = 1
							else:
								c_outin = 0
						else:
							c_outin = 0
					else:
						c_outin = 0
					pin_num = -1
					if cur[0] == 'IPIN':
						pin_num = tile_t
					elif last[0] == 'OPIN':
						pin_num = int(last[3]) 
					elif last[0] == 'SINK':
						pin_num = int(last[3]) # special case

					#connection = last[0] + " " + last[1] + " --> " + cur[0] + " " + cur[1]
					connection = "%s %s --> %s %s" % (last[0].rjust(5), last[1].rjust(6), cur[0].rjust(5), cur[1].rjust(6))
					if cur[0][:-1] == 'CHAN':
						connection = connection + " T/P: " + cur[3].rjust(2) + ' ' + str(pin_num).rjust(2)
					else:
						connection = connection + " T/P: " + last[3].rjust(2) + ' ' + str(pin_num).rjust(2)
                        
					new_route['connections'].append(connection)                   
					if VERBOSE: print('| ' + connection + ' |')

					# add switch address -- lets keep this clean shall we?
					if last[0][:-1] == 'CHAN' and cur[0][:-1] == 'CHAN':
						#SBLOCK connection: CHAN to CHAN
						block_dir = [int(cgl[0])-int(lgl[0]), int(cgl[1])-int(lgl[1])]
						track = cur[3]
						if last[0] == 'CHANY':
							if cur[0] == 'CHANY':
								if block_dir == [0,1]:
									swc = getSwcSswitch('sn', track, lgl, new_route['name'])
								else:
									swc = getSwcSswitch('ns', track, cgl, new_route['name'])
							elif cur[0] == 'CHANX':
								if block_dir == [0,0]:
									swc = getSwcSswitch('sw', track, lgl, new_route['name'])
								elif block_dir == [1,0]:
									swc = getSwcSswitch('se', track, lgl, new_route['name'])
								elif block_dir == [0,-1]:
									swc = getSwcSswitch('nw', track, cgl, new_route['name'])
								elif block_dir == [1,-1]:
									swc = getSwcSswitch('ne', track, [lgl[0],lgl[1]-1], new_route['name']) #
								else:
									print("SBLOCK switch error")
									print(block_dir)
									pdb.set_trace()
						elif last[0] == 'CHANX':
							if cur[0] == 'CHANX':
								if block_dir == [1,0]:
									swc = getSwcSswitch('we', track, lgl, new_route['name'])
								else:
									swc = getSwcSswitch('ew', track, cgl, new_route['name'])
							if cur[0] == 'CHANY':
								if block_dir == [0,1]:
									swc = getSwcSswitch('wn', track, lgl, new_route['name'])
								elif block_dir == [0,0]:
									swc = getSwcSswitch('ws', track, lgl, new_route['name']) # can be lgl or cgl
								elif block_dir == [-1,0]:
									swc = getSwcSswitch('es', track, cgl, new_route['name']) 
								elif block_dir == [-1,1]:
									swc = getSwcSswitch('en', track, [cgl[0],cgl[1]-1], new_route['name'])
								elif block_dir == [1,0]:
									swc = getSwcSswitch('se', track, lgl, new_route['name']) #%%
								elif block_dir == [0,-1]: ##special case when branching...so create CHANY->CHANY case
									swc = getSwcSswitch('sn', track, cgl, new_route['name'])
								else:
									print("SBLOCK switch error")
									print(block_dir)
									pdb.set_trace()     
					elif last[0] == 'OPIN' and cur[0][:-1] == 'CHAN':
						block_dir = [int(cgl[0])-int(lgl[0]), int(cgl[1])-int(lgl[1])]
						track = cur[3]

						#CBLOCK connection from source: CAB/CLB/IO -> CBLOCK
						if cur[0] == 'CHANX':
							swc = getSwcCblock(last[3], lgl, 'CHANX', track, cgl, new_route['name'], c_outin)
						elif cur[0]== 'CHANY':
							if block_dir ==[0,0]:
								swc = getSwcCblock(last[3], [cgl[0],cgl[1]], 'CHANY', track, cgl, new_route['name'], c_outin) # &&removed as pin_grid update
							else:		
								swc = getSwcCblock(last[3], lgl, 'CHANY', track, cgl, new_route['name'], c_outin) 

					elif last[0][:-1] == 'CHAN' and cur[0] == 'IPIN':
						track = last[3]
						block_dir = [int(cgl[0])-int(lgl[0]), int(cgl[1])-int(lgl[1])]
						#CBLOCK connection to sink: CHAN to CBLOCK
						if last[0] == 'CHANX':
							swc = getSwcCblock(tile_t, cgl, 'CHANX', track, lgl, new_route['name'], c_outin)
						else:
							swc = getSwcCblock(tile_t, cgl, 'CHANY', track, lgl, new_route['name'], c_outin)
						print ('~~~~ PIN SINK ~~~~ || net %s -> pin %s in %s %s'%(new_route['name'], cur[3], cgl[0], cgl[1]))

						#update pin order
						xarray.getSub(int(cgl[0]),int(cgl[1])).movePort(new_route['name'][1:-1], tile_t)

					if VERBOSE: print ('SWC ')
					swcs.append(swc)

				if cur[0] == 'IPIN': #$$ add the pin number for 
					last = []
					pin_loc = cur[3]
				else:
					lastlast = last
					last = cur 

	#done parsing file, add last route     
	groutes.append(new_route)

if __name__ == "__main__":
	main(c, d, a, v, p)
                

            

    
