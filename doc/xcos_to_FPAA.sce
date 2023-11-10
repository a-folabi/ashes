//***********************************
//SCRIPT TO READ FROM XCOS MODEL FILE
//***********************************
vpr_path='/home/ubuntu/rasp30/vtr_release/vtr_flow/'

clear blk blk_objs jlist cat_num loctmp loctmp2;
global file_name jlist cat_num board_num addvmm plcvpr pass_num chip_num cap_info show_dsgnmatrics;
global sft_chk ramp_chk;

disp("Compiling...");

select board_num 
case 2 then arch = 'rasp3'; brdtype = ''; loc_num=1;
case 3 then arch = 'rasp3a'; brdtype = ' -'+arch; loc_num=2;
case 4 then arch = 'rasp3n'; brdtype = ' -'+arch; loc_num=3;
case 5 arch = 'rasp3h'; brdtype = ' -'+arch; loc_num=4;
else disp("1111");messagebox('Please select the FPAA board that you are using.', "No Selected FPAA Board", "error"); abort; end

if chip_num == [] then messagebox('Please enter the FPAA board number that you are using.', "No FPAA Board Number Entered", "error"); abort; end
[path,fname,extension]=fileparts(file_name); //get filename, path and extension
cd(path); deletefile(fname+'.blif'); deletefile(fname+'.blk'); deletefile('info.txt');
hid_dir=path+'.'+fname;
unix_s('mkdir -p '+hid_dir);
deletefile(fname + '.pads');

global dac_array dac_array_map gpin_array gpin_array_map number_samples period b_elements;
b_elements = tlist(['b_element','b_ota', 'b_fgota', 'b_nfet', 'b_pfet', 'b_cap', 'b_tgate', 'b_nmirror', 'b_ble','b_ibias'],0,0,0,0,0,0,0,0,0)
dac_array = [0]; dac_array_map = ""; gpin_array = [0]; gpin_array_map = ""; number_samples = 0; period = "0x03e8";
blname = "";
numofip=0; numofop=0; numofblk=0; numoflink=0;
inps=0; accblk=1;
blk_name=cell([1,1]); link_blk=cell([1,1]); spl_blk=cell([1 1]); cat_num =cell([1 1]); junc_unq = cell([1 1]);
arb_gen = cell([1 1]); gpin = cell([1 1]); ga_idx = cell(); gpin_idx = cell();
no=length(scs_m.objs); link_name=zeros(1,no); numipsofblk=zeros(no,2);
j=1; net=1;
objnum=1; ip_count=1; op_count=1;
prime_ips=[]; prime_ops=[]; blk_objs=[];
vmm_ct=0; split = %f; spl_src = [];
ga_blk_num= 0; gpin_blk_num= 0; genarb_dac=[]; genarb_gpin=[]; dc_dac=[];
fix_gnd=0; fix_vdd=0; ramp_adc=0; mite_adc=0;

global RAMP_ADC_check sftreg_check Signal_DAC_check GPIO_IN_check MITE_ADC_check plcloc ladder_count ONchip_ADC Onchip_ADC_num Counter_class mite_count lpf_ota_count mite_adc_number;
RAMP_ADC_check=0; sftreg_check=0; Signal_DAC_check=0; GPIO_IN_check=0; MITE_ADC_check=0; ladder_count=0; ONchip_ADC =0; sftreg_count=0;Onchip_ADC_num(1,1:2) =0;Counter_class=0;mite_count=0;lpf_ota_count=0;mite_adc_number=0;
add_clk=[]; dig_blk=0; netout=[]; addvmm = %f; plcvpr = 1;
plcloc = [];
nfetloc = 1; pfetloc = 1;
chgnet = [0,0,0,0,0,0]; //gnd_i gnd gnd_dig vdd vdd_o vdd_dig
chgnet_dict= []; chgnet_tf= %f; makeblk = %f; spl_fix = []; spl_fix_chg= %f; blk_in=[]; blk_out=[];
internal_number = 1; add_tgates4logic = 0; number_tgates = 0;
dac_loc_idx=0; dac_buf_loc_idx=0; gpin_loc_idx=0; adc_loc_idx=0; adc_ip_idx1=1; adc_ip_idx2=1; adc_ip_net=[1 2];

dac_loc= cell(); dac_buf_loc= cell(); gpin_loc= cell(); adc_locin= cell(); adc_loc= cell(); iopad_loc= cell();
exec("/home/ubuntu/rasp30/sci2blif/io_info/io_info_rasp30.sce",-1);
exec("/home/ubuntu/rasp30/sci2blif/io_info/io_info_rasp30a.sce",-1);


unix_s('python3.6 /home/ubuntu/rasp30/sci2blif/xcos2verilog.py '+path+fname+'.xcos '+path)
unix_s('python3.6 /home/ubuntu/rasp30/sci2blif/verilog2blif.py '+path+fname+'.v '+path)



//exec('~/rasp30/sci2blif/retool.sce',-1);


//if chgnet_tf == %t then retool(chgnet_dict,path,fname,ext); end
//if spl_fix_chg == %t then retool(spl_fix,path,fname,ext); retool(spl_fix,path,fname,'.pads '); end


//unix_s('python3 /home/ubuntu/rasp30/sci2blif/verilog2blif.py '+path+fname+'.v '+path)


exec("~/rasp30/prog_assembly/libs/scilab_code/make_input_vector_file.sce",-1);
make_input_vector_file();


