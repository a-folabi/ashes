#***********************************
#SCRIPT TO READ FROM PYTHON MODEL FILE
#***********************************

import sys
import os



board_num = int(sys.argv[1]);
if (not sys.argv[2].isnumeric()): print('Please enter the FPAA board number that you are using.', "No FPAA Board Number Entered", "error"); sys.exit();
chip_num = int(sys.argv[2]);
file_name = sys.argv[3]
print(board_num)


vpr_path='/home/ubuntu/rasp30/vtr_release/vtr_flow/'

#del blk, blk_objs, jlist, cat_num, loctmp, loctmp2;
#global file_name jlist cat_num board_num addvmm plcvpr pass_num chip_num cap_info show_dsgnmatrics;
#global sft_chk ramp_chk;

print("Compiling...");


if(board_num == 2): 
	arch = 'rasp3'; 
	brdtype = ''; 
	loc_num=1;
elif(board_num == 3): 
	arch = 'rasp3a'; 
	brdtype = ' -'+arch; 
	loc_num=2;
elif(board_num == 4): 
	arch = 'rasp3n'; 
	brdtype = ' -'+arch; 
	loc_num=3;
elif(board_num == 5): 
	arch = 'rasp3h'; 
	brdtype = ' -'+arch; 
	loc_num=4;
else: 
	print("1111");
	print('Please select the FPAA board that you are using.', "No Selected FPAA Board", "error"); 
	sys.exit();

if chip_num == []: print('Please enter the FPAA board number that you are using.', "No FPAA Board Number Entered", "error"); sys.exit();
path=os.path.split(file_name)[0]; #get filename, path and extension
fname=os.path.basename(os.path.splitext(file_name)[0]);
extension = os.path.splitext(file_name)[1];
#print(path)
#print(fname)
#print(extension)

try:
	os.chdir(path); os.remove(fname+'.blif'); os.remove(fname+'.blk'); os.remove('info.txt');
except:
	print("found no files to remove") #do nothing
	
hid_dir=path+'.'+fname;
os.system('mkdir -p '+hid_dir);

try:
	os.remove(fname + '.pads'); 
except:
	print("found no files to remove") #do nothing

#global dac_array dac_array_map gpin_array gpin_array_map number_samples period b_elements;
#b_elements = tlist(['b_element','b_ota', 'b_fgota', 'b_nfet', 'b_pfet', 'b_cap', 'b_tgate', 'b_nmirror', 'b_ble','b_ibias'],0,0,0,0,0,0,0,0,0)
dac_array = [0]; dac_array_map = ""; gpin_array = [0]; gpin_array_map = ""; number_samples = 0; period = "0x03e8";
blname = "";
numofip=0; numofop=0; numofblk=0; numoflink=0;
inps=0; accblk=1;
#blk_name=[,]; link_blk=cell([1,1]); spl_blk=cell([1,1]); cat_num =cell([1,1]); junc_unq = cell([1,1]);
#arb_gen = cell([1,1]); gpin = cell([1,1]); ga_idx = cell(); gpin_idx = cell();
j=1; net=1;
objnum=1; ip_count=1; op_count=1;
prime_ips=[]; prime_ops=[]; blk_objs=[];
vmm_ct=0; split = "%f"; spl_src = [];
ga_blk_num= 0; gpin_blk_num= 0; genarb_dac=[]; genarb_gpin=[]; dc_dac=[];
fix_gnd=0; fix_vdd=0; ramp_adc=0; mite_adc=0;
#global RAMP_ADC_check sftreg_check Signal_DAC_check GPIO_IN_check MITE_ADC_check plcloc ladder_count ONchip_ADC Onchip_ADC_num Counter_class mite_count lpf_ota_count mite_adc_number;
RAMP_ADC_check=0; sftreg_check=0; Signal_DAC_check=0; GPIO_IN_check=0; MITE_ADC_check=0; ladder_count=0; ONchip_ADC =0; sftreg_count=0;Onchip_ADC_num =[0,[0,0]];Counter_class=0;mite_count=0;lpf_ota_count=0;mite_adc_number=0;
add_clk=[]; dig_blk=0; netout=[]; addvmm = "%f"; plcvpr = "%f";
plcloc = [];
nfetloc = 1; pfetloc = 1;
chgnet = [0,0,0,0,0,0]; #gnd_i gnd gnd_dig vdd vdd_o vdd_dig
chgnet_dict= []; chgnet_tf= "%f"; makeblk = "%f"; spl_fix = []; spl_fix_chg= "%f"; blk_in=[]; blk_out=[];
internal_number = 1; add_tgates4logic = 0; number_tgates = 0;
dac_loc_idx=0; dac_buf_loc_idx=0; gpin_loc_idx=0; adc_loc_idx=0; adc_ip_idx1=1; adc_ip_idx2=1; adc_ip_net=[1,2];
dac_loc= []; dac_buf_loc= []; gpin_loc= []; adc_locin= []; adc_loc= []; iopad_loc= [];


os.system("/home/ubuntu/scilab-5.5.2/bin/scilab -f /home/ubuntu/rasp30/sci2blif/io_info/io_info_rasp30.sce -nwni");
os.system("/home/ubuntu/scilab-5.5.2/bin/scilab -f /home/ubuntu/rasp30/sci2blif/io_info/io_info_rasp30a.sce -nwni");


