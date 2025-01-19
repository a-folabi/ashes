import pdb
from ashes_fg.fpaa.genu import *

class rasp30a(stats):
	def __init__(self):
		self.array = arrayStats()
		self.cab = cabStats()
		self.cab2 = cab2Stats()
		self.clb = clbStats()
		self.io_sd = iosdStats()
		self.io_w = iowStats()
		self.io_sa = iosaStats()
		self.io_e = ioeStats()
		self.io_el = ioelStats()
		self.io_na= ionaStats()
		self.io_nd= iondStats()
		
class arrayStats(stats):
	arch_file = './arch/rasp3a_arch.xml'
	pattern = [
		[[], 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', 'io_w', []], 
		['io_sa', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'io_na'],
		['io_sd', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'io_nd'],
		['io_sa', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'io_na'],
		['io_sd', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'io_nd'],
		['io_sa', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'cab', 'io_na'],
		['io_sd', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'clb', 'io_nd'],
		['io_sa', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'cab2', 'io_na'],
		['io_el', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e', 'io_e',[]]]

	def __init__(self):
		DEBUG = 0
		x_pattern = []
		for i in range(len(self.pattern)):
			x_pattern.append(self.pattern[i][1])
		y_pattern = self.pattern[1]

		if DEBUG:
			for j in reversed(range(len(pattern))):
				for i in range(len(pattern[j])):
					print (str(pattern[i][j]).rjust(6),)
				print ()

		#y offset is not higher order bits, but the lower bits
		#base addresses for y are the higher order bits
		#also we can't count the first clb
		#y offset:: col<3:0> while using in col 
		addrs = {'y':{'io_sa':1, 'cab':1, 'io_na':1,'io_nd':1}, 'x':{'io_w':0, 'clb':68,'cab':68,'cab2':68, 'io_e':34}}

		self.x_offsets = [0]
		self.x_offsets.append(0) # this and the [2:] are to skip the first CLB
		#!!! check the x-offsets
		for x_type in x_pattern[2:]:
			self.x_offsets.append(self.x_offsets[-1] + addrs['x'][x_type])
		self.y_offsets = [0]
		for y_type in y_pattern[1:]:
			self.y_offsets.append(self.y_offsets[-1] + addrs['y'][y_type])
            
	def getTileOffset(self, swc, grid_loc):      
		DEBUG = 0
		x = grid_loc[0]
		y = grid_loc[1]
		if DEBUG:
			return [999, 999]
		else:
			return [swc[0]+self.x_offsets[x]+34, swc[1]*2**4+self.y_offsets[y]] #kludge / hardcoded 2**4 part, fix this!

###########################################
#   CAB stats 
###########################################   
class cabStats(stats):
	def __init__(self):
		self.num_inputs = 16
		self.num_outputs = 24 #8+4
		# order is I[0:15] then si[0:3] O[0:7] so[0:12]  where si==O and so==I
		self.pin_order =['I0','I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','I14','I15','O0','O1','O2','O3','O0','O1','O2','O3','O4','O5','O6','O7','I0','I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11']	

		#CHANX--C BLOCK ---y axis of adjacent CAB
		# these are the decoder mapped addrs
		#chanx_sm = ['T[0:16]', [range(22,13,-1)+range(12,8,-1)+range(7,3,-1),0],### flipping chanx and chany ####
		chanx_sm = ['T[0:16]', [list(range(22,15,-1))+list(range(14,8,-1))+list(range(7,3,-1)),0],
			'I8',   [ 0,36],     #pin names
			'I9',   [ 0,37],
			'I13',  [ 0,38],
			'I14',  [ 0,39],
			'I15',  [ 0,40],
			'O4',   [ 0,41],
			'XI10', [ 0,42],
			'XI11', [ 0,43],
			'XI12', [ 0,44],
			'XO5',  [ 0,45],
			'XO6',  [ 0,46],
			'XO7',  [ 0,47]]
		self.chanx = smDictFromList(chanx_sm, 'remBrak')
            
		# CHANY  --x axis block of original  
		#chany_sm = ['T[0:16]', [range(22,13,-1)+range(12,8,-1)+range(7,3,-1),0],
		chany_sm = ['T[0:16]', [list(range(22,15,-1))+list(range(14,8,-1))+list(range(7,3,-1)),0],
			'I4',   [ 0,65],    #pin names
			'I5',   [ 0,66],
			'I6',   [ 0,67],
			'I7',   [ 0,68],
			'O2',   [ 0,69],
			'O3',   [ 0,70],
			'XO0',  [ 0,63],
			'XO1',  [ 0,64],
			'XI0',  [ 0,59],
			'XI1',  [ 0,60],
			#'XI2',  [ 0,61],## problem conflict might not need as no longer have A-A case $$$$$
			'XI3',  [ 0,62],
			'DXI2', [ 0,65],#------to match w/ dif DIgital tile NAME BUT ANALOG TILE MAPPING
			'DXI6',  [ 0,66], #to match w/ dif tile
			'DXI10', [ 0,67],#to match w/ dif tile
			'DXI14', [ 0,68],
			'DXO2',  [ 0,69],
			'DXO6',  [ 0,70],
			'XI2', [ 0,65],#------to match w/ dif DIgital tile NAME BUT ANALOG TILE MAPPING edge case for I/O block $$$$$$
			'XI6',  [ 0,66], #to match w/ dif tile
			'XI10', [ 0,67],#to match w/ dif tile
			'XI14', [ 0,68],
			'XO2',  [ 0,69],
			'XO6',  [ 0,70]]
			#'XO3',	[0,70]]  # $$ XO<0,4>??
		self.chany = smDictFromList(chany_sm, 'remBrak')

		# SBLOCK            
		#sb_sw = ['T[0:16]', [range(22,13,-1)+range(12,8,-1)+range(7,3,-1), 0],
		sb_sw = ['T[0:16]', [list(range(22,15,-1))+list(range(14,8,-1))+list(range(7,3,-1)), 0],
			'we',   [ 0,54],#actual ns    #track direction (these are rotated 90deg ccw from schematic name: ww->W)
			'wn',   [ 0,51],#ne                     
			'ws',   [ 0,50],#nw                     
			'ns',   [ 0,52], #ew                     
			'ne',   [ 0,53],#es                     
			'es',   [ 0,49],                     
			'ew',   [ 0,54],#ns                     
			'nw',   [ 0,51],                     
			'sw',   [ 0,50],                     
			'sn',   [ 0,52],                     
			'en',   [ 0,53],                     
			'se',   [ 0,49]]    
		self.sblock = smDictFromList(sb_sw, 'remBrak')  

		#Local Interconnect
		li_sm_0a = ['gnd','vcc','cab.I[0:15]']
		# outputs order into the CAB   ## order is very important here
		li_sm_0b = ['fgota[0].out[0]','ota_buf[0].out[0]','ota[0].out[0]','cap[0].out[0]','nfet[0].out[0]','pfet[0].out[0]','tgate[0].out[0]','nmirror[0].out[0]','c4_sp[0].out[0]','gnd_out[0].out[0]','vdd_out[0].out[0]','in2in_x1[0].out[0]','in2in_x6[0].out[0]','lpf[0].out[0]','nfet_i2v[0].out[0]','pfet_i2v[0].out[0]','i2v_pfet_gatefgota[0].out[0]','mismatch_meas[0].out[0]','mmap_local_swc[0].out[0]','ramp_fe[0].out[0:3]','hhneuron[0].out[0:2]','TIA_blk[0].out[0]','ichar_nfet[0].out[0]','tgate_so[0].out[0]','vmm4x4_SR[0].out[0]','vmm8x4_SR[0].out[0]','SR4[0].out[0:7]','vmm4x4_SR2[0].out[0]','vmm4x4[0].out[0:3]','sftreg[0].out[0]','DAC_sftreg[0].out[0]','sftreg2[0].out[0]','sftreg3[0].out[0]','sftreg4[0].out[0]','vmm8x4[0].out[0]','vmm8inx8in[0].out[0]','vmm8x4_in[0].out[0]','vmm12x1[0].out[0]','vmm12x1_wowta[0].out[0]','ota_vmm[0].out[0]','Hyst_diff[0].out[0]','Max_detect[0].out[0]','Min_detect[0].out[0]','hhn[0].out[0]','fgswitch[0].out[0]','common_drain[0].out[0]','common_drain_nfet[0].out[0]','hhn_debug[0].out[0:2]','wta_new[0].out[0]','common_source[0].out[0]','VolDivide1[0].out[0]','I_SenseAmp[0].out[0]','nmirror_w_bias[0].out[0]','SubbandArray[0].out[0:1]','HH_RG[0].out[0:1]','HH_RG_2s[0].out[0:1]','HH_RG_3s[0].out[0:1]','SOSLPF[0].out[0]','MSOS02[0].out[0]','vmm_offc[0].out[0:1]','C4_BPF[0].out[0]']
		li_sm_1 = ['fgota[0].in[0:1]','ota_buf[0].in[0]','ota[0].in[0:1]','cap[0].in[0]','nfet[0].in[0:1]','pfet[0].in[0:1]','tgate[0].in[0:1]','nmirror[0].in[0]','c4_sp[0].in[0:1]','gnd_out[0].in[0:1]','vdd_out[0].in[0:1]','in2in_x1[0].in[0:2]','in2in_x6[0].in[0:12]','lpf[0].in[0]','nfet_i2v[0].in[0]','pfet_i2v[0].in[0]','i2v_pfet_gatefgota[0].in[0]','mismatch_meas[0].in[0:2]','mmap_local_swc[0].in[0:2]','ramp_fe[0].in[0:1]','hhneuron[0].in[0:3]','TIA_blk[0].in[0]','ichar_nfet[0].in[0:1]','tgate_so[0].in[0:7]','vmm4x4_SR[0].in[0:6]','vmm8x4_SR[0].in[0:10]','SR4[0].in[0:3]','vmm4x4_SR2[0].in[0:7]','vmm4x4[0].in[0:3]','sftreg[0].in[0:18]','DAC_sftreg[0].in[0:2]','sftreg2[0].in[0:2]','sftreg3[0].in[0:3]','sftreg4[0].in[0:3]','vmm8x4[0].in[0:12]','vmm8inx8in[0].in[0:16]','vmm8x4_in[0].in[0:12]','vmm12x1[0].in[0:12]','vmm12x1_wowta[0].in[0:11]','ota_vmm[0].in[0:1]','Hyst_diff[0].in[0]','Max_detect[0].in[0]','Min_detect[0].in[0]','hhn[0].in[0:3]','fgswitch[0].in[0]','common_drain[0].in[0]','common_drain_nfet[0].in[0]','hhn_debug[0].in[0:3]','wta_new[0].in[0:2]','common_source[0].in[0]','VolDivide1[0].in[0]','I_SenseAmp[0].in[0:1]','nmirror_w_bias[0].in[0:1]','SubbandArray[0].in[0:1]','HH_RG[0].in[0:4]','HH_RG_2s[0].in[0:5]','HH_RG_3s[0].in[0:6]','SOSLPF[0].in[0]','MSOS02[0].in[0]','vmm_offc[0].in[0:12]','C4_BPF[0].in[0:1]','cab.O[0:7]']
		#O/PS        
		li_sm = ['gnd'             ,[0,  0],     #inputs from CAB and device outputs
			'vcc'              ,[0,  1],#y
			'cab.I[0:12]'        ,[0, range( 2, 15)],#y to be shifted for the decoder
			'vmm4x4_dummy[0:3]'	,[0,range(19,23)], #middle LI for VMM turn
			#O/PS OF CAB DEVICES
			'fgota[0:1].out[0]' ,[0, [15,16]],#y
			'ota_buf[0].out[0]' ,[0, 17],#y
			'ota[0:1].out[0]'      ,[0, [17,18]],#y
			'cap[0:3].out[0]'    ,[0, range(19, 23)],#y                                
			'nfet[0:1].out[0]'   ,[0, range(24, 22, -1)],#y numbering chnge for nFET0(24) and nFET1(23), needs to be verified
			'pfet[0:1].out[0]'   ,[0, range(26, 24,-1)],#y numbering chnge for pFETt0(26) and pFET1(23)
			'tgate[0:3].out[0]'  ,[0, range(27, 31)],#y
			'nmirror[0:1].out[0]',[0, range(31, 33)],#y
			'TIA_blk[0].out[0]'	 ,[0,17],
			'ichar_nfet[0].out[0]',[0,25],
			'c4_sp[0].out[0]'	 ,[0,15],# c4 with floating gates
			'gnd_out[0].out[0]',[0,24],
			'vdd_out[0].out[0]',[0,24],
			'in2in_x1[0].out[0]',[0,24],
			'in2in_x6[0].out[0]',[0,24],
			'ichar_nfet[0].in[0:1]' ,[[19,30],0],#vg,vd
			'lpf[0].out[0]',[0, 17],
			'nfet_i2v[0].out[0]',[0, 17], #ota0 output
			'pfet_i2v[0].out[0]',[0, 17], #ota0 output
			'i2v_pfet_gatefgota[0].out[0]',[0,17], #ota0 output
			'mismatch_meas[0].out[0]',[0,16], #fgota1 output
			'mmap_local_swc[0].out[0]'   ,[0,18+15], #chose col-18
			'ramp_fe[0].out[0:3]' , [0,[18,20,21,22]], #26
			'volswc[0:1].out[0]',[0, range(33, 35)],
			'hhneuron[0].out[0:2]',[0,[18,15,16]],#Vmem,VNa,VK
			'tgate_so[0].out[0]',[0,19],
			'ota_vmm[0].out[0]'      	,[0, 18],#y
			'vmm4x4_SR[0].out[0]'  ,[0,34], #19+15--->15 is offset for middle LI
			'vmm4x4_SR2[0].out[0]'  ,[0,34], #19+15--->15 is offset for middle LI
			'vmm8x4_SR[0].out[0]'  ,[0,34], #19+15--->15 is offset for middle LI
			'SR4[0].out[0:4]',	[0,[19,20,21,22,18+15]],#cap--ops+15, and the 18+15
			'vmm4x4[0].out[0:3]',	[0,range(19,23)],
			'vmm8x4[0].out[0]',	[0,0], #dummy output
			'vmm8inx8in[0].out[0]',	[0,19], #dummy output cap0's output
			'vmm8x4_in[0].out[0]',	[0,0], #dummy output
			'vmm12x1[0].out[0]',	[0,18], #wta output
			'sftreg[0].out[0]'   ,[0,18+15], #chose col-18
			'DAC_sftreg[0].out[0]'   ,[0,18+15], #chose col-18
			'sftreg2[0].out[0]'   ,[0,18+15], #chose col-18
			'sftreg3[0].out[0]'   ,[0,33], #chose col-18
			'sftreg4[0].out[0]'   ,[0,27], #tgate0's output
			'vmm12x1_wowta[0].out[0]',	[0,19], #vmm on cap out
			'Hyst_diff[0].out[0]',[0,18],
			'Max_detect[0].out[0]',[0,23],
			'Min_detect[0].out[0]',[0,25],
			'hhn[0].out[0]',[0,18],
			'fgswitch[0].out[0]',[0,19],
			'common_drain[0].out[0]',[0,25],
			'common_drain_nfet[0].out[0]',[0,23],
			'hhn_debug[0].out[0:2]',[0,[18,16,15]],
			'wta_new[0].out[0]',[0,17],
			'common_source[0].out[0]',[0,23],
			'VolDivide1[0].out[0]',[0,17],
			'I_SenseAmp[0].out[0]',[0,17],
			'nmirror_w_bias[0].out[0]',[0,31],
			'SubbandArray[0].out[0:1]',[0,[18,15]],
			'HH_RG[0].out[0:1]',[0,[17,23]],
			'HH_RG_2s[0].out[0:1]',[0,[17,23]],
			'HH_RG_3s[0].out[0:1]',[0,[17,23]],
			'SOSLPF[0].out[0]',[0,18],
			'MSOS02[0].out[0]',[0,18],
			'vmm_offc[0].out[0:1]',[0,[17,18]],
			'C4_BPF[0].out[0]',[0,17],
			'fgota[0].in[0:1]' ,[[33,32], 0],
			'fgota[1].in[0:1]' ,[[31,30], 0],
			'ota_buf[0].in[0]' ,  [29, 0],# in<0:7> y
			'ota[0].in[0:1]'     ,[[29, 28], 0],# in<0:7> y
			'cap[0:3].in[0]'     ,[range(25,21,-1), 0],# in<8:11 y
			'nfet[0:1].in[0:1]'  ,[[19, 18, 21, 20], 0],# in<12:15> y 21, 17,-1) it's flipped
			'pfet[0:1].in[0:1]'  ,[[15, 14, 17, 16], 0],# in<16:19> n---change (17, 13,-1) it;s flipped
			'tgate[0:3].in[0:1]' ,[range(13,5,-1), 0],# in<20:27> y
			'nmirror[0:1].in[0]' ,[range(5,3,-1), 0],# in<28:29> y
			'c4_sp[0].in[0:1]'   ,[[33,25],0],
			'gnd_out[0].in[0:1]'	 ,[[19,33],0],
			'vdd_out[0].in[0:1]'	 ,[[19,33],0],
			'in2in_x1[0].in[0:2]'	  ,[[19,33,33],0],
			'in2in_x6[0].in[0:12]'	  ,[[19,33,33,32,32,31,31,30,30,29,29,28,28],0],
			'lpf[0].in[0]'	 ,[29,0],
			'nfet_i2v[0].in[0]',[29,0],
			'pfet_i2v[0].in[0]',[29,0],
			'i2v_pfet_gatefgota[0].in[0]',[29,0], #ota0's in0
			'mismatch_meas[0].in[0:2]',[[12,13,11],0], #tgate0's in, s and tgate1's s
			'TIA_blk[0].in[0]'   ,[26,0],
			'ramp_fe[0].in[0:1]' , [[31,13],0],
			'hhneuron[0].in[0:3]',[[25,16,26,33],0],#Vin,ENa,EK,Vref27
			'ota_vmm[0].in[0:1]'     ,[range(27,25,-1), 0],# in<0:7> y
			'sftreg3[0].in[3]'   ,[21,0], 
			'sftreg4[0].in[3]'   ,[13,0], #tgate0's sel 
			'tgate_so[0].in[0:7]'	  ,[[12,21,10,19,8,17,6,15],0],
			'vmm4x4_SR[0].in[0:3]'	,[[33,32,31,30],0], #connection lines to turn into shift register
			'vmm4x4_SR2[0].in[0:7]'	,[[33,32,31,30,0,0,0,25],0], #connection lines to turn into shift register
			'vmm8x4_SR[0].in[0:7]'	,[[33,32,31,30,33,32,31,30],0], #connection lines to turn into shift register
			'vmm8x4[0].in[0:12]'	,[[33,32,31,30,33,32,31,30,33,32,31,30,29],0], #connection lines to turn into shift register ---check
			'vmm8inx8in[0].in[0]'	,[25,0], #dummy input cap0's input
			'vmm8x4_in[0].in[0:12]'	,[[33,32,31,30,33,32,31,30,33,32,31,30,29],0], #in[0]~[7] will be ignored by genu.py
			'vmm12x1[0].in[0:12]'	,[[19,19,19,19,19,19,19,19,19,19,19,19,21],0], #VMM_WTA INPUTS------------------------------------------------------here --------------------------------------------------
			'vmm12x1_wowta[0].in[0:11]'	,[[19,19,19,19,19,19,19,19,19,19,19,19],0], #VMM only------------------------------------------------------here --------------------------------------------------
			'SR4[0].in[0:3]'	,[[25,0,0,0],0], ## FG-OTAs input is now blocked
			'vmm4x4[0].in[0:3]'	,[[33,32,31,30],0],
			'Hyst_diff[0].in[0]',[27,0],
			'Max_detect[0].in[0]',[29,0],
			'Min_detect[0].in[0]',[29,0],
			'hhn[0].in[0:3]',[[29,16,20,31],0],
			'fgswitch[0].in[0]',[21,0],
			'common_drain[0].in[0]',[17,0],
			'common_drain_nfet[0].in[0]',[21,0],
			'hhn_debug[0].in[0:3]',[[29,16,20,31],0],
			'wta_new[0].in[0:2]',[[19,21,20],0],
			'common_source[0].in[0]',[21,0],
			'VolDivide1[0].in[0]',[29,0],
			'I_SenseAmp[0].in[0:1]',[[28,29],0],
			'nmirror_w_bias[0].in[0:1]',[[25,24],0],
			'SubbandArray[0].in[0:1]',[[33,25],0],
			'HH_RG[0].in[0:4]',[[24,16,20,31,27],0],
			'HH_RG_2s[0].in[0:5]',[[24,23,16,20,31,27],0],
			'HH_RG_3s[0].in[0:6]',[[24,23,22,16,20,31,27],0],
			'SOSLPF[0].in[0]',[33,0],
			'MSOS02[0].in[0]',[33,0],
			'vmm_offc[0].in[0:12]',[[6,7,8,9,10,11,12,13,14,15,16,17,27],0],
			'C4_BPF[0].in[0:1]',[[33,32],0],
			'cab.O[0:5]'          ,[range( 29, 23, -1), 21]] ## o/ps connectn to i/ps?? ummmmm !!! ---we need this 
		self.li = smDictFromList(li_sm)
		li0b = recStrExpand(li_sm_0b)
		li0b.reverse()
		self.li0 = recStrExpand(li_sm_0a) + li0b
		self.li1 = recStrExpand(li_sm_1)
		#CAB Devices ## order is very important here
		self.dev_types =['fgota']*1 +['ota_buf']*1+['ota']*1+['cap']*1+['nfet']*1+['pfet']*1+['tgate']*1+['nmirror']*1+['c4_sp']*1+['gnd_out']*1+['vdd_out']*1+['in2in_x1']*1+['in2in_x6']*1+['lpf']*1+['nfet_i2v']*1+['pfet_i2v']*1+['i2v_pfet_gatefgota']*1+['mismatch_meas']*1+['mmap_local_swc']*1+['ramp_fe']*1+['hhneuron']*1+['TIA_blk']*1+['ichar_nfet']*1+['tgate_so']*1+['vmm4x4_SR']*1+['vmm8x4_SR']*1+['SR4']*1+['vmm4x4_SR2']*1+['vmm4x4']*1+['sftreg']*1+['DAC_sftreg']*1 +['sftreg2']*1+['sftreg3']*1+['sftreg4']*1+['vmm8x4']*1+['vmm8inx8in']*1+['vmm8x4_in']*1+['vmm12x1']*1+['vmm12x1_wowta']*1+['ota_vmm']*1+['Hyst_diff']*1+['Max_detect']*1+['Min_detect']*1+['hhn']*1+['fgswitch']*1+['common_drain']*1+['common_drain_nfet']*1+['hhn_debug']*1+['wta_new']*1+['common_source']*1+['VolDivide1']*1+['I_SenseAmp']*1+['nmirror_w_bias']*1+['SubbandArray']*1+['HH_RG']*1+['HH_RG_2s']*1+['HH_RG_3s']*1+['SOSLPF']*1+['MSOS02']*1+['vmm_offc']*1+['C4_BPF']*1
		self.dev_pins ={'fgota_in':2,'ota_buf_in':1,'ota_in':2, 'cap_in':1, 'nfet_in':2, 'pfet_in':2,'tgate_in':2,'nmirror_in':1,'c4_sp_in':2,'gnd_out_in':2,'vdd_out_in':2,'in2in_x1_in':3,'in2in_x6_in':13,'lpf_in':1,'nfet_i2v_in':1,'pfet_i2v_in':1,'i2v_pfet_gatefgota_in':1,'mismatch_meas_in':3,'mmap_local_swc_in':3,'ramp_fe_in':2,'hhneuron_in':4,'TIA_blk_in':1,'ichar_nfet_in':2,'tgate_so_in':8,'vmm4x4_SR_in':7,'vmm8x4_SR_in':11,'SR4_in':4,'vmm4x4_SR2_in':8,'vmm4x4_in':4,'sftreg_in':19, 'DAC_sftreg_in':3,'sftreg2_in':3,'sftreg3_in':4,'sftreg4_in':4,'vmm8x4_in':13,'vmm8inx8in_in':17,'vmm8x4_in_in':13,'vmm12x1_in':13,'vmm12x1_wowta_in':12,'ota_vmm_in':2,'Hyst_diff_in':1,'Max_detect_in':1,'Min_detect_in':1,'hhn_in':4,'fgswitch_in':1,'common_drain_in':1,'common_drain_nfet_in':1,'hhn_debug_in':4,'wta_new_in':3,'common_source_in':1,'VolDivide1_in':1,'I_SenseAmp_in':2,'nmirror_w_bias_in':2,'SubbandArray_in':2,'HH_RG_in':5,'HH_RG_2s_in':6,'HH_RG_3s_in':7,'SOSLPF_in':1,'MSOS02_in':1,'vmm_offc_in':13,'C4_BPF_in':2,'fgota_out':1,'ota_buf_out':1,'ota_out':1, 'cap_out':1, 'nfet_out':1, 'pfet_out':1,'tgate_out':1,'nmirror_out':1,'c4_sp_out':1,'gnd_out_out':1,'vdd_out_out':1,'in2in_x1_out':1,'in2in_x6_out':1,'lpf_out':1,'nfet_i2v_out':1,'pfet_i2v_out':1,'i2v_pfet_gatefgota_out':1,'mismatch_meas_out':1,'mmap_local_swc_out':1,'ramp_fe_out':4,'hhneuron_out':3,'TIA_blk_out':1,'ichar_nfet_out':1,'tgate_so_out':1,'vmm4x4_SR_out':1,'vmm8x4_SR_out':1,'SR4_out':8,'vmm4x4_SR2_out':1,'vmm4x4_out':4,'sftreg_out':1,'DAC_sftreg_out':1,'sftreg2_out':1,'sftreg3_out':1,'sftreg4_out':1,'vmm8x4_out':1,'vmm8inx8in_out':1,'vmm8x4_in_out':1,'vmm12x1_out':1,'vmm12x1_wowta_out':1,'ota_vmm_out':1,'Hyst_diff_out':1,'Max_detect_out':1,'Min_detect_out':1,'hhn_out':1,'fgswitch_out':1,'common_drain_out':1,'common_drain_nfet_out':1,'hhn_debug_out':3,'wta_new_out':1,'common_source_out':1,'VolDivide1_out':1,'I_SenseAmp_out':1,'nmirror_w_bias_out':1,'SubbandArray_out':2,'HH_RG_out':2,'HH_RG_2s_out':2,'HH_RG_3s_out':2,'SOSLPF_out':1,'MSOS02_out':1,'vmm_offc_out':2,'C4_BPF_out':1}
		dev_fgs_sm = [
			'ota[0]'	,[0, 0],
			'ota_buf[0]' 	,[0, 0],
			'fgota[0]',[0, 0],
			'lpf[0]'	,[0, 62],
			'nfet_i2v[0]'	,[0, 0],
			'pfet_i2v[0]'	,[0, 0],
			'i2v_pfet_gatefgota[0]'	,[0, 0],
			'mismatch_meas[0]'	,[0, 0],
			'mmap_local_swc[0]' , [0,0],
			'ichar_nfet[0]' ,[0, 62],
			'c4_sp[0]'  	, [0,62], # set as ota[0] now
			'TIA_blk[0]'  	, [0,0],
			'gnd_out[0]' ,[0,0],
			'vdd_out[0]' ,[0,0],
			'in2in_x1[0]' ,[0,0],
			'in2in_x6[0]' ,[0,0],
			'ramp_fe[0]'    ,[0,62],
			'hhneuron[0]' ,[0,0],
			'nmirror[0]',[0,0],
			'cap[0:3]'	,[0, [57,60,57,60]],
			'tgate_so[0]' ,[0,0],
			'ota_vmm[0]'	,[0, 63],
			'vmm4x4[0]'	,[0,0],
			'vmm8x4[0]'	,[0,0],
			'vmm8inx8in[0]'	,[0,0],
			'vmm8x4_in[0]'	,[0,0],
			'vmm12x1[0]'	,[0,0],
			'vmm4x4_SR[0]'  ,[0,0],
			'vmm8x4_SR[0]'  ,[0,0],
			'vmm4x4_SR2[0]'  ,[0,0],
			'vmm12x1_wowta[0]'	,[0,0],
			'SR4[0]'	,[0,0],
			'sftreg[0]' , [0,0],
			'DAC_sftreg[0]' , [0,0],
			'sftreg2[0]' , [0,0],
			'sftreg3[0]' , [0,0],
			'sftreg4[0]' , [0,0],
			'Hyst_diff[0]',[0,0],
			'Max_detect[0]',[0,0],
			'Min_detect[0]',[0,0],
			'hhn[0]',[0,0],
			'fgswitch[0]',[0,0],
			'common_drain[0]',[0,0],
			'common_drain_nfet[0]',[0,0],
			'hhn_debug[0]',[0,0],
			'wta_new[0]',[0,0],
			'common_source[0]',[0,0],
			'VolDivide1[0]',[0,0],
			'I_SenseAmp[0]',[0,0],
			'nmirror_w_bias[0]',[0,0],
			'SubbandArray[0]',[0,0],
			'HH_RG[0]',[0,0],
			'HH_RG_2s[0]',[0,0],
			'HH_RG_3s[0]',[0,0],
			'SOSLPF[0]',[0,0],
			'MSOS02[0]',[0,0],
			'vmm_offc[0]',[0,0],
			'C4_BPF[0]',[0,0],
			##### now the define parts
			#'ota_bias'	,[[32, 0],[33,0]],
			'ladder_fg[0]',[[31,15],[29,16],[32,16],[28,17]],
			'ota_bias[0]'	,[[32, 62]],
			'ota_bias[1]'	,[[32, 63]],
			'ota_buf_ls[0]'	,[[28,17]],
			'ota_buf_bias[0]'	,[[32, 62]],
			'ramp_ota_biasfb[0]',[[32,-1],[28,17-63]],
			'gnd_out_c[0]', [[33, 0]],
			'vdd_out_c[0]', [[33, 1]],
			'ichar_nfet_fg[0]' , [[17,16-62],[16,24-62],[31,24-62],[18,0-62],[31,2-62+58],[31,3-62+58]],
			'cs_bias[0]'   ,[[25,1]],
			'fgota_bias[0]', [[32, 58]],
			'fgota_bias[1]', [[32, 60]],
			'fgota_p_bias[0]', [[33, 59]],
			'fgota_n_bias[0]', [[33, 58]],
			'fgota_p_bias[1]', [[33, 61]],
			'fgota_n_bias[1]', [[33, 60]],
			'c4_sp_ota_p_bias[0]', [[33, 1-62+58]],
			'c4_sp_ota_n_bias[0]', [[33, 0-62+58]],
			'c4_sp_ota_p_bias[1]', [[33, 1-62+60]],
			'c4_sp_ota_n_bias[1]', [[33, 0-62+60]],
			'TIA_ota_p_bias[0]', [[33, 59]],
			'TIA_ota_n_bias[0]', [[33, 58]],
			'TIA_ota_p_bias[1]', [[33, 61]],
			'TIA_ota_n_bias[1]', [[33, 60]],
			'TIA_fgota_bias[0]',[[32, 58]],
			'TIA_fgota_bias[1]',[[32, 60]],
			'TIA_ota_bias[0]',[[32, 63]],
			'TIA_ota_buf_out[0]',[32, 62],
			'TIA_fg[0]'	,[[26,15],[33,18],[32,15],[31,1+58],[31,0+58],[27,16],[30,16],[31,1],[31,1+60],[31,0+60],[29,18],[30,19],[25,0],[28,57],[28,17],[29,20],[24,0],[29,57]],
			'ladder_fg_fb[0]', [[30,16-62]],
			'hhneuron_fg[0]', [[32,19],[25,20],[24,19],[31,58],[31,59],[28,2+60],[28,1+60],[28,0+60],[28,2+57],[28,1+57],[28,0+57],[17,15],[31,24],[30,16],[19,16],[25,18],[31,60],[31,61],[26,27],[18,27]],
			'nfet_i2v_fg[0]', [[28,17],[29,24],[19,24],[18,0]],
			'nfet_i2v_otabias[0]', [32,62],
			'pfet_i2v_fg[0]', [[28,17],[29,26],[15,0],[14,0]],
			'pfet_i2v_otabias[0]', [32,62],
			'i2v_pfet_gatefgota_fg[0]', [[29,26],[14,0],[15,15],[28,17],[33,1],[32,15],[31,58],[31,59]], 
			'i2v_pfet_gatefgota_ota0bias[0]', [32,62],
			'i2v_pfet_gatefgota_fgotabias[0]', [32,58],
			'i2v_pfet_gatefgota_fgotapbias[0]', [33,59],
			'i2v_pfet_gatefgota_fgotanbias[0]', [33,58],
			'mismatch_meas_fg[0]', [[31,26],[14,0],[15,15],[30,0],[33,1],[32,15],[31,58],[31,59],[31,60],[31,61],[31,27],[31,28]], 
			'mismatch_meas_pfetg_fgotabias[0]', [32,58],
			'mismatch_meas_pfetg_fgotapbias[0]', [33,59],
			'mismatch_meas_pfetg_fgotanbias[0]', [33,58],
			'mismatch_meas_out_fgotabias[0]', [32,60],
			'mismatch_meas_out_fgotapbias[0]', [33,61],
			'mismatch_meas_out_fgotanbias[0]', [33,60],
			'mismatch_meas_cal_bias[0]', [10,1],
			'mmap_ls_fg[0]' ,[[30,40],[30,41],[30,42],[30,43],[30,44],[30,45],[30,46],[30,47],[30,48],[30,49],[30,50],[30,51],[30,52],[30,53],[30,54],[30,55],[25,19+15+21]],
			'mmap_ls_in_r0_vdd[0]' ,[[33,1]],
			'mmap_ls_in_r0[0]' ,[[33,8],[33,9],[33,10],[33,11],[33,12],[33,13],[33,2],[33,3],[33,4],[33,5],[33,6],[33,7]],
			'mmap_ls_in_r1_vdd[0]' ,[[32,1]],
			'mmap_ls_in_r1[0]' ,[[32,8],[32,9],[32,10],[32,11],[32,12],[32,13],[32,2],[32,3],[32,4],[32,5],[32,6],[32,7]],
			'mmap_ls_in_r2_vdd[0]' ,[[31,1]],
			'mmap_ls_in_r2[0]' ,[[31,8],[31,9],[31,10],[31,11],[31,12],[31,13],[31,2],[31,3],[31,4],[31,5],[31,6],[31,7]],
			'mmap_ls_in_r3_vdd[0]' ,[[30,1]],
			'mmap_ls_in_r3[0]' ,[[30,8],[30,9],[30,10],[30,11],[30,12],[30,13],[30,2],[30,3],[30,4],[30,5],[30,6],[30,7]],
			'mmap_ls_in_r4_vdd[0]' ,[[29,1]],
			'mmap_ls_in_r4[0]' ,[[29,8],[29,9],[29,10],[29,11],[29,12],[29,13],[29,2],[29,3],[29,4],[29,5],[29,6],[29,7]],
			'mmap_ls_in_r5_vdd[0]' ,[[28,1]],
			'mmap_ls_in_r5[0]' ,[[28,8],[28,9],[28,10],[28,11],[28,12],[28,13],[28,2],[28,3],[28,4],[28,5],[28,6],[28,7]],
			'mmap_ls_in_r6_vdd[0]' ,[[27,1]],
			'mmap_ls_in_r6[0]' ,[[27,8],[27,9],[27,10],[27,11],[27,12],[27,13],[27,2],[27,3],[27,4],[27,5],[27,6],[27,7]],
			'mmap_ls_in_r7_vdd[0]' ,[[26,1]],
			'mmap_ls_in_r7[0]' ,[[26,8],[26,9],[26,10],[26,11],[26,12],[26,13],[26,2],[26,3],[26,4],[26,5],[26,6],[26,7]],
			'mmap_ls_in_r8_vdd[0]' ,[[25,1]],
			'mmap_ls_in_r8[0]' ,[[25,8],[25,9],[25,10],[25,11],[25,12],[25,13],[25,2],[25,3],[25,4],[25,5],[25,6],[25,7]],
			'mmap_ls_in_r9_vdd[0]' ,[[24,1]],
			'mmap_ls_in_r9[0]' ,[[24,8],[24,9],[24,10],[24,11],[24,12],[24,13],[24,2],[24,3],[24,4],[24,5],[24,6],[24,7]],
			'mmap_ls_in_r10_vdd[0]' ,[[23,1]],
			'mmap_ls_in_r10[0]' ,[[23,8],[23,9],[23,10],[23,11],[23,12],[23,13],[23,2],[23,3],[23,4],[23,5],[23,6],[23,7]],
			'mmap_ls_in_r11_vdd[0]' ,[[22,1]],
			'mmap_ls_in_r11[0]' ,[[22,8],[22,9],[22,10],[22,11],[22,12],[22,13],[22,2],[22,3],[22,4],[22,5],[22,6],[22,7]],
			'mmap_ls_in_r12_vdd[0]' ,[[21,1]],
			'mmap_ls_in_r12[0]' ,[[21,8],[21,9],[21,10],[21,11],[21,12],[21,13],[21,2],[21,3],[21,4],[21,5],[21,6],[21,7]],
			'mmap_ls_in_r13_vdd[0]' ,[[20,1]],
			'mmap_ls_in_r13[0]' ,[[20,8],[20,9],[20,10],[20,11],[20,12],[20,13],[20,2],[20,3],[20,4],[20,5],[20,6],[20,7]],
			'mmap_ls_in_r14_vdd[0]' ,[[19,1]],
			'mmap_ls_in_r14[0]' ,[[19,8],[19,9],[19,10],[19,11],[19,12],[19,13],[19,2],[19,3],[19,4],[19,5],[19,6],[19,7]],
			'mmap_ls_in_r15_vdd[0]' ,[[18,1]],
			'mmap_ls_in_r15[0]' ,[[18,8],[18,9],[18,10],[18,11],[18,12],[18,13],[18,2],[18,3],[18,4],[18,5],[18,6],[18,7]],
			'mmap_ls_in_r16_vdd[0]' ,[[17,1]],
			'mmap_ls_in_r16[0]' ,[[17,8],[17,9],[17,10],[17,11],[17,12],[17,13],[17,2],[17,3],[17,4],[17,5],[17,6],[17,7]],
			'mmap_ls_in_r17_vdd[0]' ,[[16,1]],
			'mmap_ls_in_r17[0]' ,[[16,8],[16,9],[16,10],[16,11],[16,12],[16,13],[16,2],[16,3],[16,4],[16,5],[16,6],[16,7]],
			'mmap_ls_in_r18_vdd[0]' ,[[15,1]],
			'mmap_ls_in_r18[0]' ,[[15,8],[15,9],[15,10],[15,11],[15,12],[15,13],[15,2],[15,3],[15,4],[15,5],[15,6],[15,7]],
			'mmap_ls_in_r19_vdd[0]' ,[[14,1]],
			'mmap_ls_in_r19[0]' ,[[14,8],[14,9],[14,10],[14,11],[14,12],[14,13],[14,2],[14,3],[14,4],[14,5],[14,6],[14,7]],
			'mmap_ls_in_r20_vdd[0]' ,[[13,1]],
			'mmap_ls_in_r20[0]' ,[[13,8],[13,9],[13,10],[13,11],[13,12],[13,13],[13,2],[13,3],[13,4],[13,5],[13,6],[13,7]],
			'mmap_ls_in_r21_vdd[0]' ,[[12,1]],
			'mmap_ls_in_r21[0]' ,[[12,8],[12,9],[12,10],[12,11],[12,12],[12,13],[12,2],[12,3],[12,4],[12,5],[12,6],[12,7]],
			'mmap_ls_in_r22_vdd[0]' ,[[11,1]],
			'mmap_ls_in_r22[0]' ,[[11,8],[11,9],[11,10],[11,11],[11,12],[11,13],[11,2],[11,3],[11,4],[11,5],[11,6],[11,7]],
			'mmap_ls_in_r23_vdd[0]' ,[[10,1]],
			'mmap_ls_in_r23[0]' ,[[10,8],[10,9],[10,10],[10,11],[10,12],[10,13],[10,2],[10,3],[10,4],[10,5],[10,6],[10,7]],
			'mmap_ls_in_r24_vdd[0]' ,[[9,1]],
			'mmap_ls_in_r24[0]' ,[[9,8],[9,9],[9,10],[9,11],[9,12],[9,13],[9,2],[9,3],[9,4],[9,5],[9,6],[9,7]],
			'mmap_ls_in_r25_vdd[0]' ,[[8,1]],
			'mmap_ls_in_r25[0]' ,[[8,8],[8,9],[8,10],[8,11],[8,12],[8,13],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7]],
			'mmap_ls_in_r26_vdd[0]' ,[[7,1]],
			'mmap_ls_in_r26[0]' ,[[7,8],[7,9],[7,10],[7,11],[7,12],[7,13],[7,2],[7,3],[7,4],[7,5],[7,6],[7,7]],
			'mmap_ls_in_r27_vdd[0]' ,[[6,1]],
			'mmap_ls_in_r27[0]' ,[[6,8],[6,9],[6,10],[6,11],[6,12],[6,13],[6,2],[6,3],[6,4],[6,5],[6,6],[6,7]],
			'mmap_ls_in_r28_vdd[0]' ,[[5,1]],
			'mmap_ls_in_r28[0]' ,[[5,8],[5,9],[5,10],[5,11],[5,12],[5,13],[5,2],[5,3],[5,4],[5,5],[5,6],[5,7]],
			'mmap_ls_in_r29_vdd[0]' ,[[4,1]],
			'mmap_ls_in_r29[0]' ,[[4,8],[4,9],[4,10],[4,11],[4,12],[4,13],[4,2],[4,3],[4,4],[4,5],[4,6],[4,7]],
			'mmap_ls_in_vdd1_vdd[0]' ,[[33,8],[32,9],[31,10],[30,11],[29,12],[28,13],[27,2],[26,3],[25,4],[24,5],[23,6],[22,7]],
			'mmap_ls_in_vdd1[0]' ,[[33,1],[32,1],[31,1],[30,1],[29,1],[28,1],[27,1],[26,1],[25,1],[24,1],[23,1],[22,1]],
			'mmap_ls_in_vdd2_vdd[0]' ,[[21,8],[20,9],[19,10],[18,11],[17,12],[16,13],[15,2],[14,3],[13,4],[12,5],[11,6],[10,7]],
			'mmap_ls_in_vdd2[0]' ,[[21,1],[20,1],[19,1],[18,1],[17,1],[16,1],[15,1],[14,1],[13,1],[12,1],[11,1],[10,1]],
			'mmap_ls_in_vdd3_vdd[0]' ,[[9,8],[8,9],[7,10],[6,11]],
			'mmap_ls_in_vdd3[0]' ,[[9,1],[8,1],[7,1],[6,1]],
			'mmap_ls_in_in12_1_vdd[0]' ,[[33,8],[32,9],[31,10],[30,11],[29,12],[28,13],[27,2],[26,3],[25,4],[24,5],[23,6],[22,7],[21,1],[21,14]],
			'mmap_ls_in_in12_1[0]' ,[[33,14],[32,14],[31,14],[30,14],[29,14],[28,14],[27,14],[26,14],[25,14],[24,14],[23,14],[22,14]],
			'mmap_ls_in_in12_2_vdd[0]' ,[[21,8],[20,9],[19,10],[18,11],[17,12],[16,13],[15,2],[14,3],[13,4],[12,5],[11,6],[10,7],[22,1],[22,14]],
			'mmap_ls_in_in12_2[0]' ,[[21,14],[20,14],[19,14],[18,14],[17,14],[16,14],[15,14],[14,14],[13,14],[12,14],[11,14],[10,14]],
			'mmap_ls_in_in12_3_vdd[0]' ,[[9,8],[8,9],[7,10],[6,11],[10,1],[10,14]],
			'mmap_ls_in_in12_3[0]' ,[[9,14],[8,14],[7,14],[6,14]],
			'hh_nabias', [32,58],
			'hh_kbias', [32,60],
			'hh_fbpfetbias', [32,15],
			'hh_vinbias', [32,63],
			'hh_voutbias', [32,62],
			'hh_ota_p_bias[0]', [[33, 59]],
			'hh_ota_n_bias[0]', [[33, 58]],
			'hh_ota_p_bias[1]', [[33, 61]],
			'hh_ota_n_bias[1]', [[33, 60]],
			'hh_leak', [31,1],
			#'ota_small_cap[0]', [[31,1],[31,0]],
			#'ota_small_cap[1]', [[31,1],[31,0]],
			'ladder_fb[0]' , [[28,0],[27,-1]],
			'cs_bias[0]'   ,[[5,1]],
			'c4_sp_ota_bias[0]',[[32, 0-62+58]],#62-17 ota_bias col-ota_out[0]col value
			'c4_sp_ota_bias[1]',[[32, 0-62+60]],
			'c4_sp_fg[0]'	,[[32,-43],[32,-46],[30,-46],[31,-47],[32,20-62],[24,15-62],[28,62-62]],#[ota_bias0|ota0neg->cap0|cap0.in->ota0out|ota_bias1|ota1_fb] |c2 and c3 conections
			'TIA_fg[0]'	,[[26,15],[33,18],[32,15],[31,1+58],[31,0+58],[27,16],[30,16],[31,1],[31,1+60],[31,0+60],[29,18],[30,19],[25,0],[28,57],[28,17],[29,20],[24,0],[29,57]],
			'c4_sp_cap_3x[0]',[28,2-62+57],
			'c4_sp_cap_2x[0]',[28,1-62+57],
			'c4_sp_cap_1x[0]',[28,0-62+57],
			'c4_sp_ota_small_cap[0]', [[31,1-62+58],[31,0-62+58]],
			'c4_sp_ota_small_cap[1]', [[31,1-62+60],[31,0-62+60]],
			'lpf_fg[0]'	,[[26,-43],[26,-42],[26,-41],[26,-40],[25,-61],[24,-61],[23,-61],[22,-61]],
			'ramp_fe_fg[0]' ,[[32,27-62],[25,27-62],[12,19-62],[12,15-62],[30,15-62],[28,2-62+57],[31,1-62+58],[31,0-62+58],[33,1-62],[31,1-62+60],[31,0-62+60],[27,16-62],[26,18-62]], #w/tgate and no fb, also needs buffer for GPIO
			'ramp_pfetinput[0]' ,[[32,1-62]], #w/tgate and no fb
			'ramp_pfetinput[1]' ,[[14,1-62]], #w/tgate and no fb
			'ramp_otabias[0]' ,[[32, 63-62]], #w/tgate and no fb
			'lpf_cap_3x[0:1]',[28,[-5,-2]],
			'lpf_cap_2x[0:1]',[28,[-4,-1]],
			'lpf_cap_1x[0:1]',[28,[-3, 0]],
			'lpf_cap_3x[2:3]',[29,[-5,-2]],# cap2 and 3
			'lpf_cap_2x[2:3]',[29,[-4,-1]],
			'lpf_cap_1x[2:3]',[29,[-3, 0]],
			'fgota_small_cap[0]',[[31,59],[31,58]],# switch for both n and p
			'fgota_small_cap[1]',[[31,61],[31,60]],#switches for both n and p
			'cap_1x_cs[0:3]'	,[[28,29,28,29], 2],
			'cap_2x_cs[0:3]'	,[[28,29,28,29], 1],
			'tgate_so_fg[0]',[[21,27],[19,28],[17,29],[15,30],[13,19],[11,19],[9,19],[7,19]],
			'ota0bias[0]'   ,[32,62], # for vmm sense amps
			'ota1bias[0]'   ,[32,63],
			'fgota0bias[0]' ,[32,62],
			'fgota1bias[0]' ,[32,63],
			'fgota0pbias[0]' ,[33,59],
			'fgota1pbias[0]' ,[33,61],
			'fgota0nbias[0]' ,[33,58],
			'fgota1nbias[0]' ,[33,60],
			'vmm_target[0]'  ,[0,0],
			'vmm12x1_wowta_fg[0]',[[19,19]],#VMM fg[19,23]
			'SR_fg[0]'	     ,[[33,19],[32,20],[31,21],[30,22],[33,8],[32,12],[31,2],[30,6],[25,18+15],[25,19+15]],
			'vmm_bias[0:3]'	     ,[[33,32,31,30],0],
			'vmm4x4_target[0:3]',[33,[10,11,13,14]], # Shift-register0
			'vmm4x4_target[4:7]',[32,[10,11,13,14]], #SR1
			'vmm4x4_target[8:11]',[31,[10,11,13,14]], #SR2
			'vmm4x4_target[12:15]',[30,[10,11,13,14]],#SR3
			'vmm8x4_target[0:7]',[33,[10,11,13,14,3,4,5,7]], # Shift-register0
			'vmm8x4_target[8:15]',[32,[10,11,13,14,3,4,5,7]], #SR1
			'vmm8x4_target[16:23]',[31,[10,11,13,14,3,4,5,7]], #SR2
			'vmm8x4_target[24:31]',[30,[10,11,13,14,3,4,5,7]],#SR3
			'vmm8x4_in_target[0:7]',[33,[2,3,4,5,6,7,8,9]], # 
			'vmm8x4_in_target[8:15]',[32,[2,3,4,5,6,7,8,9]], # 
			'vmm8x4_in_target[16:23]',[31,[2,3,4,5,6,7,8,9]], # 
			'vmm8x4_in_target[24:31]',[30,[2,3,4,5,6,7,8,9]], # 
			'vmm12x1_target[0:11]',[19,[2,3,4,5,6,7,8,9,10,11,12,13]],#VMM target values
			'vmm12x1_fg[0]',[[19,23],[20,0],[21,24],[18,20],[27,20],[26,18],[21,31]],#VMM fg[19,23]
			'vmm12x1_pfetbias[0]' ,[18,1], #WTA pfet bias
			'vmm12x1_offsetbias[0]' ,[19,1], #WTA pfet bias,offset for the vmm
			'vmm12x1_otabias[0]' ,[32,63], #WTA pfet bias
			'vmm8inx8in_fg[0]' ,[[33,10],[32,11],[31,12],[30,13],[20,23],[18,24],[16,25],[14,26],[29,44],[28,45],[27,46],[26,47]], # fg_io block
			'vmm8inx8in_target[0:7]',[33,[2,3,4,5,6,7,8,9]],  
			'vmm8inx8in_target[8:15]',[32,[2,3,4,5,6,7,8,9]],  
			'vmm8inx8in_target[16:23]',[31,[2,3,4,5,6,7,8,9]],  
			'vmm8inx8in_target[24:31]',[30,[2,3,4,5,6,7,8,9]],  
			'vmm8inx8in_target[32:39]',[20,[2,3,4,5,6,7,8,9]],  
			'vmm8inx8in_target[40:47]',[18,[2,3,4,5,6,7,8,9]],  
			'vmm8inx8in_target[48:55]',[16,[2,3,4,5,6,7,8,9]],  
			'vmm8inx8in_target[56:63]',[14,[2,3,4,5,6,7,8,9]],  
			'sftreg_fg[0]'  ,[[30,40],[30,41],[30,42],[30,43],[30,44],[30,45],[30,46],[30,47],[30,48],[30,49],[30,50],[30,51],[30,52],[30,53],[30,54],[30,55],[25,19+15+21]],
			'DAC_sftreg_fg[0]'  ,[[25,19+15+21],[33,1],[30,40],[30,41],[30,42],[30,43],[30,44],[30,45],[30,46],[30,47],[30,48],[30,49],[30,50],[30,51],[30,52],[30,53],[30,54],[30,55]],
			'DAC_sftreg_normal[0]'  ,[[33,1],[33,15],[25,33]],
			'DAC_bias_pfet[0]'  ,[25,0],
			'DAC_sftreg_target[0:5]'  ,[33,[8,9,10,11,12,13]],
			'DAC_sftreg_target[6:7]'  ,[[26,27],36],
			'DAC_sftreg_target[8:13]'  ,[33,[2,3,4,5,6,7]],
			'DAC_sftreg_target[14:15]'  ,[[28,29],36],
			'sftreg2_fg[0]' ,[[30,40],[30,41],[30,42],[30,43],[30,44],[30,45],[30,46],[30,47],[30,48],[30,49],[30,50],[30,51],[30,52],[30,53],[30,54],[30,55],[25,19+15+21]],
			'sftreg3_fg[0]' ,[[30,40],[30,41],[30,42],[30,43],[30,44],[30,45],[30,46],[30,47],[30,48],[30,49],[30,50],[30,51],[30,52],[30,53],[30,54],[30,55],[21,33],[21,34]],
			'sftreg4_fg[0]' ,[[30,40],[30,41],[30,42],[30,43],[30,44],[30,45],[30,46],[30,47],[30,48],[30,49],[30,50],[30,51],[30,52],[30,53],[30,54],[30,55],[12,33],[12,34],[29,33],[29,34],[28,17],[10,27],[28,28],[16,1],[11,25],[20,0],[11,23],[13,24],[21,24],[17,24]],
			'sftreg4_otabias[0]'   ,[[32,62]],  # ota0's bias
			'Hyst_diff_ls[0]',[[26,23],[26,25],[21,18],[20,1],[17,18],[16,0]],
			'Hyst_diff_ota1_ibias[0]',[32,63],
			'Max_detect_ls[0]',[[28,23],[28,31],[21,17],[20,1]],
			'Max_detect_ota0_ibias[0]',[32,62],
			'Max_detect_fgswc_ibias[0]',[5,1],
			'Min_detect_ls[0]',[[28,25],[17,17],[16,0]],
			'Min_detect_ota0_ibias[0]',[32,62],
			'Min_detect_fgswc_ibias[0]',[28,1],
			'hhn_ls[0]',[[33,17],[33,23],[32,15],[30,19],[28,27],[27,17],[27,25],[26,18],[25,17],[21,15],[20,27],[17,16],[31,61],[31,60],[31,59],[31,58]],
			'hhn_cap0_4x_cs[0]',[28,57],
			'hhn_cap0_2x_cs[0]',[28,58],
			'hhn_cap0_1x_cs[0]',[28,59],
			'hhn_fgota1_ibias[0]',[32,60],
			'hhn_fgota1_pbias[0]',[33,61],
			'hhn_fgota1_nbias[0]',[33,60],
			'hhn_fgota0_ibias[0]',[32,58],
			'hhn_fgota0_pbias[0]',[33,59],
			'hhn_fgota0_nbias[0]',[33,58],
			'hhn_ota0_ibias[0]',[32,62],
			'hhn_ota1_ibias[0]',[32,63],
			'hhn_fgswc_ibias[0]',[30,16],
			'fgswitch_ls[0]',[[33,0]],
			'fgswitch_fgswc_ibias[0]',[21,19],
			'common_drain_ls[0]',[[25,25],[16,0]],
			'common_drain_fgswc_ibias[0]',[25,1],
			'common_drain_nfet_ls[0]',[[20,1],[19,23],[19,31]],
			'common_drain_nfet_ibias[0]',[5,1],
			'hhn_debug_ls[0]',[[33,17],[33,23],[32,15],[30,19],[28,27],[27,17],[27,25],[26,18],[25,17],[21,15],[20,27],[17,16],[31,61],[31,60],[31,59],[31,58]],
			'hhn_debug_cap0_4x_cs[0]',[28,57],
			'hhn_debug_cap0_2x_cs[0]',[28,58],
			'hhn_debug_cap0_1x_cs[0]',[28,59],
			'hhn_debug_fgota1_ibias[0]',[32,60],
			'hhn_debug_fgota1_pbias[0]',[33,61],
			'hhn_debug_fgota1_nbias[0]',[33,60],
			'hhn_debug_fgota0_ibias[0]',[32,58],
			'hhn_debug_fgota0_pbias[0]',[33,59],
			'hhn_debug_fgota0_nbias[0]',[33,58],
			'hhn_debug_ota0_ibias[0]',[32,62],
			'hhn_debug_ota1_ibias[0]',[32,63],
			'hhn_debug_fgswc_ibias[0]',[30,16],
			'vmm_volatile[0]'     ,[[30,40],[30,44],[30,48],[30,52],[25,54]],
			'wta_new_ls[0]',[[29,19],[28,17],[21,24],[19,23],[18,19]],
			'wta_new_buf_bias[0]',[32,62],
			'wta_new_wta_bias[0]',[18,1],
			'common_source_ls[0]',[[25,23],[20,0]],
			'common_source_ibias[0]',[25,1],
			'VolDivide1_ls[0]',[[33,1],[32,15],[32,17],[28,17],[31,59],[31,58]],
			'VolDivide1_fgota0_ibias[0]',[32,58],
			'VolDivide1_fgota0_pbias[0]',[33,59],
			'VolDivide1_fgota0_nbias[0]',[33,58],
			'VolDivide1_ota0_ibias[0]',[32,62],
			'I_SenseAmp_ls[0]',[[33,17],[32,15],[28,15],[25,0],[24,0],[21,17],[21,19],[21,20],[31,59],[31,58]],
			'I_SenseAmp_cap0_4x_cs[0]',[28,57],
			'I_SenseAmp_cap0_2x_cs[0]',[28,58],
			'I_SenseAmp_cap0_1x_cs[0]',[28,59],
			'I_SenseAmp_cap1_4x_cs[0]',[28,57],
			'I_SenseAmp_cap1_2x_cs[0]',[28,58],
			'I_SenseAmp_cap1_1x_cs[0]',[28,59],
			'I_SenseAmp_fgota0_ibias[0]',[32,58],
			'I_SenseAmp_fgota0_pbias[0]',[33,59],
			'I_SenseAmp_fgota0_nbias[0]',[33,58],
			'I_SenseAmp_ota0_ibias[0]',[32,62],
			'nmirror_w_bias_ls[0]',[[25,31]],
			'nmirror_w_bias_ibias[0]',[5,1],
			'SubbandArray_ls[0]',[[32,16],[32,19],[32,21],[31,15],[30,16],[29,15],[28,23],[28,31],[27,23],[26,18],[23,15],[21,17],[20,1],[31,61],[31,60],[31,59],[31,58]],
			'SubbandArray_FFcap_4x_cs[0]',[28,57],
			'SubbandArray_FFcap_2x_cs[0]',[28,58],
			'SubbandArray_FFcap_1x_cs[0]',[28,59],
			'SubbandArray_FBcap_4x_cs[0]',[28,57],
			'SubbandArray_FBcap_2x_cs[0]',[28,58],
			'SubbandArray_FBcap_1x_cs[0]',[28,59],
			'SubbandArray_FBbias[0]',[32,60],
			'SubbandArray_FBpbias[0]',[33,61],
			'SubbandArray_FBnbias[0]',[33,60],
			'SubbandArray_FFbias[0]',[32,58],
			'SubbandArray_FFpbias[0]',[33,59],
			'SubbandArray_FFnbias[0]',[33,58],
			'SubbandArray_Maxota[0]',[32,62],
			'SubbandArray_LPF[0]',[32,63],
			'SubbandArray_Maxpfet[0]',[5,1],
			'HH_RG_ls[0]',[[33,23],[32,15],[30,19],[29,26],[28,17],[26,23],[26,25],[25,23],[21,15],[17,16],[15,18],[13,18],[12,26],[6,27],[6,31],[31,61],[31,60],[31,59],[31,58]],
			'HH_RG_cap0_4x_cs[0]',[28,57],
			'HH_RG_cap0_2x_cs[0]',[28,58],
			'HH_RG_cap0_1x_cs[0]',[28,59],
			'HH_RG_Na_ibias[0]',[32,60],
			'HH_RG_Na_pbias[0]',[33,61],
			'HH_RG_Na_nbias[0]',[33,60],
			'HH_RG_K_ibias[0]',[32,58],
			'HH_RG_K_pbias[0]',[33,59],
			'HH_RG_K_nbias[0]',[33,58],
			'HH_RG_buf_ibias[0]',[32,62],
			'HH_RG_comp_ibias[0]',[32,63],
			'HH_RG_Nafb_ibias[0]',[30,16],
			'HH_RG_in0_ibias[0]',[24,25],
			'HH_RG_pfet_ibias[0]',[14,1],
			'HH_RG_nmr_ibias[0]',[5,1],
			'HH_RG_2s_ls[0]',[[33,23],[32,15],[30,19],[29,26],[28,17],[26,23],[26,25],[25,23],[21,15],[17,16],[15,18],[13,18],[12,26],[6,27],[6,31],[31,61],[31,60],[31,59],[31,58]],
			'HH_RG_2s_cap0_4x_cs[0]',[28,57],
			'HH_RG_2s_cap0_2x_cs[0]',[28,58],
			'HH_RG_2s_cap0_1x_cs[0]',[28,59],
			'HH_RG_2s_Na_ibias[0]',[32,60],
			'HH_RG_2s_Na_pbias[0]',[33,61],
			'HH_RG_2s_Na_nbias[0]',[33,60],
			'HH_RG_2s_K_ibias[0]',[32,58],
			'HH_RG_2s_K_pbias[0]',[33,59],
			'HH_RG_2s_K_nbias[0]',[33,58],
			'HH_RG_2s_buf_ibias[0]',[32,62],
			'HH_RG_2s_comp_ibias[0]',[32,63],
			'HH_RG_2s_Nafb_ibias[0]',[30,16],
			'HH_RG_2s_syn0_ibias[0]',[24,25],
			'HH_RG_2s_syn1_ibias[0]',[23,25],
			'HH_RG_2s_pfet_ibias[0]',[14,1],
			'HH_RG_2s_nmr_ibias[0]',[5,1],
			'HH_RG_3s_ls[0]',[[33,23],[32,15],[30,19],[29,26],[28,17],[26,23],[26,25],[25,23],[21,15],[17,16],[15,18],[13,18],[12,26],[6,27],[6,31],[31,61],[31,60],[31,59],[31,58]],
			'HH_RG_3s_cap0_4x_cs[0]',[28,57],
			'HH_RG_3s_cap0_2x_cs[0]',[28,58],
			'HH_RG_3s_cap0_1x_cs[0]',[28,59],
			'HH_RG_3s_Na_ibias[0]',[32,60],
			'HH_RG_3s_Na_pbias[0]',[33,61],
			'HH_RG_3s_Na_nbias[0]',[33,60],
			'HH_RG_3s_K_ibias[0]',[32,58],
			'HH_RG_3s_K_pbias[0]',[33,59],
			'HH_RG_3s_K_nbias[0]',[33,58],
			'HH_RG_3s_buf_ibias[0]',[32,62],
			'HH_RG_3s_comp_ibias[0]',[32,63],
			'HH_RG_3s_Nafb_ibias[0]',[30,16],
			'HH_RG_3s_syn0_ibias[0]',[24,25],
			'HH_RG_3s_syn1_ibias[0]',[23,25],
			'HH_RG_3s_syn2_ibias[0]',[22,25],
			'HH_RG_3s_pfet_ibias[0]',[14,1],
			'HH_RG_3s_nmr_ibias[0]',[5,1],
			'SOSLPF_ls[0]',[[32,15],[31,15],[31,17],[30,16],[29,17],[28,16],[27,16],[26,18],[31,61],[31,60],[31,59],[31,58]],
			'SOSLPF_Ibias2[0]',[32,60],
			'SOSLPF_FG2p[0]',[33,61],
			'SOSLPF_FG2n[0]',[33,60],
			'SOSLPF_Ibias1[0]',[32,58],
			'SOSLPF_FG1p[0]',[33,59],
			'SOSLPF_FG1n[0]',[33,58],
			'SOSLPF_Feedback[0]',[32,62],
			'SOSLPF_Buffer[0]',[32,63],
			'MSOS02_ls[0]',[[32,15],[31,15],[31,17],[30,16],[29,17],[28,16],[27,16],[26,18],[31,61],[31,60],[31,59],[31,58]],
			'MSOS02_Ibias2[0]',[32,60],
			'MSOS02_Wbp[0]',[33,61],
			'MSOS02_Wbn[0]',[33,60],
			'MSOS02_Ibias1[0]',[32,58],
			'MSOS02_Wap[0]',[33,59],
			'MSOS02_Wan[0]',[33,58],
			'MSOS02_Feedback[0]',[32,62],
			'MSOS02_Buffer[0]',[32,63],
			'vmm_offc_ls[0]',[[33,17],[32,15],[32,19],[31,18],[30,16],[30,20],[29,27],[28,15],[28,19],[27,27],[26,16],[26,20],[21,31],[19,32],[5,15],[4,16],[31,61],[31,60],[31,59],[31,58]],
			'vmm_offc_o2_fgibias[0]',[32,60],
			'vmm_offc_o2_pbias[0]',[33,61],
			'vmm_offc_o2_pbias[0]',[33,60],
			'vmm_offc_o1_fgibias[0]',[32,58],
			'vmm_offc_o1_pbias[0]',[33,59],
			'vmm_offc_o1_nbias[0]',[33,58],
			'vmm_offc_o1_ibias[0]',[32,62],
			'vmm_offc_o1_ibias[0]',[32,63],
			'vmm_offc_off1_ibias[0]',[21,1],
			'vmm_offc_off2_ibias[0]',[19,1],
			'vmm_offc_w16n[0]',[17,19],
			'vmm_offc_w26n[0]',[17,20],
			'vmm_offc_w16p[0]',[16,19],
			'vmm_offc_w26p[0]',[16,20],
			'vmm_offc_w15n[0]',[15,19],
			'vmm_offc_w25n[0]',[15,20],
			'vmm_offc_w15p[0]',[14,19],
			'vmm_offc_w25p[0]',[14,20],
			'vmm_offc_w14n[0]',[13,19],
			'vmm_offc_w24n[0]',[13,20],
			'vmm_offc_w14p[0]',[12,19],
			'vmm_offc_w24p[0]',[12,20],
			'vmm_offc_w13n[0]',[11,19],
			'vmm_offc_w23n[0]',[11,20],
			'vmm_offc_w13p[0]',[10,19],
			'vmm_offc_w23p[0]',[10,20],
			'vmm_offc_w12n[0]',[9,19],
			'vmm_offc_w22n[0]',[9,20],
			'vmm_offc_w12p[0]',[8,19],
			'vmm_offc_w22p[0]',[8,20],
			'vmm_offc_w11n[0]',[7,19],
			'vmm_offc_w21n[0]',[7,20],
			'vmm_offc_w11p[0]',[6,19],
			'vmm_offc_w21p[0]',[6,20],
			'C4_BPF_ls[0]',[[32,16],[32,19],[32,20],[31,15],[30,16],[29,15],[28,17],[24,15],[33,3],[25,2],[31,61],[31,60],[31,59],[31,58]],
			'C4_BPF_Cin_4x_cs[0]',[28,57],
			'C4_BPF_Cin_2x_cs[0]',[28,58],
			'C4_BPF_Cin_1x_cs[0]',[28,59],
			'C4_BPF_Cfb_4x_cs[0]',[28,60],
			'C4_BPF_Cfb_2x_cs[0]',[28,61],
			'C4_BPF_Cfb_1x_cs[0]',[28,62],
			'C4_BPF_Feedback_ibias[0]',[32,60],
			'C4_BPF_Feedback_pbias[0]',[33,61],
			'C4_BPF_Feedback_nbias[0]',[33,60],
			'C4_BPF_Forward_ibias[0]',[32,58],
			'C4_BPF_Forward_pbias[0]',[33,59],
			'C4_BPF_Forward_nbias[0]',[33,58],
			'C4_BPF_Buffer_ibias[0]',[32,62],
			'cap_4x_cs[0:3]',[[28,29,28,29], 0]]
		self.dev_fgs = smDictFromList(dev_fgs_sm)

###########################################
#   CAB2 stats 
###########################################   
class cab2Stats(stats):
	def __init__(self):
		self.num_inputs = 13
		self.num_outputs = 8
		self.pin_order =['I0','I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','I14','I15','O0','O1','O0','O1','O2','O3','O4','O5','O6','O7']

		#CHANX--C BLOCK ---y axis of adjacent CAB
		# these are the decoder mapped addrs
		#chanx_sm = ['T[0:16]', [range(22,13,-1)+range(12,8,-1)+range(7,3,-1),0],### flipping chanx and chany ####
		chanx_sm = ['T[0:16]', [list(range(22,15,-1))+list(range(14,8,-1))+list(range(7,3,-1)),0],
			'I8',   [ 0,36],     #pin names
			'I9',   [ 0,37],
			'I13',  [ 0,38],
			'I14',  [ 0,39],
			'I15',  [ 0,40],
			'O4',   [ 0,41],
			'XI10', [ 0,42],
			'XI11', [ 0,43],
			'XI12', [ 0,44],
			'XO5',  [ 0,45],
			'XO6',  [ 0,46],
			'XO7',  [ 0,47]]
		self.chanx = smDictFromList(chanx_sm, 'remBrak')

		# CHANY  --x axis block of original  
		#chany_sm = ['T[0:16]', [range(22,13,-1)+range(12,8,-1)+range(7,3,-1),0],
		chany_sm = ['T[0:16]', [list(range(22,15,-1))+list(range(14,8,-1))+list(range(7,3,-1)),0],
			'I4',   [ 0,65],    #pin names
			'I5',   [ 0,66],
			'I6',   [ 0,67],
			'I7',   [ 0,68],
			'O2',   [ 0,69],
			'O3',   [ 0,70],
			'XO0',  [ 0,63],
			'XO1',  [ 0,64],
			'XI0',  [ 0,59],
			'XI1',  [ 0,60],
			'XI2',  [ 0,61],## problem conflict
			'XI3',  [ 0,62],
			'DXI2', [ 0,65],#------to match w/ dif DIgital tile NAME BUT ANALOG TILE MAPPING
			'DXI6',  [ 0,66], #to match w/ dif tile
			'DXI10', [ 0,67],#to match w/ dif tile
			'DXI14', [ 0,68],
			'DXO2',  [ 0,69],
			'DXO6',  [ 0,70]]
		self.chany = smDictFromList(chany_sm, 'remBrak')

		# SBLOCK            
		#sb_sw = ['T[0:16]', [range(22,13,-1)+range(12,8,-1)+range(7,3,-1), 0],
		sb_sw = ['T[0:16]', [list(range(22,15,-1))+list(range(14,8,-1))+list(range(7,3,-1)), 0],
			'we',   [ 0,54],#actual ns    #track direction (these are rotated 90deg ccw from schematic name: ww->W)
			'wn',   [ 0,51],#ne                     
			'ws',   [ 0,50],#nw                     
			'ns',   [ 0,52], #ew                     
			'ne',   [ 0,53],#es                     
			'es',   [ 0,49],                     
			'ew',   [ 0,54],#ns                     
			'nw',   [ 0,51],                     
			'sw',   [ 0,50],                     
			'sn',   [ 0,52],                     
			'en',   [ 0,53],                     
			'se',   [ 0,49]]    
		self.sblock = smDictFromList(sb_sw, 'remBrak')  

		#Local Interconnect
		li_sm_0a = ['gnd','vcc','cab2.I[0:15]']
		# outputs order into the CAB
		li_sm_0b = ['ota_buffer.out[0]','tgate[0:2].out[0]','cap2[0:2].out[0]','tgate2[0:2].out[0]','mite[0:2].out[0]','mite2.out[0:1]','signalmult[0].out[0:1]','meas_volt_mite[0:1].out','ota2.out','current_ref.out[0]']
		# defining the inputs order into the CAB #?? last term to connect i/ps to o/ps?
		li_sm_1 = ['ota_buffer.in[0]','tgate[0:2].in[0:1]','cap2[0:2].in[0]','tgate2[0:2].in[0:1]','mite[0:2].in[0:2]','mite2.in[0:1]','signalmult[0].in[0:3]','meas_volt_mite[0:1].in','ota2.in[0:1]','current_ref.in[0:1]','cab2.O[0:5]'] 
		#O/PS        
		li_sm = ['gnd'           ,[0,  0],     #inputs from CAB and device outputs
			'vcc'                ,[0,  1],#y
			'cab2.I[0:12]'       ,[0, range( 2, 15)],#y to be shifted for the decoder
			#O/PS OF CAB DEVICES
			'ota2.out[0]'         ,[0, 15],#y
			'ota_buffer.out[0]'  ,[0, 15],#y
			'current_ref.out[0]'  ,[0, 25],#y need to figure out the switch numbers
			'tgate[0:2].out[0]'  ,[0,range(16,19)],
			'cap2[0:2].out[0]'    ,[0,range(19, 22)],#y                                
			'tgate2[0:2].out[0]' ,[0,range(22, 25)],#y numbering chnge for nFET0(24) and nFET1(23)
			'mite[0:2].out[0]'   ,[0,[25,26,31]],# out<10,11,16>
			'mite2.out[0:1]'  	 ,[0,[32,18]],# out<17>,out<3> --it's a 2 i/p 2o/p mite
			'signalmult[0:1].out[0:1]' ,[0,range(27,31)],# out<12:14>
			'meas_volt_mite[0:1].out',[0,[[25,26],[31,32,18]]], # we don't want to connect the outout
			'ota2.in[0:1]'  	 ,[range(33,31,-1), 0],# in<0:1> y
			'ota_buffer.in[0]'  	 ,[33, 0],# in<0:1> y
			'tgate[0:2].out'     ,[range(31,27,-1), 0],# in<2:7> y
			'current_ref.in[0:1]'  ,[[13,12], 0],#y
			'cap2[0:2].in[0]'     ,[range(27,22,-1), 0],# in<8:10> y
			'tgate2[0:1].in[0:1]',[list(range(17,13,-1))+[15,22], 0],# in<> y 21, 17,-1) it's flipped
			'mite[0:2].in[0:2]'  ,[[13,12,11,10,9,8,31,29,15], 0],# in<16:19> n---change (17, 13,-1) it;s flipped
			'mite2.in[0:1]' 	 ,[[27,17], 0],# in<6,16> y
			'signalmult[0:1].in[0:3]'  ,[list(range(7,3,-1))+list(range(21,17,-1)), 0],# in<26:29> +in<12:15>
			'meas_volt_mite[0:1].in',[[[13,12,10,9],[31,29,27,17]],0],
			'cab2.O[0:5]'        ,[range( 29, 23, -1), 21]] ##its 21 
		self.li = smDictFromList(li_sm)
		li0b = recStrExpand(li_sm_0b)
		li0b.reverse()
		self.li0 = recStrExpand(li_sm_0a) + li0b #$$$$
		self.li1 = recStrExpand(li_sm_1)

		#CAB Devices ## to check
		self.dev_types = ['ota_buffer']*1 + ['tgate']*3+['cap2']*3 + ['tgate2']*3 + ['mite']*3 + ['mite2']*1 +['signalmult']*1+['meas_volt_mite']*2+['ota2']*1+['current_ref']*1
		self.dev_pins = {'tgate_in':2,'tgate_out':1, 'cap2_in':1,'cap2_out':1, 'tgate2_in':2,'tgate2_out':1,'ota2_out':1, 'mite_in':3,'mite_out':1,'current_ref_out':1, 'mite2_in':2, 'mite2_out':2,'signalmult_in':4, 'signalmult_out':2,'meas_volt_mite_in':1,'meas_volt_mite_out':1,'ota_buffer_in':1, 'ota2_in':2,'ota_buffer_out':1,'current_ref_in':2}  
		dev_fgs_sm = ['meas_volt_mite[0:1]',[0, [61, 63]],
			'mite2[0]'	,[0,63],
			'ota2[0]'	,[0,0],
			'mite[0:2]',[0, [0,0,0]],
			'current_ref[0]',[0, 0],
			#'mite[0]'	,[0,61],
			'signalmult[0]'	,[0,0],
			'ota_buffer[0]',[[3,4]],
			'cap2[0:3]',[0, [57,60,57,60]],
			'mite_fg[0:2]'   ,[[31,31,31], 0],
			'mite_fg0[0]'   ,[[31, 61]],
			'mite2_fg[0]'  ,[[31, 0]],
			'current_ref_fg[0]' ,[[31, 61]],
			'current_ref_bias1[0]' ,[[31, 62]],
			'current_ref_bias2[0]' ,[[32, 62]],
			'ota_bias',[[1, 0],[2,0]],
			'ota2_bias[0]',[[33,62]], #ota in CAB2
			#'ota_biasfb',[[1, 0],[2,0]],
			'meas_fg[1]', [[31, 0],[15,-60],[18,-60]], ## check again
			'meas_fg[0]', [[31, 0],[11,-60],[8,-60]],
			'signalmult_fg[0]',[[32,58]],
			'signalmult_v1p[0]',[[32,59]],
			'signalmult_v1n[0]',[[32,60]],
			'cap2_1x[0:3]',[[28,29,28,29], 0],
			'cap2_2x[0:3]',[[28,29,28,29], 1],
			'cap2_3x[0:3]',[[28,29,28,29], 2]]
		self.dev_fgs = smDictFromList(dev_fgs_sm)

###########################################
#   CLB stats 
###########################################      
class clbStats(stats):
	def __init__(self):
		self.num_inputs = 16
		self.num_outputs = 8
		self.pin_order =['I0','I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','I14','I15','O0','O1','O2','O3','O4','O5','O6','O7']

		chanx_sm = ['T[0:16]', [list(range(20,13,-1))+list(range(12,6,-1))+list(range(5,1,-1)),0],
			'I3',   [ 0,46],     #pin names
			'I7',   [ 0,47],
			'I11',  [ 0,48],
			'I15',  [ 0,49],
			'O3',   [ 0,50],
			'O7',   [ 0,51],
			'XI1',  [ 0,52],
			'XI5',  [ 0,53],
			'XI9',  [ 0,54],
			'XI13', [ 0,55],
			'XO1',  [ 0,56],
			'XO5',  [ 0,57]]
		self.chanx = smDictFromList(chanx_sm, 'remBrak')

		# CHANY    
		chany_sm = ['T[0:16]', [list(range(20,13,-1))+list(range(12,6,-1))+list(range(5,1,-1)),0],
			'I2',   [ 0,39],    #pin names $$ south side right?
			'I6',   [ 0,40],
			'I10',  [ 0,41],
			'I14',  [ 0,42],
			'O2',   [ 0,43],
			'O6',   [ 0,44],
			'XI0',  [ 0,33],
			'XI4',  [ 0,34],
			'XI8',  [ 0,35],
			'XI12', [ 0,36],
			'XO0',  [ 0,37],
			'XO4',  [ 0,38],
			'AXI4',  [ 0,39],#&&& problem AS THIS BLOCK IS IN CLB
			'AXI5',  [ 0,40], #extra pin for D|A|D case 
			'AXI6',  [ 0,41], #extra pin for D|A|D case 
			'AXI7',  [ 0,42], #extra pin for D|A|D case 
			'AXO2',  [ 0,43],#extra guy
			'AXO3',  [ 0,44]] #@@dummy need IA(4,5,6,7)==ID(2,6,10,14)
		self.chany = smDictFromList(chany_sm, 'remBrak')

		# SBLOCK      
		#track direction (these are rotated 90deg ccw from schematic name: ww->W)
		sb_sw = ['T[0:16]', [list(range(20,13,-1))+list(range(12,6,-1))+list(range(5,1,-1)),0],
			'we',[ 0,64],
			'wn',[ 0,61],
			'ws',[ 0,60],
			'ns',[ 0,62],
			'ne',[ 0,63],
			'es',[ 0,59],
			'ew',[ 0,64],
			'nw',[ 0,61],
			'sw',[ 0,60],
			'sn',[ 0,62],
			'en',[ 0,63],
			'se',[ 0,59]]    
		self.sblock = smDictFromList(sb_sw, 'remBrak')  

		#Local Interconnect -- new numbers as of 8/17/14
		li_sm_0 = ['clb.I[0:15]', 'ble[0:7].out[0]']
		li_sm_1 = ['ble[0:7].in[0:3]']
		li_sm = [
			'clb.I[0:15]'        ,[range(21,5,-1), 0],
			'ble[0:7].out[0]'    ,[range(7,-1,-1), 0],
			'ble[0:7].in[0:3]'   ,[0, range(0,32)]]
		self.li0 = recStrExpand(li_sm_0)
		self.li1 = recStrExpand(li_sm_1)
		self.li = smDictFromList(li_sm)

		#CLB Devices
		self.dev_types = ['ble']*8
		self.dev_pins = {'ble':5}          
		dev_fgs_sm = ['ble[0]', [0,0], ## 0 4 8 instead of 2 1 0 as that's the diff btw rsel
			'ble[1]',	[4,0],
			'ble[2]',	[8,0],
			'ble[3]',	[0,22],
			'ble[4]',	[4,22],
			'ble[5]',	[8,22],
			'ble[6]',	[0,44],
			'ble[7]',	[4,44], #offsets
			'0000',     [[22, 3], [25, 0]], #pFET #nFET
			'0001',     [[22, 11], [25, 8]],
			'0010',     [[22, 7], [25, 4]],
			'0011',     [[22, 15], [25, 12]],
			'0100',     [[22, 1], [25, 2]],
			'0101',     [[22, 9], [25, 10]],
			'0110',     [[22, 5], [25, 6]],
			'0111',     [[22, 13], [25, 14]],
			'1000',     [[22, 2], [25, 1]],
			'1001',     [[22, 10], [25, 9]],
			'1010',     [[22, 6], [25, 5]],
			'1011',     [[22, 14], [25, 13]],
			'1100',     [[22, 0], [25, 3]],
			'1101',     [[22, 8], [25, 11]],
			'1110',     [[22, 4], [25, 7]],
			'1111',     [[22, 12], [25, 15]],
			'clk_r',    [0, 0], #default condition after tunnel, probably do need this address
			'clk_g',    [[22, 16], [25,16]],
			'clk_a',    [[22, 17], [25,16]], #used for counter macroblock to chain flipflops
			'res_r',    [0, 0], #default condition after tunnel, probably do need this address
			'res_g',    [[22, 19], [25,18]],#[22, 19], [25,18]
			'res_a',    [0, 0], #does not exist
			'ff_out',   [[22, 20], [25,19]],
			'lut_out',  [0, 0], #default condition after tunnel, probably do need this address
			'ff_in',	[[22,18], [25,17]]] #used for counter macroblock
		self.dev_fgs = smDictFromList(dev_fgs_sm)

class iowStats(stats):
	def __init__(self):
		self.num_inputs = 12
		self.num_outputs = 6
		self.pin_order = [
			'I2','I2','I2','I6','I6','I6','I10','I10','I10','I14','I14','I14','O2','O2','O2','O6','O6','O6']

class ioeStats(stats):
	""" needs real fg numbers --  --done now-sg """
	def __init__(self):
		self.num_inputs = 12 # as we have 4 i/ps...each can be i/p or o/p or clk (thus 4x3 options)
		self.num_outputs = 6 # as we have 2 o/ps (2x3)
		self.pin_order = [
			'E0','E1','E2','E3','E4','E5','E6','IE6','E8','E9','E10','E11','E12','E13','E14','OE3','E16','E17']

		chany_sm = ['T[0:16]', [0,list(range(1,8))+list(range(9,15))+list(range(16,20))],
			'E0' ,  [6,21],
			'E1' ,  [6,21],
			'E2' ,  [0,21],
			'E3' ,  [5,21],
			'E4' ,  [5,21],
			'E5' ,  [0,21],
			'E6' ,  [4,21],
			'E7' ,  [4,21],
			'E8' ,  [0,21],
			'E9' ,  [3,21],
			'E10' ,  [3,21],
			'E11' ,  [0,21],
			'E12' ,  [2,21],
			'E13' ,  [2,21],
			'E14' ,  [0,21],
			'E15' ,  [1,21],
			'E16' ,  [1,21],
			'E17' ,  [0,21],
			'E18' ,  [0,21],
			'E19' ,  [0,21],
			'I4',   [ 6,0],    #pin names
			'I5',   [ 5,0],
			'I6',   [ 4,0],
			'I7',   [ 3,0],
			'O2',   [ 2,0],
			'O3',   [ 1,0],
			'XO0',  [ 2,21], ### to be seen
			'XO1',  [ 1,21],
			'XI0',  [ 6,21],
			'XI1',  [ 5,21],
			'XI2',  [ 4,21],## problem conflict
			'XI3',  [ 3,21], # $$$$
			'IE6',  [4,21], #$$$$ TO BE RESOLVED
			'OE3',  [1,21],
			### To be updated
			'XI2',  [ 0,39],#------to match w/ dif DIgital tile
			'XI6',  [ 0,40], #to match w/ dif tile
			'XI10', [ 0,41],#to match w/ dif tile
			'XI14', [ 0,42],
			'XI4',  [ 0,59],#IO BLOCK io_e
			'XI5',  [ 0,60], #to match w/ dif tile
			#'XI6',  [ 0,61],#to match w/ dif tile
			'XI7',  [ 0,62], # $$might have to include more?? hmmm XI<0,4,8,12?> # $$might have to include more?? hmmm XI<0,4,8,12?>
			'XO2',  [ 0,69], ### PROBLEM FROM i/o same as O2
			'XO3',  [ 0,70],
			'XO2',  [ 0,43],
			'XO6',  [ 0,44]]  # $$ XO<0,4>??
		self.chany = smDictFromList(chany_sm, 'remBrak')	

		self.sblock = {
			'T0':   [ 5, 0],    #track names
			'T1':   [ 4, 0],    
			'T2':   [ 3, 0],
			'T3':   [ 2, 0],
			'T4':   [ 1, 0],
			'T5':   [ 0, 0],
			'T6':   [ 5, 0],
			'T7':   [ 4, 10],
			'T8':   [ 3, 10],
			'T9':   [ 2, 10],
			'T10':  [ 1, 10],
			'T11':  [ 0, 10],
			'T12':  [ 6, 20],
			'T13':  [ 4, 20],
			'T14':  [ 3, 20],
			'T15':  [ 2, 20],
			'T16':  [ 1, 20],
			'ns':   [ 0,3+42], #actual ew  #track direction++ ADDING +14 for this row
			'ne':   [ 0,4+42], #es
			'nw':   [ 0,2+42], #en
			'ew':   [ 0,5+42], #sn
			'es':   [ 0,0+42], #sw
			'sw':   [ 0,1+42], #wn
			'sn':   [ 0,3+42], #we
			'en':   [ 0,4+42], #se
			'wn':   [ 0,2+42], #ne
			'we':   [ 0,5+42], #ns
			'se':   [ 0,0+42], #ws
			'ws':   [ 0,1+42]} #nw

		self.dev_fgs = {
			'c4_out[0]':          [[22,13],[18,13]],
			'tgate_in[0]':    	  [[ 21, 13],[ 9, 11]],    #last switch is for bias
			'c4_out[1]':    	  [[26,13],[25,13]],
			'tgate_in[1]':    	  [[27,13]],
			'tgate[0]':			  [[8,25],[7,26]],
			'tgate[1]':			  [[8,26],[7,25]],
			'int[0]':             [[7,27]],              #offsets were wrong--ss
			'int[1]':             [[8,27]],
			'int[2]':             [[7,28]],
			'int[3]':             [[8,28]],
			'int[4]':             [[7,29]],
			'int[5]':             [[8,29]]}

		##row address for local interconnect    
		self.li = {
			'I4':				[7,38],
			'I5':				[7,36],
			'I6':				[7,34],
			'I7':				[8,38],
			'O2':				[8,36],
			'O3':				[8,34],
			'tgate[0]':			[0,0],
			'tgate[1]':			[0,0],
			'c4_out[0]':        [ 0, 7],    #io pin names
			'tgate_in[0]':   	[ 0, 6],
			'c4_out[1]':        [ 0,13],
			'tgate_in[1]':	[ 0,12]}   

class ioelStats(stats):
	""" needs real fg numbers --  --done now-sg """
	def __init__(self):
		self.num_inputs = 12 # as we have 4 i/ps...each can be i/p or o/p or clk (thus 4x3 options)
		self.num_outputs = 6 # as we have 2 o/ps (2x3)
		self.pin_order = [
			'I4','I4','I4','I5','I5','I5','I6','I6','I6','I7','I7','I7','O2','O2','O2','O3','O3','O3']

		chany_sm = ['T[0:16]', [0,list(range(1,8))+list(range(9,15))+list(range(16,20))],
			'I4',   [ 6,0],    #pin names
			'I5',   [ 5,0],
			'I6',   [ 4,0],
			'I7',   [ 3,0],
			'O2',   [ 2,0],
			'O3',   [ 1,0],
			'XO0',  [ 2,21], ### to be seen
			'XO1',  [ 1,21],
			'XI0',  [ 6,21],
			'XI1',  [ 5,21],
			'XI2',  [ 4,21],## problem conflict
			'XI3',  [ 3,21],
			### To be updated
			'XI2',  [ 0,39],#------to match w/ dif DIgital tile
			'XI6',  [ 0,40], #to match w/ dif tile
			'XI10', [ 0,41],#to match w/ dif tile
			'XI14', [ 0,42],
			'XI4',  [ 0,59],#IO BLOCK io_e
			'XI5',  [ 0,60], #to match w/ dif tile
			'XI6',  [ 0,61],#to match w/ dif tile
			'XI7',  [ 0,62], # $$might have to include more?? hmmm XI<0,4,8,12?> # $$might have to include more?? hmmm XI<0,4,8,12?>
			'XO2',  [ 0,69], ### PROBLEM FROM i/o same as O2
			'XO3',  [ 0,70],
			'XO2',  [ 0,43],
			'XO6',  [ 0,44]]  # $$ XO<0,4>??
		self.chany = smDictFromList(chany_sm, 'remBrak')	

		self.sblock = {
			'T0':   [ 5, 12],    #track names
			'T1':   [ 4, 12],    
			'T2':   [ 3, 12],
			'T3':   [ 2, 12],
			'T4':   [ 1, 12],
			'T5':   [ 0, 12],
			'T6':   [ 5, 12],
			'T7':   [ 4, 6],
			'T8':   [ 3, 6],
			'T9':   [ 2, 6],
			'T10':  [ 1, 6],
			'T11':  [ 0, 6],
			'T12':  [ 6, 0],
			'T13':  [ 4, 0],
			'T14':  [ 3, 0],
			'T15':  [ 2, 0],
			'T16':  [ 1, 0],
			'ns':   [ 0,3+14], #actual ew  #track direction++ ADDING +14 for this row
			'ne':   [ 0,4+14], #es
			'nw':   [ 0,2+14], #en
			'ew':   [ 0,5+14], #sn
			'es':   [ 0,0+14], #sw
			'sw':   [ 0,1+14], #wn
			'sn':   [ 0,3+14], #we
			'en':   [ 0,4+14], #se
			'wn':   [ 0,2+14], #ne
			'we':   [ 0,5+14], #ns
			'se':   [ 0,0+14], #ws
			'ws':   [ 0,1+14]} #nw     
 
class ioeStats11(stats):
	""" needs real fg numbers --  --done now-sg """
	def __init__(self):
		self.num_inputs = 12 # as we have 4 i/ps...each can be i/p or o/p or clk (thus 4x3 options)
		self.num_outputs = 6 # as we have 2 o/ps (2x3)
		self.pin_order = [
			'I4','I4','I4','I5','I5','I5','I6','I6','I6','I7','I7','I7','O2','O2','O2','O3','O3','O3']

		chany_sm = ['T[0:16]', [list(range(32,26,-1))+list(range(32,26,-1))+[33]+list(range(31,27,-1)),0],
			'I4',   [ 0,65],    #pin names
			'I5',   [ 0,66],
			'I6',   [ 0,67],
			'I7',   [ 0,68],
			'O2',   [ 0,69],
			'O3',   [ 0,70],
			'XO0',  [ 0,63],
			'XO1',  [ 0,64],
			'XI0',  [ 0,59],
			'XI1',  [ 0,60],
			'XI2',  [ 0,61],## problem conflict
			'XI3',  [ 0,62],
			'XI2',  [ 0,39],#------to match w/ dif DIgital tile
			'XI6',  [ 0,40], #to match w/ dif tile
			'XI10', [ 0,41],#to match w/ dif tile
			'XI14', [ 0,42],
			'XI4',  [ 0,59],#IO BLOCK io_e
			'XI5',  [ 0,60], #to match w/ dif tile
			'XI6',  [ 0,61],#to match w/ dif tile
			'XI7',  [ 0,62], # $$might have to include more?? hmmm XI<0,4,8,12?> # $$might have to include more?? hmmm XI<0,4,8,12?>
			'XO2',  [ 0,69], ### PROBLEM FROM i/o same as O2
			'XO3',  [ 0,70],
			'XO2',  [ 0,43],
			'XO6',  [ 0,44]]  # $$ XO<0,4>??
		self.chany = smDictFromList(chany_sm, 'remBrak')	

		self.sblock = {
			'T0':   [ 32, 42],    #track names # 42 is the vd offset..inside cab vd<0:5>
			'T1':   [ 31, 42],    
			'T2':   [ 30, 42],
			'T3':   [ 29, 42],
			'T4':   [ 28, 42],
			'T5':   [ 27, 42],
			'T6':   [ 32, 52],	#track names # 52 is the vd offset..inside cab vd<10:15>
			'T7':   [ 31, 52],
			'T8':   [ 30, 52],
			'T9':   [ 29, 52],
			'T10':  [ 28, 52],
			'T11':  [ 27, 52],
			'T12':  [ 33, 62],	#track names # 62 is the vd offset..inside cab vd<20:25>
			'T13':  [ 31, 62],
			'T14':  [ 30, 62],
			'T15':  [ 29, 62],
			'T16':  [ 28, 62],
			'ns':   [ 0,3], #actual ne   #track direction++ ADDING +14 for this row
			'ne':   [ 0,4], #se
			'nw':   [ 0,2], #ne
			'ew':   [ 0,5], # ns
			'es':   [ 0,0], #sw
			'sw':   [ 0,1], #nw
			'sn':   [ 0,3], #en
			'en':   [ 0,4],
			'wn':   [ 0,2],
			'we':   [ 0,5],
			'se':   [ 0,0],
			'ws':   [ 0,1]}

		self.dev_fgs = {
			'c4_out[0]':          [[22,13],[18,13]],
			'tgate_in[0]':    	  [[ 21, 13],[ 9, 11]],    #last switch is for bias
			'c4_out[1]':    	  [[26,13],[25,13]],
			'tgate_in[1]':    	  [[27,13]],
			'int[0]':             [[16, 8]],
			'int[1]':             [[16, 9]],
			'int[2]':             [[16,10]],
			'int[3]':             [[16,11]],
			'int[4]':             [[16,12]],
			'int[5]':             [[16,13]]}

		##row address for local interconnect    
		self.li = {
			'I0':               [13, 0],    #pin names from self.array
			'I1':               [14, 0],
			'I2':               [15, 0],
			'I3':               [13, 0],
			'O0':               [14, 0],
			'O1':               [15, 0],
			'c4_out[0]':        [ 0, 7],    #io pin names
			'tgate_in[0]':   	[ 0, 6],
			'c4_out[1]':        [ 0,13],
			'tgate_in[1]':	[ 0,12]}   

class iosdStats(stats):
	def __init__(self):
		self.num_inputs = 12
		self.num_outputs = 6
		self.pin_order = [
			'I3','I3','I3','I7','I7','I7','I11','I11','I11','I15','I15','I15','O3','O3','O3','O7','O7','O7']

		chanx_sm = ['T[0:16]', [[31,30,28,27,26,24,23,21,20,19,18,17,16,14,13,12,11], 0],
			'I3'   ,[ 0,17], #pin names
			'I7'   ,[ 0,18], #physical le<0:5>
			'I11'  ,[ 0,19],
			'I15'  ,[ 0,20],
			'O3'   ,[ 0,21],
			'O7'   ,[ 0,22],
			'XI1'  ,[ 0,23], #physical lw<0:5>
			'XI5'  ,[ 0,24],
			'XI9'  ,[ 0,25],
			'XI13' ,[ 0,26],
			'XO1'  ,[ 0,27],
			'XO5'  ,[ 0,28]]   
		self.chanx = smDictFromList(chanx_sm, 'remBrak')

		self.sblock = {
			'T0':   [ 8, 6],    #track names +3 as vd<0> inside translates to vd<3> thus vd<6:13>~ vd<9:16>
			'T1':   [ 7, 6],    
			'T2':   [ 6, 6],
			'T3':   [ 5, 6],
			'T4':   [ 4, 6],
			'T5':   [ 1, 6],
			'T6':   [ 2, 6],
			'T7':   [ 0, 6],
			'T8':   [ 9, 0],
			'T9':   [ 8, 0],
			'T10':  [ 7, 0],
			'T11':  [ 6, 0],
			'T12':  [ 5, 0],
			'T13':  [ 3, 0],
			'T14':  [ 2, 0],
			'T15':  [ 1, 0],
			'T16':  [ 0, 0],
			'ns':   [ 0,20],    #track direction
			'ne':   [ 0,21],
			'nw':   [ 0,19],
			'ew':   [ 0,22],
			'es':   [ 0,17],
			'sw':   [ 0,18],
			'sn':   [ 0,20],
			'en':   [ 0,21],
			'wn':   [ 0,19],
			'we':   [ 0,22],  	
			'se':   [ 0,17],
			'ws':   [ 0,18]}
		#these are specific FGs (for Tgate) to be turned on
		#starting io_pad pin
		self.dev_fgs = {
			'tgate[0]':          [[18,13],[14,13]],
			'ana_buff_in[0]':    [[17, 13],[ 5, 11]],    #last switch is for bias
			'ana_buff_out[0]':   [[16, 13],[ 7, 13]],
			'ana_buff_out2[0]':  [[16, 13],[ 7, 13],[ 9, 1]],
			'dig_buff_in[0]':    [[19,13],[20,13]],
			'dig_buff_out[0]':   [[15,13]],
			'tgate[1]':          [[26,13],[27,13]],
			'ana_buff_in[1]':    [[30,13],[5, 2]],
			'ana_buff_out[1]':   [[24,13],[28,13]],
			'ana_buff_out2[1]':  [[24,13],[28,13],[9,0]],
			'dig_buff_in[1]':    [[22,13],[21,13]],
			'dig_buff_out[1]':   [[23,13]],
			'int[0]':            [[12, 8]],
			'int[1]':            [[12, 9]],
			'int[2]':            [[12,10]],
			'int[3]':            [[12,11]],
			'int[4]':            [[12,12]],
			'int[5]':            [[12,13]]}

		self.li = {
			'I3':                [ 9, 0],    #pin names from self.array
			'I7':                [10, 0],
			'I11':               [11, 0],
			'I15':               [ 9, 0],
			'O3':                [10, 0],
			'O7':                [11, 0],
			'tgate[0]':          [ 0, 7],    #io pin names
			'ana_buff_in[0]':    [ 0, 6],
			'ana_buff_out[0]':   [ 0, 5],
			'dig_buff_in[0]':    [ 0, 4],
			'dig_buff_out[0]':   [ 0, 3],
			'tgate[1]':          [ 0,13],
			'ana_buff_in[1]':    [ 0,12],
			'ana_buff_out[1]':   [ 0,11],
			'dig_buff_in[1]':    [ 0,10],
			'dig_buff_out[1]':   [ 0, 9]}

class iosaStats(stats):
	""" needs real fg numbers -- just copied from iosd --done now-sg """
	def __init__(self):
		self.num_inputs = 12 # as we have 4 i/ps...each can be i/p or o/p or clk (thus 4x3 options)
		self.num_outputs = 6 # as we have 2 o/ps (2x3) KInda irrelevant as all of these are I/Os
		self.pin_order = [
			'I8','I8','I8','I9','I9','I9','I13','I13','I13','I14','I14','I14','I15','I15','I15','O4','O4','O4']

		#chanx_sm = ['T[0:16]', [[31,30,28,27,26,24,23,21,20,19,18,17,16,14,13,12,11], 0],
		chanx_sm = ['T[0:16]', [ [32,31,30,29,28,27,26,24,23,22,21,20,19,17,16,15,14], 0],
			'I8'   ,[ 0,17],    #pin names # 14(COL_OFFSET)+3(OFFSET)
			'I9'   ,[ 0,18],
			'I13'  ,[ 0,19],
			'I14'  ,[ 0,20],
			'I15'  ,[ 0,21],
			'O4'   ,[ 0,22],
			'XI10' ,[ 0,23],
			'XI11' ,[ 0,24],
			'XI12' ,[ 0,25],
			'XO5'  ,[ 0,26],
			'XO6'  ,[ 0,27],
			'XO7'  ,[ 0,28]]  
		self.chanx = smDictFromList(chanx_sm, 'remBrak')

		self.sblock = {
			'T0':   [ 12, 6],    #track names
			'T1':   [ 11, 6],    
			'T2':   [ 10, 6],
			'T3':   [ 9, 6],
			'T4':   [ 8, 6],
			'T5':   [ 5, 6],
			'T6':   [ 6, 6],
			'T7':   [ 4, 6],
			'T8':   [ 13, 0],
			'T9':   [ 12, 0],
			'T10':  [ 11, 0],
			'T11':  [ 10, 0],
			'T12':  [ 9, 0],
			'T13':  [ 7, 0],
			'T14':  [ 6, 0],
			'T15':  [ 5, 0],
			'T16':  [ 4, 0],
			'ns':   [ 0,20], #actual ne   #track direction++ ADDING +14 for this row
			'ne':   [ 0,21], #se
			'nw':   [ 0,19], #ne
			'ew':   [ 0,22], # ns
			'es':   [ 0,17], #sw
			'sw':   [ 0,18], #nw
			'sn':   [ 0,20], #en
			'en':   [ 0,21],
			'wn':   [ 0,19],
			'we':   [ 0,22],
			'se':   [ 0,17],
			'ws':   [ 0,18]}

		self.dev_fgs = {
			'tgate[0]':           [[22,13],[18,13]],
			'ana_buff_in[0]':     [[ 21, 13],[ 9, 11]],    #last switch is for bias
			'ana_buff_out[0]':    [[ 20, 13],[ 11, 13]],
			'ana_buff_out2[0]':   [[ 20, 13],[ 13, 1]],
			'dig_buff_in[0]':     [[23,13],[19,13]],
			'dig_buff_out[0]':    [[19,13]],
			'tgate[1]':           [[30,13],[31,13]],
			'ana_buff_in[1]':     [[29, 13],[9, 2]], #$$ no3rd switch
			'ana_buff_out[1]':    [[28, 13],[32,13]],
			'ana_buff_out2[1]':   [[28, 13],[ 13, 0]],
			'dig_buff_in[1]':     [[26,13],[25,13]],
			'dig_buff_out[1]':    [[27,13]],
			'int[0]':             [[16, 8]],
			'int[1]':             [[16, 9]],
			'int[2]':             [[16,10]],
			'int[3]':             [[16,11]],
			'int[4]':             [[16,12]],
			'int[5]':             [[16,13]]}

		##row address for local interconnect    
		self.li = {
			'I8':               [13, 0],    #pin names from self.array
			'I9':               [14, 0],
			'I13':              [15, 0],
			'I14':              [13, 0],
			'I15':              [14, 0],
			'O4':               [15, 0],
			'tgate[0]':         [ 0, 7],    #io pin names
			'ana_buff_in[0]':   [ 0, 6],
			'ana_buff_out[0]':  [ 0, 5],
			'dig_buff_in[0]':   [ 0, 4],
			'dig_buff_out[0]':  [ 0, 3],
			'tgate[1]':         [ 0,13],
			'ana_buff_in[1]':   [ 0,12],
			'ana_buff_out[1]':  [ 0,11],
			'dig_buff_in[1]':   [ 0,10],
			'dig_buff_out[1]':  [ 0, 9]}        

class iondStats(stats):
	def __init__(self):
		self.num_inputs = 12
		self.num_outputs = 6
		self.pin_order = [
			'I1','I1','I1','I5','I5','I5','I9','I9','I9','I13','I13','I13','O1','O1','O1','O5','O5','O5']

		#these are specific FGs (for Tgate) to be turned on
		#starting io_pad pin
		self.dev_fgs = {
			'tgate[0]':          [[18,0],[14,0]],
			'ana_buff_in[0]':    [[17, 0],[ 5, 2]],    #last switch is for bias
			'ana_buff_out[0]':   [[16, 0],[ 7, 0]],
			'ana_buff_out2[0]':  [[16, 0],[ 7, 0],[ 9, 12]],
			'dig_buff_in[0]':    [[19,0],[20,0]],
			'dig_buff_out[0]':   [[15,0]],
			'tgate[1]':          [[26,0],[13,0]],
			'ana_buff_in[1]':    [[8,0],[5, 11]],
			'ana_buff_out[1]':   [[6,0],[30,0]],
			'ana_buff_out2[1]':  [[6,0],[30,0],[9,13]],
			'dig_buff_in[1]':    [[22,0],[21,0]],
			'dig_buff_out[1]':   [[3,0]],
			'int[0]':            [[12, 5]],
			'int[1]':            [[12, 4]],
			'int[2]':            [[12,3]],
			'int[3]':            [[12,2]],
			'int[4]':            [[12,1]],
			'int[5]':            [[12,0]]}

		self.li = {
			'I1':                [ 9, 0],    #pin names from self.array
			'I5':                [10, 0],
			'I9':               [11, 0],
			'I13':               [ 9, 0],
			'O1':                [10, 0],
			'O5':                [11, 0],
			'tgate[0]':          [ 0, 6],    #io pin names
			'ana_buff_in[0]':    [ 0, 7],
			'ana_buff_out[0]':   [ 0, 8],
			'dig_buff_in[0]':    [ 0, 9],
			'dig_buff_out[0]':   [ 0, 10],
			'tgate[1]':          [ 0,0],
			'ana_buff_in[1]':    [ 0,1],
			'ana_buff_out[1]':   [ 0,2],
			'dig_buff_in[1]':    [ 0,3],
			'dig_buff_out[1]':   [ 0, 4]}

class ionaStats(stats):
	""" needs real fg numbers -- just copied from iosd --done now-sg """
	def __init__(self):
		self.num_inputs = 12 # as we have 4 i/ps...each can be i/p or o/p or clk (thus 4x3 options)
		self.num_outputs = 6 # as we have 2 o/ps (2x3) KInda irrelevant as all of these are I/Os
		self.pin_order = [
			'I10','I10','I10','I11','I11','I11','I12','I12','I12','O5','O5','O5','O6','O6','O6','O7','O7','O7']

		self.dev_fgs = {
			'tgate[0]':           [[22,0],[18,0]],
			'ana_buff_in[0]':     [[ 21, 0],[ 9, 2]],    #last switch is for bias
			'ana_buff_out[0]':    [[ 20, 0],[ 11, 0]],   #last switch is for bias
			'ana_buff_out2[0]':   [[ 20, 0],[ 13, 12]], 
			'dig_buff_in[0]':     [[23,0],[24,0]],
			'dig_buff_out[0]':    [[19,0]],
			'tgate[1]':           [[30,0],[31,0]],
			'ana_buff_in[1]':     [[29, 0],[9,11]], #$$ no3rd switch
			'ana_buff_out[1]':    [[28, 0],[32,0]], #last switch is for bias
			'ana_buff_out2[1]':   [[28, 0],[ 13, 13]], 
			'dig_buff_in[1]':     [[26,0],[25,0]],
			'dig_buff_out[1]':    [[27,0]],
			'int[0]':             [[16, 5]],
			'int[1]':             [[16, 4]],
			'int[2]':             [[16,3]],
			'int[3]':             [[16,2]],
			'int[4]':             [[16,1]],
			'int[5]':             [[16,0]]}

		##row address for local interconnect    
		self.li = {
			'I10':               [13, 0],    #pin names from self.array
			'I11':               [14, 0],
			'I12':              [15, 0],
			'O5':              [13, 0],
			'O6':              [14, 0],
			'O7':               [15, 0],
			'tgate[0]':         [ 0, 6],    #io pin names
			'ana_buff_in[0]':   [ 0, 7],
			'ana_buff_out[0]':  [ 0, 8],
			'dig_buff_in[0]':   [ 0, 9],
			'dig_buff_out[0]':  [ 0, 10],
			'tgate[1]':         [ 0,0],
			'ana_buff_in[1]':   [ 0,1],
			'ana_buff_out[1]':  [ 0,2],
			'dig_buff_in[1]':   [ 0,3],
			'dig_buff_out[1]':  [ 0, 4]}        

class array(pbarray):
	def __init__(self):
		xsize = len(arrayStats.pattern)
		ysize = len(arrayStats.pattern[0])
		super(array, self).__init__(xsize, ysize)
		self.name = 'rasp30_array'

class clb(complexBlock):
	def __init__(self, name):
		self.name = name
		self.type = 'CLB'
		self.stats = clbStats()
		self.array_stats = arrayStats()
		self.subblocks = []

		#CLB ports
		self.inputs = ['open']*self.stats.num_inputs
		self.outputs = ['open']*self.stats.num_outputs

		#CLB Devices
		dev_types = self.stats.dev_types
		dev_pins = self.stats.dev_pins    
		self.addSubs(dev_types, dev_pins)

	def genLI(self, *var):
		verbose = 0
		if len(var) == 1: verbose = 1
		self.swcs = []        

		# inputs to local interconnect--
		# inputs to CAB + outputs from DEVs
		self.li_in_in = self.inputs
		self.li_in_dev = []
		for i in range(len(self.subblocks)):
			self.li_in_dev.append(self.getSub(i).outputs)
		self.li_in = self.li_in_in + self.li_in_dev

		# outputs from local interconnect--
		# inputs to DEVs + outputs from CAB
		self.li_out_out = self.outputs
		self.li_out_dev = []
		for i in range(len(self.subblocks)):
			for j in range(len(self.getSub(i).inputs)):
				self.li_out_dev.append(self.getSub(i).inputs[j])
		self.li_out = self.li_out_dev + self.li_out_out
		self.li = [[0]*len(self.li_in) for x in self.li_out]

		#printing connectivity matrix
		x = 2
		for i in range(len(self.li_in)):
			print ('%s'%str(i).ljust(2),)
		print ()

		for i in range(len(self.li_in)):
			if self.li_in[i] != 'open':
				if verbose: print ('%s'%self.li_in[i].ljust(x),)
			else:
				if verbose: print (''.ljust(x),)
		if verbose: print ()

		for i in range(len(self.li_out_dev)):
			if self.li_out[i] != 'open':
				for j in range(len(self.li_in)):
					if self.li_out[i] == self.li_in[j]:
						if verbose: print (str('X').ljust(x),)
						self.li[i][j] = 1
					else:
						if verbose: print (str('.').ljust(x),)
				if verbose: 
					print (self.li_out[i].ljust(2),) 
					print (str(i).ljust(2))
			else:
				for j in range(len(self.li_in)):
					if verbose: print (str('.').ljust(x),)
				if verbose: print ('%s%s'%(''.ljust(3), str(i).ljust(2)))    

		#actually generating the switch addresses here    
		self.swcsFromLi()

	def dispLI(self):
		self.genLI('verbose')

	########################################## gen dev fgs for bles!!    
	def genDevFgs(self): 
		verbose = 1
		for i in range(len(self.subblocks)):
			sb = self.getSub(i)
			## set initial conditions
			TT=['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
			KK=[]
			TT=set(TT)
			# add if counter8
			# make ble[0] then variable containing ble[1-7]
			# for each ble make a kk list of clb.dev_fgs for counter support
			# run through similar switch generation as normal lut/ff
			if sb.outputs != 'open':
				#this generates the FG addresses for the LUT states
				# need to add the FG addresses for BLE configuration
				# LUT -> out, FF -> out, clk and reset select, etc
				#pdb.set_trace()
				ex_fgs_orig = sb.ex_fgs
				p0 = sb.inputs_orig
				#p0.reverse() #need to reverse ble input order, not sure why, but it works
				p1 = sb.inputs 
				print ("ble input re-ordered")
				print (p0)
				print (p1)
				if ex_fgs_orig[0] == 'ff_in': #counter lut hack
					kk = ex_fgs_orig              
				elif ex_fgs_orig[-1] == 'ff_out': #flip flop lut hack
					kk = lutExpand(ex_fgs_orig[:-2], p0, p1) 
					KK=set(kk)
					kk=TT.difference(KK)
					kk=list(kk) # return as list
					kk.append('res_g')
					kk.append('ff_out')
				else:
					kk = lutExpand(ex_fgs_orig, p0, p1)
					KK=set(kk)
					kk=TT.difference(KK) ## take difference of list
					kk=list(kk) # return as list
				sb.ex_fgs = kk
				swc_name0 = sb.name
				swc0 = self.stats.dev_fgs[swc_name0]
				for j in kk: ##all truth table values
					swc_name1 = j
					swc2 = self.stats.dev_fgs[swc_name1]
					for n in range(len(swc2)):
						if isinstance(swc2[0],int):
							swc1=swc2
						else:
							swc1=swc2[n]
						swc = [swc0[0]+swc1[0], swc0[1]+swc1[1]]
						swcx = self.array_stats.getTileOffset(swc, self.grid_loc)
						if verbose: print ('999%s %s -> (%g %g) -> (%g %g)'%(swc_name0, swc_name1, swc[0], swc[1], swcx[0], swcx[1]))
						self.swcs.append(swcx)

class cab(complexBlock):
	def __init__(self, name):
		self.name = name
		self.type = 'CAB'
		self.stats = cabStats()     
		self.array_stats = arrayStats()
		self.subblocks = []

		#CAB ports
		self.inputs = ['open']*self.stats.num_inputs
		self.outputs = ['open']*self.stats.num_outputs

		#CAB Devices
		dev_types = self.stats.dev_types
		dev_pins = self.stats.dev_pins 
		self.addSubs(dev_types, dev_pins)

	def genLI(self, *var):
		self.swcs = []
		verbose = 0
		if len(var) == 1: verbose = 1

		# inputs to local interconnect--
		# inputs to CAB + outputs from DEVs
		for pwr in range(len(self.inputs)):
			if self.inputs[pwr] in ['gnd','vcc']:
				self.inputs[pwr]='open'

		self.li_in_in = ['gnd','vcc']+self.inputs
		self.li_in_dev = []
		for i in range(len(self.subblocks)):
			if isinstance(self.getSub(i).outputs,str):
				self.getSub(i).outputs= self.getSub(i).outputs.split()
			for j in range(len(self.getSub(i).outputs)):
				self.li_in_dev.append(self.getSub(i).outputs[j])
		self.li_in_dev.reverse()
		self.li_in = self.li_in_in + self.li_in_dev

		# outputs from local interconnect--
		# inputs to DEVs + outputs from CAB
		self.li_out_out = self.outputs
		self.li_out_dev = []
		for i in range(len(self.subblocks)):
			for j in range(len(self.getSub(i).inputs)):
				self.li_out_dev.append(self.getSub(i).inputs[j])      
		self.li_out = self.li_out_dev+self.li_out_out 
		self.li = [[0]*len(self.li_in) for x in self.li_out]
		#printing connectivity matrix and filling the local interconnect matrix
		x = 2
		for i in range(len(self.li_in)):
			if verbose: print ('%s'%str(i).ljust(2),)
		if verbose: print ()
		for i in range(len(self.li_in)):
			if self.li_in[i] != 'open':
				if verbose: print ('%s'%self.li_in[i].ljust(x),)
			else:
				if verbose: print (''.ljust(x),)
		if verbose: print ()
		for i in range(len(self.li_out_dev)):
			if self.li_out[i] != 'open':
				for j in range(len(self.li_in)):
					if self.li_out[i] == self.li_in[j]:
						if verbose: print (str('X').ljust(x),)
						self.li[i][j] = 1
					else:
						if verbose: print (str('.').ljust(x),)
				if verbose: 
					print (self.li_out[i].ljust(2),) 
					print (str(i).ljust(2))
			else:
				for j in range(len(self.li_in)):
					if verbose: print (str('.').ljust(x),)
				if verbose: print ('%s%s'%(''.ljust(3), str(i).ljust(2)))
		for i in range(len(self.li_out_out)):
			for j in range(len(self.li_in_in)):
				if verbose: print (''.ljust(x),)
			for j in range(len(self.li_in_dev)):
				if self.li_out_out[i] == self.li_in_dev[j] and self.li_out_out[i] != 'open':
					if verbose: print ('X'.ljust(x),)
					self.li[i+len(self.li_out_dev)][j+len(self.li_in_in)] = 1
				else:
					if verbose: print ('.'.ljust(x),)
			if self.li_out_out[i] == 'open':
				if verbose: print (self.li_out_out[i])
			else:
				if verbose: print (self.li_out_out[i])

		#actually generating the switches addresses here  
		self.swcsFromLi()    
                 
	def dispLI(self):
		self.genLI('verbose')

	def genDevFgs(self):
		print ("getting here!")
		verbose = 1
		for i in range(len(self.subblocks)):
			sb = self.getSub(i)
			if sb.outputs != 'open':
				swc_name0 = sb.name
				print("\nSubblock Name: " + swc_name0)
				if sb.ex_fgs:
					ex_fg=sb.ex_fgs.split("&")
					print("\n Extra FGs: " + sb.ex_fgs)
					for s in range(len(ex_fg)):
						for j in ex_fg[s].split()[::2]:
							if swc_name0 in["c4_sp[0]","TIA_blk[0]","lpf[0]","hhneuron[0]","ramp_fe[0]",'nmirror[0]','ichar_nfet[0]']:
								swc_name1 = j
							elif swc_name0 in ["vmm4x4_SR[0]","vmm4x4_SR2[0]","vmm8x4_SR[0]",'vmm4x4[0]','vmm8x4[0]','vmm8x4_in[0]','vmm12x1[0]','vmm12x1_wowta[0]','DAC_sftreg[0]','vmm8inx8in[0]']:
								swc_name1 = j+'['+sb.name.split('[')[1]
								if swc_name0 in ['vmm4x4_SR[0]','vmm4x4_SR2[0]','vmm4x4[0]']:
									vmm_size=16
									vmm_str='vmm4x4_target'
								elif swc_name0 in ['vmm12x1[0]','vmm12x1_wowta[0]']:
									vmm_size=12
									vmm_str='vmm12x1_target'
								elif swc_name0 in ['DAC_sftreg[0]']:
									vmm_size=16
									vmm_str='DAC_sftreg_target'
								elif swc_name0 in ['vmm8x4_in[0]']:
									vmm_size=32
									vmm_str='vmm8x4_in_target'
								elif swc_name0 in ['vmm8x4[0]']:
									vmm_size=32
									vmm_str='vmm8x4_target'
								elif swc_name0 in ['vmm8inx8in[0]']:
									vmm_size=64
									vmm_str='vmm8inx8in_target'
								if swc_name1 in ['vmm4x4_target[0]','vmm8x4_target[0]','vmm8x4_in_target[0]','vmm12x1_target[0]','DAC_sftreg_target[0]','vmm8inx8in_target[0]']:
									targets=list(ex_fg[s].split("=")[1].split(","))
									for h in range(0,vmm_size):
										swc_name1=vmm_str+'['+str(h)+']'
										swc2 = self.stats.dev_fgs[swc_name1]
										swcx = self.array_stats.getTileOffset(swc2, self.grid_loc)
										swcx.append(targets[h])
										swcx.append(1)
										self.swcs.append(swcx)
										if verbose: print ('%s %s -> (%g %g) -> (%g %g)'%(swc_name0, swc_name1, swc2[0], swc2[1], swcx[0], swcx[1]))
									continue
								elif swc_name1=='vmm_bias[0]':
									targets=list(ex_fg[s].split("=")[1].split(","))
									for h in range(0,4):
										swc_name1='vmm_bias['+str(h)+']'
										swc2 = self.stats.dev_fgs[swc_name1]
										swcx = self.array_stats.getTileOffset(swc2, self.grid_loc)
										swcx.append(targets[h])
										swcx.append(1)
										self.swcs.append(swcx)
										if verbose: print ('%s %s -> (%g %g) -> (%g %g)'%(swc_name0, swc_name1, swc2[0], swc2[1], swcx[0], swcx[1]))
									continue
								else:
									swc_name1 = j+'['+sb.name.split('[')[1]
							else:
								swc_name1 = j+'['+sb.name.split('[')[1]
							swc0 = self.stats.dev_fgs[swc_name0]
							swc2 = self.stats.dev_fgs[swc_name1]
							for n in range(len(swc2)):
								if isinstance(swc2[0],int):
									swc1=swc2
								else:
									swc1=swc2[n]
								swc = [swc0[0]+swc1[0], swc0[1]+swc1[1]]
								swcx = self.array_stats.getTileOffset(swc, self.grid_loc)
								if verbose: print ('%s %s -> (%g %g) -> (%g %g)'%(swc_name0, swc_name1, swc[0], swc[1], swcx[0], swcx[1]))
								if n==0 and swc_name1 not in ['sftreg_fg[0]', 'DAC_sftreg_fg[0]','sftreg2_fg[0]','sftreg3_fg[0]','sftreg4_fg[0]','nfet_i2v_fg[0]','pfet_i2v_fg[0]','i2v_pfet_gatefgota_fg[0]','mismatch_meas_fg[0]','mmap_ls_fg[0]','mmap_ls_in_r0_vdd[0]','mmap_ls_in_r0[0]','mmap_ls_in_r1_vdd[0]','mmap_ls_in_r1[0]','mmap_ls_in_r2_vdd[0]','mmap_ls_in_r2[0]','mmap_ls_in_r3_vdd[0]','mmap_ls_in_r3[0]','mmap_ls_in_r4_vdd[0]','mmap_ls_in_r4[0]','mmap_ls_in_r5_vdd[0]','mmap_ls_in_r5[0]','mmap_ls_in_r6_vdd[0]','mmap_ls_in_r6[0]','mmap_ls_in_r7_vdd[0]','mmap_ls_in_r7[0]','mmap_ls_in_r8_vdd[0]','mmap_ls_in_r8[0]','mmap_ls_in_r9_vdd[0]','mmap_ls_in_r9[0]','mmap_ls_in_r10_vdd[0]','mmap_ls_in_r10[0]','mmap_ls_in_r11_vdd[0]','mmap_ls_in_r11[0]','mmap_ls_in_r12_vdd[0]','mmap_ls_in_r12[0]','mmap_ls_in_r13_vdd[0]','mmap_ls_in_r13[0]','mmap_ls_in_r14_vdd[0]','mmap_ls_in_r14[0]','mmap_ls_in_r15_vdd[0]','mmap_ls_in_r15[0]','mmap_ls_in_r16_vdd[0]','mmap_ls_in_r16[0]','mmap_ls_in_r17_vdd[0]','mmap_ls_in_r17[0]','mmap_ls_in_r18_vdd[0]','mmap_ls_in_r18[0]','mmap_ls_in_r19_vdd[0]','mmap_ls_in_r19[0]','mmap_ls_in_r20_vdd[0]','mmap_ls_in_r20[0]','mmap_ls_in_r21_vdd[0]','mmap_ls_in_r21[0]','mmap_ls_in_r22_vdd[0]','mmap_ls_in_r22[0]','mmap_ls_in_r23_vdd[0]','mmap_ls_in_r23[0]','mmap_ls_in_r24_vdd[0]','mmap_ls_in_r24[0]','mmap_ls_in_r25_vdd[0]','mmap_ls_in_r25[0]','mmap_ls_in_r26_vdd[0]','mmap_ls_in_r26[0]','mmap_ls_in_r27_vdd[0]','mmap_ls_in_r27[0]','mmap_ls_in_r28_vdd[0]','mmap_ls_in_r28[0]','mmap_ls_in_r29_vdd[0]','mmap_ls_in_r29[0]','mmap_ls_in_vdd1_vdd[0]','mmap_ls_in_vdd1[0]','mmap_ls_in_vdd2_vdd[0]','mmap_ls_in_vdd2[0]','mmap_ls_in_vdd3_vdd[0]','mmap_ls_in_vdd3[0]','mmap_ls_in_in12_1_vdd[0]','mmap_ls_in_in12_1[0]','mmap_ls_in_in12_2_vdd[0]','mmap_ls_in_in12_2[0]','mmap_ls_in_in12_3_vdd[0]','mmap_ls_in_in12_3[0]']: 
									swcx.append(ex_fg[s].split('=')[1])
								if ex_fg[s].split('=')[0] in ['fgota0nbias ','fgota0pbias ','fgota1nbias ','fgota1pbias ','i2v_pfet_gatefgota_fgotapbias[0]','i2v_pfet_gatefgota_fgotanbias[0]','mismatch_meas_pfetg_fgotapbias[0]','mismatch_meas_pfetg_fgotanbias[0]','mismatch_meas_out_fgotapbias[0]','mismatch_meas_out_fgotanbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['c4_sp_ota_p_bias[0]','c4_sp_ota_n_bias[0]','c4_sp_ota_p_bias[1]','c4_sp_ota_n_bias[1]','TIA_ota_p_bias[0]','TIA_ota_n_bias[0]','TIA_ota_p_bias[1]','TIA_ota_n_bias[1]','hh_ota_p_bias[0]','hh_ota_n_bias[0]','hh_ota_p_bias[1]','hh_ota_n_bias[1]','i2v_pfet_gatefgota_fgotapbias[0]','i2v_pfet_gatefgota_fgotanbias[0]','mismatch_meas_pfetg_fgotapbias[0]','mismatch_meas_pfetg_fgotanbias[0]','mismatch_meas_out_fgotapbias[0]','mismatch_meas_out_fgotanbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['fgota_bias[0]','fgota_bias[1]','hh_nabias','hh_kbias','hh_vinbias','hh_voutbias','ramp_otabias[0]','c4_sp_ota_bias[0]','c4_sp_ota_bias[1]','TIA_fgota_bias[0]','TIA_fgota_bias[1]','TIA_ota_bias[0]','TIA_ota_buf_out[0]','nfet_i2v_otabias[0]','pfet_i2v_otabias[0]','i2v_pfet_gatefgota_ota0bias[0]','i2v_pfet_gatefgota_fgotabias[0]','mismatch_meas_pfetg_fgotabias[0]','mismatch_meas_out_fgotabias[0]','vmm12x1_otabias[0]']:
									swcx.append(2)
								elif swc_name1 in ['hh_leak','hh_fbpfetbias','ramp_pfetinput[0]','ramp_pfetinput[1]','vmm12x1_pfetbias[0]','DAC_bias_pfet[0]','vmm12x1_offsetbias[0]','cs_bias[0]','mismatch_meas_cal_bias[0]']:
									swcx.append(1)
								elif swc_name1 in ['ota_bias[0]','ota_bias[1]','ota_buf_bias[0]','ota_buf_bias[1]']:
									swcx.append(2)
								elif swc_name1 in ['fgota_p_bias[0]','fgota_p_bias[1]','fgota_n_bias[0]','fgota_n_bias[1]']:
									swcx.append(3)
								elif sb.name.split('[')[0] in ['c4_sp','ramp_fe'] and swc_name1[0:6]!="c4_sp_cap" and  swc_name1[0:5]!="c4_sp_fg" and n==0 and swc_name1 not in ['lpf_fg[0]'] and swc_name1[0:7] not in ['lpf_cap','ramp_fe','sigma_d','ota_sma'] :
									swcx.append(0)
								elif swc_name1 in ['mmap_ls_in_r0[0]','mmap_ls_in_r1[0]','mmap_ls_in_r2[0]','mmap_ls_in_r3[0]','mmap_ls_in_r4[0]','mmap_ls_in_r5[0]','mmap_ls_in_r6[0]','mmap_ls_in_r7[0]','mmap_ls_in_r8[0]','mmap_ls_in_r9[0]','mmap_ls_in_r10[0]','mmap_ls_in_r11[0]','mmap_ls_in_r12[0]','mmap_ls_in_r13[0]','mmap_ls_in_r14[0]','mmap_ls_in_r15[0]','mmap_ls_in_r16[0]','mmap_ls_in_r17[0]','mmap_ls_in_r18[0]','mmap_ls_in_r19[0]','mmap_ls_in_r20[0]','mmap_ls_in_r21[0]','mmap_ls_in_r22[0]','mmap_ls_in_r23[0]','mmap_ls_in_r24[0]','mmap_ls_in_r25[0]','mmap_ls_in_r26[0]','mmap_ls_in_r27[0]','mmap_ls_in_r28[0]','mmap_ls_in_r29[0]','mmap_ls_in_vdd1[0]','mmap_ls_in_vdd2[0]','mmap_ls_in_vdd3[0]','mmap_ls_in_in12_1[0]','mmap_ls_in_in12_2[0]','mmap_ls_in_in12_3[0]']:
									swcx.append(ex_fg[s].split('=')[1])
									swcx.append(11)
								elif swc_name1 in ['Hyst_diff_ota1_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['Max_detect_fgswc_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['Max_detect_ota0_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['Min_detect_fgswc_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['Min_detect_ota0_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['hhn_fgswc_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['hhn_ota0_ibias[0]','hhn_ota1_ibias[0]','hhn_fgota1_ibias[0]','hhn_fgota0_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['hhn_fgota1_pbias[0]','hhn_fgota1_nbias[0]','hhn_fgota0_pbias[0]','hhn_fgota0_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['fgswitch_fgswc_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['common_drain_fgswc_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['common_drain_nfet_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['hhn_debug_fgswc_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['hhn_debug_ota0_ibias[0]','hhn_debug_ota1_ibias[0]','hhn_debug_fgota1_ibias[0]','hhn_debug_fgota0_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['hhn_debug_fgota1_pbias[0]','hhn_debug_fgota1_nbias[0]','hhn_debug_fgota0_pbias[0]','hhn_debug_fgota0_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['wta_new_wta_bias[0]']:
									swcx.append(1)
								elif swc_name1 in ['wta_new_buf_bias[0]']:
									swcx.append(2)
								elif swc_name1 in ['common_source_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['VolDivide1_ota0_ibias[0]','VolDivide1_fgota0_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['VolDivide1_fgota0_pbias[0]','VolDivide1_fgota0_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['I_SenseAmp_ota0_ibias[0]','I_SenseAmp_fgota0_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['I_SenseAmp_fgota0_pbias[0]','I_SenseAmp_fgota0_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['nmirror_w_bias_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['SubbandArray_Maxpfet[0]']:
									swcx.append(1)
								elif swc_name1 in ['SubbandArray_Maxota[0]','SubbandArray_LPF[0]','SubbandArray_FBbias[0]','SubbandArray_FFbias[0]']:
									swcx.append(2)
								elif swc_name1 in ['SubbandArray_FBpbias[0]','SubbandArray_FBnbias[0]','SubbandArray_FFpbias[0]','SubbandArray_FFnbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['HH_RG_Nafb_ibias[0]','HH_RG_in0_ibias[0]','HH_RG_pfet_ibias[0]','HH_RG_nmr_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['HH_RG_buf_ibias[0]','HH_RG_comp_ibias[0]','HH_RG_Na_ibias[0]','HH_RG_K_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['HH_RG_Na_pbias[0]','HH_RG_Na_nbias[0]','HH_RG_K_pbias[0]','HH_RG_K_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['HH_RG_2s_Nafb_ibias[0]','HH_RG_2s_syn0_ibias[0]','HH_RG_2s_syn1_ibias[0]','HH_RG_2s_pfet_ibias[0]','HH_RG_2s_nmr_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['HH_RG_2s_buf_ibias[0]','HH_RG_2s_comp_ibias[0]','HH_RG_2s_Na_ibias[0]','HH_RG_2s_K_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['HH_RG_2s_Na_pbias[0]','HH_RG_2s_Na_nbias[0]','HH_RG_2s_K_pbias[0]','HH_RG_2s_K_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['HH_RG_3s_Nafb_ibias[0]','HH_RG_3s_syn0_ibias[0]','HH_RG_3s_syn1_ibias[0]','HH_RG_3s_syn2_ibias[0]','HH_RG_3s_pfet_ibias[0]','HH_RG_3s_nmr_ibias[0]']:
									swcx.append(1)
								elif swc_name1 in ['HH_RG_3s_buf_ibias[0]','HH_RG_3s_comp_ibias[0]','HH_RG_3s_Na_ibias[0]','HH_RG_3s_K_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['HH_RG_3s_Na_pbias[0]','HH_RG_3s_Na_nbias[0]','HH_RG_3s_K_pbias[0]','HH_RG_3s_K_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['SOSLPF_Feedback[0]','SOSLPF_Buffer[0]','SOSLPF_Ibias2[0]','SOSLPF_Ibias1[0]']:
									swcx.append(2)
								elif swc_name1 in ['SOSLPF_FG2p[0]','SOSLPF_FG2n[0]','SOSLPF_FG1p[0]','SOSLPF_FG1n[0]']:
									swcx.append(3)
								elif swc_name1 in ['MSOS02_Feedback[0]','MSOS02_Buffer[0]','MSOS02_Ibias2[0]','MSOS02_Ibias1[0]']:
									swcx.append(2)
								elif swc_name1 in ['MSOS02_Wbp[0]','MSOS02_Wbn[0]','MSOS02_Wap[0]','MSOS02_Wan[0]']:
									swcx.append(3)
								elif swc_name1 in ['vmm_offc_off1_ibias[0]','vmm_offc_off2_ibias[0]','vmm_offc_w16n[0]','vmm_offc_w26n[0]','vmm_offc_w16p[0]','vmm_offc_w26p[0]','vmm_offc_w15n[0]','vmm_offc_w25n[0]','vmm_offc_w15p[0]','vmm_offc_w25p[0]','vmm_offc_w14n[0]','vmm_offc_w24n[0]','vmm_offc_w14p[0]','vmm_offc_w24p[0]','vmm_offc_w13n[0]','vmm_offc_w23n[0]','vmm_offc_w13p[0]','vmm_offc_w23p[0]','vmm_offc_w12n[0]','vmm_offc_w22n[0]','vmm_offc_w12p[0]','vmm_offc_w22p[0]','vmm_offc_w11n[0]','vmm_offc_w21n[0]','vmm_offc_w11p[0]','vmm_offc_w21p[0]']:
									swcx.append(1)
								elif swc_name1 in ['vmm_offc_o1_ibias[0]','vmm_offc_o1_ibias[0]','vmm_offc_o2_fgibias[0]','vmm_offc_o1_fgibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['vmm_offc_o2_pbias[0]','vmm_offc_o2_pbias[0]','vmm_offc_o1_pbias[0]','vmm_offc_o1_nbias[0]']:
									swcx.append(3)
								elif swc_name1 in ['C4_BPF_Buffer_ibias[0]','C4_BPF_Feedback_ibias[0]','C4_BPF_Forward_ibias[0]']:
									swcx.append(2)
								elif swc_name1 in ['C4_BPF_Feedback_pbias[0]','C4_BPF_Feedback_nbias[0]','C4_BPF_Forward_pbias[0]','C4_BPF_Forward_nbias[0]']:
									swcx.append(3)
								self.swcs.append(swcx)
								if isinstance(swc2[0],int): break

class cab2(complexBlock):
	def __init__(self, name):
		self.name = name
		self.type = 'CAB2'
		self.stats = cab2Stats()     
		self.array_stats = arrayStats()
		self.subblocks = []

		#CAB ports
		self.inputs = ['open']*self.stats.num_inputs
		self.outputs = ['open']*self.stats.num_outputs

		#CAB Devices
		dev_types = self.stats.dev_types
		dev_pins = self.stats.dev_pins    
		self.addSubs(dev_types, dev_pins)

	def genLI(self, *var):
		self.swcs = []
		verbose = 1
		if len(var) == 1: verbose = 1
		# inputs to local interconnect--
		# inputs to CAB + outputs from DEVs
		self.li_in_in = ['gnd','vcc']+self.inputs
		self.li_in_dev = []
		for i in range(len(self.subblocks)):
			if isinstance(self.getSub(i).outputs,str):
				self.getSub(i).outputs= self.getSub(i).outputs.split()
			for j in range(len(self.getSub(i).outputs)):
				self.li_in_dev.append(self.getSub(i).outputs[j])
		self.li_in_dev.reverse()
		self.li_in = self.li_in_in + self.li_in_dev

		# outputs from local interconnect--
		# inputs to DEVs + outputs from CAB
		self.li_out_out = self.outputs
		self.li_out_dev = []
		for i in range(len(self.subblocks)):
			for j in range(len(self.getSub(i).inputs)):
				self.li_out_dev.append(self.getSub(i).inputs[j])      
		self.li_out = self.li_out_dev+self.li_out_out 
		self.li = [[0]*len(self.li_in) for x in self.li_out]
		#printing connectivity matrix and filling the local interconnect matrix
		x = 2
		for i in range(len(self.li_in)):
			if verbose: print ('%s'%str(i).ljust(2),)
		if verbose: print ("Hallelujah!")
		for i in range(len(self.li_in)):
			if self.li_in[i] != 'open':
				if verbose: print ('%s'%self.li_in[i].ljust(x),)
			else:
				if verbose: print (''.ljust(x),)
		if verbose: print ()
		for i in range(len(self.li_out_dev)):
			if self.li_out[i] != 'open':
				for j in range(len(self.li_in)):
					if self.li_out[i] == self.li_in[j]:
						if verbose: print (str('X').ljust(x),)
						self.li[i][j] = 1
					else:
						if verbose: print (str('.').ljust(x),)
				if verbose: 
					print (self.li_out[i].ljust(2),) 
					print (str(i).ljust(2))
			else:
				for j in range(len(self.li_in)):
					if verbose: print (str('.').ljust(x),)
				if verbose: print ('%s%s'%(''.ljust(3), str(i).ljust(2)))
		for i in range(len(self.li_out_out)):
			for j in range(len(self.li_in_in)):
				if verbose: print (''.ljust(x),)
			for j in range(len(self.li_in_dev)):
				if self.li_out_out[i] == self.li_in_dev[j] and self.li_out_out[i] != 'open':
					if verbose: print ('X'.ljust(x),)
					self.li[i+len(self.li_out_dev)][j+len(self.li_in_in)] = 1
				else:
					if verbose: print ('.'.ljust(x),)
			if self.li_out_out[i] == 'open':
				if verbose: print (self.li_out_out[i])
			else:
				if verbose: print (self.li_out_out[i])

		#actually generating the switches addresses here  
		self.swcsFromLi()    

	def dispLI(self):
		self.genLI('verbose')

	def genDevFgs(self):
		print ("getting here!")
		verbose = 0
		for i in range(len(self.subblocks)):
			sb = self.getSub(i)
			if sb.outputs != 'open':
				swc_name0 = sb.name
				if sb.ex_fgs:
					ex_fg=sb.ex_fgs.split("&")
					for s in range(len(ex_fg)):
						print ("ok here too22")
						for j in ex_fg[s].split()[::2]:
							swc_name1 = j+'['+sb.name.split('[')[1]
							swc0 = self.stats.dev_fgs[swc_name0]
							swc2 = self.stats.dev_fgs[swc_name1]
							for n in range(len(swc2)):
								if isinstance(swc2[0],int):
									swc1=swc2
								else:
									swc1=swc2[n]
								swc = [swc0[0]+swc1[0], swc0[1]+swc1[1]]
								swcx = self.array_stats.getTileOffset(swc, self.grid_loc)
								if verbose: print ('%s %s -> (%g %g) -> (%g %g)'%(swc_name0, swc_name1, swc[0], swc[1], swcx[0], swcx[1]))
								if n==0: ##double check
									swcx.append(ex_fg[s].split('=')[1])
								else:
									swcx.append(0)
								if sb.name.split('[')[0] == 'meas_volt_mite' and n==0:
									swcx.append(4)
								if swc_name1 in ['meas_fg[0]','current_ref_bias1[0]','current_ref_bias2[0]'] and n==0:
									swcx.append(4)
								if sb.name.split('[')[0] == 'mite' and n==0:
									swcx.append(4)
								elif sb.name.split('[')[0] == 'signalmult' and n==0:
									swcx.append(1)
								elif sb.name.split('[')[0] == 'ota2_bias' and n==0:
									swcx.append(2)					    
								else:
									swcx.append(0)
								self.swcs.append(swcx)
								if isinstance(swc2[0],int):
									n=2

class ioblock(complexBlock):
	def __init__(self, name):
		self.name = name
		self.type = 'ioblock'
		self.inputs = ['open']*12
		self.outputs= ['open']*6
		self.portorder = [0,3,6,9,12,15,1,2,4,5,7,8,10,11,13,14,16,17] ## $$
		self.num=[]
		self.swcs = []
		self.stats = iosdStats()    #$$ 
		self.array_stats = arrayStats()
		self.subblocks = []
		for i in range(6):
			self.addSub(pblock('empty', 'ioslice'))

	def genLI(self):
		#global groutes
		port_sd = ['I3','I7','I11','I15','O3','O7'] #$$
		port_sa = ['I8','I9','I13','I14','I15','O4']
		port_nd = ['I1','I5','I9','I13','O1','O5']
		port_na = ['I10','I11','I12','O5','O6','O7']
		port_east = ['I4','I5','I6','I7','O2','O3']
		verbose = 1
		for i in range(len(self.subblocks)):
			csub = self.getSub(i)
			if csub.outputs != 'open':
				if(csub.grid_loc[0] in [2,4,6]):
					if(csub.grid_loc[1] in [0]):
						self.stats=iosdStats()	
						swc_name0 = port_sd[csub.number]
						swc_name1 = csub.type
					else:
						self.stats=iondStats()	
						swc_name0 = port_nd[csub.number]
						swc_name1 = csub.type
				elif(csub.grid_loc[0] == 8):
					self.stats=ioeStats()
					swc_name0 = port_east[csub.number]
					swc_name1 = csub.type
				elif(csub.grid_loc[0] in [1,3,5,7]):
					if(csub.grid_loc[1] in [0]):
						self.stats=iosaStats()		
						swc_name0 = port_sa[csub.number]
						swc_name1 = csub.type
						swc_name1 = swc_name1.strip() # strips leading and ending spaces
					else:
						self.stats=ionaStats()		
						swc_name0 = port_na[csub.number]
						swc_name1 = csub.type
						swc_name1 = swc_name1.strip()
				elif(csub.grid_loc[0] == 0):       #Michelle
					print ('Using a DAC')
					self.stats=ioeStats()
					swc_name0 = port_east[csub.number]
					swc_name1 = csub.type
				else:
					print ('IO block does not exist!')
				if (swc_name1 == 'int[0]' or swc_name1 == '') :
					pdb.set_trace()
				if (swc_name1[1:-3] != 'int'and csub.name != 'gnd' and csub.name != 'vcc' and csub.name != 'out:gnd') :    #we'll pick these up in the devFG generation          
					print (csub)
					swc_name1=swc_name1[1:]
					swc0 = self.stats.li[swc_name0] #get input name
					swc1 = self.stats.li[swc_name1] #get input type
					swc = [swc0[0]+swc1[0],swc0[1]+swc1[1]]
					swcx = self.array_stats.getTileOffset(swc, self.grid_loc)
					if verbose: print ('%s %s -> (%g %g) -> (%g %g)'%(swc_name0, swc_name1, swc[0], swc[1], swcx[0], swcx[1]))
					self.swcs.append(swcx)

	###gendevFgs --IO BLOCK $$
	def genDevFgs(self):
		print ("I/O Blocks dev FGs")
		for i in range(len(self.subblocks)):
			csub = self.getSub(i)
			if csub.outputs != 'open' and csub.type[1:-3] in ['int','tgate','ana_buff_out','ana_buff_in','dig_buff_out','dig_buff_in'] : #?? dunno why was a condition
				if(csub.grid_loc[0] in [2,4,6]):
					if(csub.grid_loc[1] in [0]):
						self.stats=iosdStats()
					else:
						self.stats=iondStats()
				elif(csub.grid_loc[0] in [8]): # IO_E case
					self.stats=ioeStats()
				elif(csub.grid_loc[0] in [0]): # IO_W case
					self.stats=iowStats()
				elif(csub.grid_loc[0] in [1,3,5,7]):
					if(csub.grid_loc[1] in [0]):
						self.stats=iosaStats()
					else:
						self.stats=ionaStats()	
				else:
					print ('I/O block does not exist!!!')  
				if csub.grid_loc[0] in [0]:
					print ('NO FGSSSSSS!')
					continue
				else:
					dev_type = csub.type[1:]		
					nswcs = self.stats.dev_fgs[dev_type]
					for i in range(len(nswcs)):
						swc = [nswcs[i][0],nswcs[i][1]]
						print ('!!!!!!!!!!!!!!%s --> '%(dev_type),)
						swcx = self.array_stats.getTileOffset(swc, self.grid_loc)
						print ('DEV FGs  -> (%g %g) -> (%g %g)'%(swc[0], swc[1], swcx[0], swcx[1]))
						if csub.type[1:-3] in ['ana_buff_out','ana_buff_in'] and i==1:
							swcx.append('0.000002')
							swcx.append(2)
						self.swcs.append(swcx)