if arch == 'rasp3a' then unix_s('python3.6 /home/ubuntu/rasp30/sci2blif/gen_pads_30a.py '+path+fname+' '+path);end
if arch == 'rasp3' then unix_s('python3.6 /home/ubuntu/rasp30/sci2blif/gen_pads_30.py '+path+fname+' '+path);end


//////////////////////////////////replace .pads file, for testing 2/18/2023
//unix_s('rm '+fname+'.pads')
//fd_io= mopen (fname+'.pads','a+'); mputl('gnd 7 0 4 #int[4]',fd_io); mclose(fd_io);
//fd_io= mopen (fname+'.pads','a+'); mputl('net1_1 8 1 5 #tgate[1]',fd_io); mclose(fd_io);
//fd_io= mopen (fname+'.pads','a+'); mputl('net2_1 8 2 5 #tgate[1]',fd_io); mclose(fd_io);
//fd_io= mopen (fname+'.pads','a+'); mputl('out:net11_1 8 9 5 #tgate[1]',fd_io); mclose(fd_io);
//fd_io= mopen (fname+'.pads','a+'); mputl('out:net11_2 8 10 5 #tgate[1]',fd_io); mclose(fd_io);
//fd_io= mopen (fname+'.pads','a+'); mputl('out:net11_3 8 11 5 #tgate[1]',fd_io); mclose(fd_io);
//fd_io= mopen (fname+'.pads','a+'); mputl('out:net11_4 8 12 5 #tgate[1]',fd_io); mclose(fd_io);




if(makeblk) then 
    exec('~/rasp30/sci2blif/blif4blk.sce',-1);
    mkblk(fd_w,blk,blk_objs);
    disp('Done!');
else
    if plcvpr then
        if addvmm then unix_s('/home/ubuntu/rasp30/vtr_release/vpr/vpr /home/ubuntu/rasp30/vpr2swcs/./arch/'+arch+'_arch.xml ' + path + fname + '  -route_chan_width 17 -timing_analysis off -fix_pins ' + path + fname + '.pads -nodisp');
        else unix_s('/home/ubuntu/rasp30/vtr_release/vpr/vpr /home/ubuntu/rasp30/vpr2swcs/./arch/'+arch+'_arch.xml ' + path + fname + '  -route_chan_width 17 -timing_analysis off -fix_pins ' + path + fname + '.pads -nodisp');
        end
        plcfile=mopen(path + fname + '.place','r'); tmpplc=mgetl(plcfile); mclose(plcfile);
        for plcidx=6:size(tmpplc,'r') 
            if size(strsplit(tmpplc(plcidx),"/\s\s/")','c') == 1 then
                loctmp(plcidx-5,:)=strsplit(tmpplc(plcidx),"/\s/")'; //has net names
                loctmp2(plcidx-5) = strcat(loctmp(plcidx-5,2:4), ' ');
            else
                loctmp(plcidx-5,:)=[strsplit(tmpplc(plcidx),"/\s\s/")' ' ' ' ' ' ']; //has net names
                tmploc =strsplit(loctmp(plcidx-5,2), '/\t/');
                tmploc = strcat(tmploc, ' ');
                tmploc = strsubst(tmploc,"/#.*/",'','r');
                loctmp2(plcidx-5) = stripblanks(tmploc)
            end
        end

        loc_matrix=[loctmp(:,1) loctmp2]; //disp(loc_matrix)
        l_loc_matrix=size(loc_matrix,"r");
        l_plcloc=size(plcloc,"r");
        for i_plcloc=1:l_plcloc
            for i_loc_matrix=1:l_loc_matrix
                if loc_matrix(i_loc_matrix,1) == plcloc(i_plcloc,1) then
                    for j_loc_matrix=1:l_loc_matrix
                        if loc_matrix(j_loc_matrix,2) == plcloc(i_plcloc,2) then
                            loc_matrix(j_loc_matrix,2) = loc_matrix(i_loc_matrix,2);
                        end
                    end
                    loc_matrix(i_loc_matrix,2) = plcloc(i_plcloc,2);
                end
            end
        end
        loc_matrix(:,3)=loc_matrix(:,1)+" "+loc_matrix(:,2);
        plcfile=mopen(path + fname + '.place','wt'); mputl(tmpplc(1:5),plcfile); mclose(plcfile);
        plcfile=mopen(path + fname + '.place','a'); mputl(loc_matrix(:,3),plcfile); mclose(plcfile);

        // generate switches
        unix_s('python /home/ubuntu/rasp30/vpr2swcs/genswcs.py -c ' + path + fname + ' -d '+ path + ' -route' + brdtype);
    else
        unix_s('python /home/ubuntu/rasp30/vpr2swcs/genswcs.py -c ' + path + fname + ' -d '+ path + brdtype);
    end
    unix_s('mv ' + fname' + '.pads ' + fname + '.place ' + fname + '.net ' + fname + '.route ' +hid_dir);
    
    if show_dsgnmatrics == 1 then cap_info = caps4sim(cap_info); end

    unix_s('mv ' + fname' + '.caps ' +hid_dir);
    if show_dsgnmatrics == 1 & pass_num == 2 then exec("~/rasp30/prog_assembly/libs/scilab_code/MakeProgramlilst_CompileAssembly.sce",-1); end
    if show_dsgnmatrics == 0 then exec("~/rasp30/prog_assembly/libs/scilab_code/MakeProgramlilst_CompileAssembly.sce",-1); end
    
    disp("Compilation Completed from new flow. Ready to Program.");
end
if show_dsgnmatrics == 1 then cap_infos = cap_info; end

