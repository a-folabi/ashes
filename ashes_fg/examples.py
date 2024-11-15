import ashes_fg.class_lib_ext as fg

def hhn_ex_one():
    V_in = fg.inpad(1)
    V_na = fg.inpad(2)
    V_k = fg.inpad(3)
    V_ref = fg.inpad(4)
    hhn_input = [V_in, V_na, V_k, V_ref]
    # Only 2 of all values changed
    hhn_out = fg.hhn(hhn_input,
                     type='FPAA',
                     hhn_fgota1_ibias=2e-6,
                     hhn_fgota1_nbias=3e-7)
    pad_5 = fg.outpad(hhn_out, 5)
    return pad_5


def min_detect():
    input_voltage = fg.dc_in(DC_value=1.3)
    ota_out = fg.ota_buf(input_voltage)
    min_det_out = fg.Min_detect(ota_out,
                                Min_detect_fgswc_ibias=5e-9,
                                Min_detect_ota0_ibias=1e-6)
    pad_out = fg.outpad(min_det_out, 11)
    return pad_out


def hhn_chain():
    V_in = fg.inpad(1)
    V_na = fg.inpad(2)
    V_k = fg.inpad(3)
    V_ref = fg.inpad(4)
    neuron1_in = [V_in, V_na, V_k, V_ref]
    neuron1_out = fg.hhn(neuron1_in,
                         type='FPAA',
                         hhn_fgota1_ibias=2e-6,
                         hhn_fgota1_nbias=3e-7)
    neuron2_in = [neuron1_out, V_na, V_k, V_ref]
    neuron2_out = fg.hhn(neuron2_in, type='FPAA', hhn_ota0_ibias=2e-10)
    neuron3_in = [neuron2_out, V_na, V_k, V_ref]
    neuron3_out = fg.hhn(neuron3_in)
    pad_out = fg.outpad(neuron3_out, 7)
    return pad_out


def shift_reg():
    dc_in = fg.dc_in(1.3)
    inpad_1 = fg.inpad(1)
    inpad_2 = fg.inpad(2)
    inpad_3 = fg.inpad(3)
    input_array = [dc_in, inpad_1, inpad_2, inpad_3]
    [out1, out2, out3] = fg.sr_1i_16o(input_array)()
    outpad1 = fg.outpad(out1, 4)
    outpad2 = fg.outpad(out2, 5)
    outpad3 = fg.outpad(out3, 6)
    return [outpad1, outpad2, outpad3]


def vec_alice():
    inpad1 = fg.inpad([1])
    inpad2 = fg.inpad([2])
    c4_out = fg.c4_sp([inpad1, inpad2], num_instances=4)
    min_det_out = fg.Min_detect(c4_out, num_instances=4)
    gnd = fg.gnd()
    [delay_stg1, delay_stg2] = fg.delay_block([min_det_out, gnd], num_instances=4)()
    [delay_stg3, _] = fg.delay_block([delay_stg1, delay_stg2], num_instances=4)()
    vmm_out = fg.vmm_12x4([min_det_out, delay_stg1, delay_stg3], num_instances=1)
    nmirror_out = fg.nmirror_w_bias(nmirror_out)
    wta_out = fg.wta_new([vmm_out, nmirror_out, gnd], num_instances=4)
    outpad = fg.outpada(wta_out, [9, 10, 11, 12])

def small_afe(pre=None):
    parallel_rows = 4
    bpf = fg.bandpass_filter(pre, num_instances=parallel_rows)
    amp = fg.amplitude_detect(bpf, num_instances=parallel_rows)
    delay1 = fg.ladder_filter(amp, None, num_instances=parallel_rows)
    delay2 = fg.ladder_filter(delay1, delay1, num_instances=parallel_rows)
    return bpf, amp, delay1, delay2

def small_classifier(vector_in):
    vmm = fg.vector_matrix_multiply(vector_in, dims=(1,6))
    wta = fg.wta_direct_vmm(vmm, vmm, vmm, vmm, num_instances=1)
    scan = fg.scanner(wta, wta, wta, wta, num_instances=1)
    return vmm, wta, scan

def the_small_asic_v2():
    '''
    This version of the design calls an AFE cell with cells at the edge but internal dimensions fixed
    '''
    afe = fg.fixed_size_afe(None)
    vector_in = [afe]
    vmm, wta, scan = small_classifier(vector_in)
    return vmm, afe, wta, scan

def the_small_asic_v1():
    '''
    This version of the design does not have pins at the edge of the AFE
    '''
    pre_bpf = fg.bandpass_filter(None)
    bpf, amp, delay1, delay2 = small_afe(pre_bpf)
    vector_in = [amp, delay1, delay2]
    vmm, wta, scan = small_classifier(vector_in)
    return bpf, amp, delay1, delay2, vmm, wta, scan, pre_bpf

def test0():
    vmm = fg.vector_matrix_multiply(None)
    return vmm

# 3/28/2023 new examples
def test1():
    inpad1 = fg.inpad([1])
    input_voltage = fg.dc_in(1.3)
    c4_out = fg.c4_sp([inpad1, input_voltage])
    outpada = fg.outpada(c4_out, [13])

def test2():
    inpad1 = fg.inpad([1])
    inpad2 = fg.inpad([2])
    lpf_out1 = fg.lpfota(inpad1)
    lpf_out2 = fg.lpfota(inpad2)
    outpad1 = fg.outpada(lpf_out1, [14])
    outpad2 = fg.outpada(lpf_out2, [13])

def test3():
    inpad1 = fg.inpad([1])
    inpad2 = fg.inpad([2])
    lpf_out1 = fg.MSOS02(inpad1, MSOS02_Buffer='4e-06')
    lpf_out2 = fg.MSOS02(inpad2)
    outpad1 = fg.outpada(lpf_out1, [14])
    outpad2 = fg.outpada(lpf_out2, [13])

## ORS GUI Examples
def LPF_offchip():
    inpad1 = fg.inpad([3])
    lpf_out1 = fg.lpfota(inpad1)
    outpad1 = fg.outpada(lpf_out1, [13])

def c4_offchip():
    inpad1 = fg.inpad([1])
    input_voltage = fg.dc_in(1.3)
    c4_out = fg.c4_sp([inpad1, input_voltage])
    outpada = fg.outpada(c4_out, [13])

def MSOS02_test01():
    inpad1 = fg.inpad([1])
    mead_out = fg.MSOS02(inpad1)
    outpada = fg.outpada(mead_out, [13])

def ors_buffer():
    inpad1 = fg.inpad([5])
    buff_out = fg.ota_buf(inpad1)
    outpad = fg.outpada(buff_out, [6])
