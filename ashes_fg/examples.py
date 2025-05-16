import ashes_fg as fg

def c4_offchip():
    inpad1 = fg.inpad([5])
    input_voltage = fg.dc_in(1.9, fix_loc = [1,5,5])
    c4_out = fg.C4_BPF([input_voltage, inpad1], C4_BPF_Feedback_ibias =3.5e-10, C4_BPF_Forward_ibias = 7.5e-10, fix_loc=[1,5,6])
    outpada = fg.outpada(c4_out, [6])
    
def ors_buffer():
    inpad1 = fg.inpad([5])
    buff_out = fg.ota_buf(inpad1, fix_loc = [1,11,6])
    outpad = fg.outpad(buff_out, [6])
    
def drain_follower_nfet():
    inpad1 = fg.inpad([5])
    src_fol_out = fg.common_drain_nfet(inpad1, common_drain_nfet_ibias='5e-6')
    buf = fg.ota_buf(src_fol_out)
    outpad = fg.outpad(buf, [6])

def drain_follower_pfet():
    inpad1 = fg.inpad([5])
    src_fol_out = fg.common_drain(inpad1, common_drain_fgswc_ibias='5e-9')
    buf = fg.ota_buf(src_fol_out)
    outpad = fg.outpad(buf, [6])
	
def cs_amp():
	inpad1 = fg.inpad([5])
	src_amp = fg.common_source(inpad1, common_source_ibias='5e-07', fix_loc = [1,1,5])
	buf_out = fg.ota_buf(src_amp, fix_loc = [1,3,5])
	outpad = fg.outpad(buf_out, [6])	