os.system('python3 /home/ubuntu/ashes/ashes_fg/fpaa/new_converter.py '+path+fname+'.py /')
os.system('python3 /home/ubuntu/ashes/ashes_fg/fpaa/verilog2blif.py '+path+fname+'.v '+path)



#os.system('~/rasp30/sci2blif/retool.sce');


#if chgnet_tf == %t then retool(chgnet_dict,path,fname,ext); end
#if spl_fix_chg == %t then retool(spl_fix,path,fname,ext); retool(spl_fix,path,fname,'.pads '); end


#unix_s('python3 /home/ubuntu/rasp30/sci2blif/verilog2blif.py '+path+fname+'.v '+path)


os.system("/home/rasp30/prog_assembly/libs/scilab_code/make_input_vector_file.sce");
make_input_vector_file();


if (arch == 'rasp3a'): os.system('python3 /home/ubuntu/rasp30/sci2blif/gen_pads_30a.py '+path+fname+' '+path);
if (arch == 'rasp3'): os.system('python3 /home/ubuntu/rasp30/sci2blif/gen_pads_30.py '+path+fname+' '+path);



if(makeblk):
    os.system('~/rasp30/sci2blif/blif4blk.sce');
    mkblk(fd_w,blk,blk_objs);
    print('Done!');
else:
    if plcvpr:
        if (addvmm): os.system('/home/ubuntu/rasp30/vtr_release/vpr/vpr /home/ubuntu/rasp30/vpr2swcs/./arch/'+arch+'_arch.xml ' + path + fname + '  -route_chan_width 17 -timing_analysis off -fix_pins ' + path + fname + '.pads -nodisp');
        else: os.system('/home/ubuntu/rasp30/vtr_release/vpr/vpr /home/ubuntu/rasp30/vpr2swcs/./arch/'+arch+'_arch.xml ' + path + fname + '  -route_chan_width 17 -timing_analysis off -fix_pins ' + path + fname + '.pads -nodisp');
    

        plcfile=mopen(path + fname + '.place','r'); tmpplc=mgetl(plcfile); mclose(plcfile);

        for plcidx in range(6, size(tmpplc,'r')): 
            if (len(tmpplc[plcidx].split("\s\s")) == 1):
                loctmp[plcidx-5,:]=tmpplc[plcidx].split("\s") #has net names
                loctmp2[plcidx-5] = loctmp[plcidx-5,2:4] + ' '
            else:
                loctmp[plcidx-5,:]=tmpplc[plcidx].split("\s\s") #has net names
                tmploc =loctmp[plcidx-5,2].split('\t')
                tmploc = tmploc + ' ';
                tmploc = strsubst(tmploc,"/#.*/",'','r');
                loctmp2[plcidx-5] = stripblanks(tmploc)

   

        loc_matrix=[loctmp[:,1], loctmp2]; #disp(loc_matrix)
        l_loc_matrix=size(loc_matrix,"r");
        l_plcloc=size(plcloc,"r");
        for i_plcloc in range (1,l_plcloc):
            for i_loc_matrix in range(1,l_loc_matrix):
                if loc_matrix((i_loc_matrix,1) == plcloc(i_plcloc,1)):
                    for j_loc_matrix in range(1,l_loc_matrix):
                        if (loc_matrix[j_loc_matrix,2] == plcloc[i_plcloc,2]):
                            loc_matrix[j_loc_matrix,2] = loc_matrix[i_loc_matrix,2];
                    loc_matrix[i_loc_matrix,2] = plcloc[i_plcloc,2];
        loc_matrix[:,3]=loc_matrix[:,1] +" " +loc_matrix[:,2];
        plcfile=mopen(path + fname + '.place','wt'); mputl(tmpplc[1:5],plcfile); mclose(plcfile);
        plcfile=mopen(path + fname + '.place','a'); mputl(loc_matrix[:,3],plcfile); mclose(plcfile);

        # generate switches
        os.system('python /home/ubuntu/rasp30/vpr2swcs/genswcs.py -c ' + path + fname + ' -d '+ path + ' -route' + brdtype);
    else:
        os.system('python /home/ubuntu/rasp30/vpr2swcs/genswcs.py -c ' + path + fname + ' -d '+ path + brdtype);

    os.system('mv ' + fname + '.pads ' + fname + '.place ' + fname + '.net ' + fname + '.route ' +hid_dir);
    
    if (show_dsgnmatrics == 1): cap_info = caps4sim(cap_info);

    os.system('mv ' + fname + '.caps ' +hid_dir);
    if (show_dsgnmatrics == 1 & pass_num == 2): os.system("~/rasp30/prog_assembly/libs/scilab_code/MakeProgramlilst_CompileAssembly.sce",-1);
    if (show_dsgnmatrics == 0): os.system("~/rasp30/prog_assembly/libs/scilab_code/MakeProgramlilst_CompileAssembly.sce",-1); end
    
    print("Compilation Completed from new flow. Ready to Program.");
end
if (show_dsgnmatrics == 1): cap_infos = cap_info;

