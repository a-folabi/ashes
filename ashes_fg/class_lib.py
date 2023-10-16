class std_cell:
	def __init__(self, input, num_instances, cell_type):
		self.input = input
		self.num_instances = num_instances
		self.cell_type = cell_type

class iopad:
	def __init__(self, frame, pad_num):
		self.frame = frame
		self.pad_num = pad_num

class frame:
	def __init__(self, num_pads, cell_type='ASIC', prefix_str='IO_'):
		self.num_pads = num_pads
		self.cell_type = cell_type
		self.prefix_str = prefix_str
	
	def __call__(self):
		self.iopads = [ iopad(self.__class__.__name__, f'{self.prefix_str}{i}') for i in range(self.num_pads)]
		return self.iopads

class inpad:
    def __init__(self, pad_number):
        self.pad_number = pad_number


class outpad:
    def __init__(self, input, pad_number):
        self.input = input
        self.pad_number = pad_number

class outpada:
	def __init__(self,input,pad_number):
		self.input=input
		self.pad_number=pad_number

class BPF:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='both',
                 Gain_Bias='3e-07',
                 Gain_Bias_n='3e-07',
                 Gain_Bias_p='3e-07',
                 Feedback_bias='3e-07',
                 Feedback_bias_n='3e-07',
                 Feedback_bias_p='3e-07',
                 Input_cap='2',
                 foundry='skywater',
                 process_node='130nm'):
        self.input = input
        self.num_instances = num_instances
        self.Gain_Bias = Gain_Bias
        self.Gain_Bias_n = Gain_Bias_n
        self.Gain_Bias_p = Gain_Bias_p
        self.Feedback_bias = Feedback_bias
        self.Feedback_bias_n = Feedback_bias_n
        self.Feedback_bias_p = Feedback_bias_p
        self.Input_cap = Input_cap


class SHblock1:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 SHblock1_ls='0',
                 SHblock1_Ibias='3e-06',
                 SHblock1_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.SHblock1_ls = SHblock1_ls
        self.SHblock1_Ibias = SHblock1_Ibias
        self.SHblock1_cap0_1x_cs = SHblock1_cap0_1x_cs


class switchint1:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 switchint1_ls='0',
                 switchint1_Ibias1='3e-06',
                 switchint1_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.switchint1_ls = switchint1_ls
        self.switchint1_Ibias1 = switchint1_Ibias1
        self.switchint1_cap0_1x_cs = switchint1_cap0_1x_cs


class lpfota:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 cut_off_freq='21.7'):
        self.input = input
        self.num_instances = num_instances
        self.cut_off_freq = cut_off_freq


class hhn_debug:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 hhn_debug_ls='0',
                 hhn_debug_fgswc_ibias='5.000D-08',
                 hhn_debug_fgota1_ibias='2e-06',
                 hhn_debug_fgota1_pbias='2e-06',
                 hhn_debug_fgota1_nbias='2e-06',
                 hhn_debug_fgota0_ibias='2e-06',
                 hhn_debug_fgota0_pbias='2e-06',
                 hhn_debug_fgota0_nbias='2e-06',
                 hhn_debug_ota0_ibias='2e-06',
                 hhn_debug_ota1_ibias='2e-06',
                 hhn_debug_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.hhn_debug_ls = hhn_debug_ls
        self.hhn_debug_fgswc_ibias = hhn_debug_fgswc_ibias
        self.hhn_debug_fgota1_ibias = hhn_debug_fgota1_ibias
        self.hhn_debug_fgota1_pbias = hhn_debug_fgota1_pbias
        self.hhn_debug_fgota1_nbias = hhn_debug_fgota1_nbias
        self.hhn_debug_fgota0_ibias = hhn_debug_fgota0_ibias
        self.hhn_debug_fgota0_pbias = hhn_debug_fgota0_pbias
        self.hhn_debug_fgota0_nbias = hhn_debug_fgota0_nbias
        self.hhn_debug_ota0_ibias = hhn_debug_ota0_ibias
        self.hhn_debug_ota1_ibias = hhn_debug_ota1_ibias
        self.hhn_debug_cap0_1x_cs = hhn_debug_cap0_1x_cs


class HH_RG_2s:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 HH_RG_2s_ls='0',
                 HH_RG_2s_Nafb_ibias='5.000D-08',
                 HH_RG_2s_syn0_ibias='5.000D-08',
                 HH_RG_2s_syn1_ibias='5.000D-08',
                 HH_RG_2s_pfet_ibias='5.000D-08',
                 HH_RG_2s_nmr_ibias='5.000D-08',
                 HH_RG_2s_Na_ibias='2e-06',
                 HH_RG_2s_Na_pbias='2e-06',
                 HH_RG_2s_Na_nbias='2e-06',
                 HH_RG_2s_K_ibias='2e-06',
                 HH_RG_2s_K_pbias='2e-06',
                 HH_RG_2s_K_nbias='2e-06',
                 HH_RG_2s_buf_ibias='2e-06',
                 HH_RG_2s_comp_ibias='2e-06',
                 HH_RG_2s_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.HH_RG_2s_ls = HH_RG_2s_ls
        self.HH_RG_2s_Nafb_ibias = HH_RG_2s_Nafb_ibias
        self.HH_RG_2s_syn0_ibias = HH_RG_2s_syn0_ibias
        self.HH_RG_2s_syn1_ibias = HH_RG_2s_syn1_ibias
        self.HH_RG_2s_pfet_ibias = HH_RG_2s_pfet_ibias
        self.HH_RG_2s_nmr_ibias = HH_RG_2s_nmr_ibias
        self.HH_RG_2s_Na_ibias = HH_RG_2s_Na_ibias
        self.HH_RG_2s_Na_pbias = HH_RG_2s_Na_pbias
        self.HH_RG_2s_Na_nbias = HH_RG_2s_Na_nbias
        self.HH_RG_2s_K_ibias = HH_RG_2s_K_ibias
        self.HH_RG_2s_K_pbias = HH_RG_2s_K_pbias
        self.HH_RG_2s_K_nbias = HH_RG_2s_K_nbias
        self.HH_RG_2s_buf_ibias = HH_RG_2s_buf_ibias
        self.HH_RG_2s_comp_ibias = HH_RG_2s_comp_ibias
        self.HH_RG_2s_cap0_1x_cs = HH_RG_2s_cap0_1x_cs


class subbandArray:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 SubbandArray_ls='0',
                 SubbandArray_FBbias='5.000D-10',
                 SubbandArray_FBpbias='5.000D-08',
                 SubbandArray_FBnbias='5.000D-08',
                 SubbandArray_FFbias='5.000D-08',
                 SubbandArray_FFpbias='5.000D-08',
                 SubbandArray_FFnbias='5.000D-08',
                 SubbandArray_Maxota='5.000D-08',
                 SubbandArray_LPF='3.000D-09',
                 SubbandArray_FFcap_1x_cs='1',
                 SubbandArray_FBcap_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.SubbandArray_ls = SubbandArray_ls
        self.SubbandArray_FBbias = SubbandArray_FBbias
        self.SubbandArray_FBpbias = SubbandArray_FBpbias
        self.SubbandArray_FBnbias = SubbandArray_FBnbias
        self.SubbandArray_FFbias = SubbandArray_FFbias
        self.SubbandArray_FFpbias = SubbandArray_FFpbias
        self.SubbandArray_FFnbias = SubbandArray_FFnbias
        self.SubbandArray_Maxota = SubbandArray_Maxota
        self.SubbandArray_LPF = SubbandArray_LPF
        self.SubbandArray_FFcap_1x_cs = SubbandArray_FFcap_1x_cs
        self.SubbandArray_FBcap_1x_cs = SubbandArray_FBcap_1x_cs


class common_drain:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 common_drain_ls='0',
                 common_drain_fgswc_ibias='5.000D-08'):
        self.input = input
        self.num_instances = num_instances
        self.common_drain_ls = common_drain_ls
        self.common_drain_fgswc_ibias = common_drain_fgswc_ibias


class Senseamp1:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 Senseamp1_ls='0',
                 Senseamp1_fgota0_ibias='5e-07',
                 Senseamp1_fgota0_pbias='2e-07',
                 Senseamp1_fgota0_nbias='2e-07',
                 Senseamp1_ota0_ibias='3e-06'):
        self.input = input
        self.num_instances = num_instances
        self.Senseamp1_ls = Senseamp1_ls
        self.Senseamp1_fgota0_ibias = Senseamp1_fgota0_ibias
        self.Senseamp1_fgota0_pbias = Senseamp1_fgota0_pbias
        self.Senseamp1_fgota0_nbias = Senseamp1_fgota0_nbias
        self.Senseamp1_ota0_ibias = Senseamp1_ota0_ibias


class Hyst_diff:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 Hyst_diff_ls='0',
                 Hyst_diff_ota1_ibias='2e-06'):
        self.input = input
        self.num_instances = num_instances
        self.Hyst_diff_ls = Hyst_diff_ls
        self.Hyst_diff_ota1_ibias = Hyst_diff_ota1_ibias


class common_drain_nfet:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 common_drain_nfet_ls='0',
                 common_drain_nfet_ibias='5.000D-08'):
        self.input = input
        self.num_instances = num_instances
        self.common_drain_nfet_ls = common_drain_nfet_ls
        self.common_drain_nfet_ibias = common_drain_nfet_ibias


class ota_buf:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 ota_buf_bias='1e-05'):
        self.input = input
        self.num_instances = num_instances
        self.ota_buf_bias = ota_buf_bias


class hhn:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 hhn_ls='0',
                 hhn_fgswc_ibias='5.000D-08',
                 hhn_fgota1_ibias='2e-06',
                 hhn_fgota1_pbias='2e-06',
                 hhn_fgota1_nbias='2e-06',
                 hhn_fgota0_ibias='2e-06',
                 hhn_fgota0_pbias='2e-06',
                 hhn_fgota0_nbias='2e-06',
                 hhn_ota0_ibias='2e-06',
                 hhn_ota1_ibias='2e-06',
                 hhn_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.hhn_ls = hhn_ls
        self.hhn_fgswc_ibias = hhn_fgswc_ibias
        self.hhn_fgota1_ibias = hhn_fgota1_ibias
        self.hhn_fgota1_pbias = hhn_fgota1_pbias
        self.hhn_fgota1_nbias = hhn_fgota1_nbias
        self.hhn_fgota0_ibias = hhn_fgota0_ibias
        self.hhn_fgota0_pbias = hhn_fgota0_pbias
        self.hhn_fgota0_nbias = hhn_fgota0_nbias
        self.hhn_ota0_ibias = hhn_ota0_ibias
        self.hhn_ota1_ibias = hhn_ota1_ibias
        self.hhn_cap0_1x_cs = hhn_cap0_1x_cs


class Min_detect:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 Min_detect_ls='0',
                 Min_detect_fgswc_ibias='5.000D-08',
                 Min_detect_ota0_ibias='2e-06'):
        self.input = input
        self.num_instances = num_instances
        self.Min_detect_ls = Min_detect_ls
        self.Min_detect_fgswc_ibias = Min_detect_fgswc_ibias
        self.Min_detect_ota0_ibias = Min_detect_ota0_ibias


class signalmult:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 signalmult_fg='1e-06',
                 signalmult_v1p='5e-08',
                 signalmult_v1n='5e-08'):
        self.input = input
        self.num_instances = num_instances
        self.signalmult_fg = signalmult_fg
        self.signalmult_v1p = signalmult_v1p
        self.signalmult_v1n = signalmult_v1n


class common_source:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 common_source_ls='0',
                 common_source_ibias='5.000D-08'):
        self.input = input
        self.num_instances = num_instances
        self.common_source_ls = common_source_ls
        self.common_source_ibias = common_source_ibias


class VolDivide1:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 VolDivide1_ls='0',
                 VolDivide1_fgota0_ibias='2e-06',
                 VolDivide1_fgota0_pbias='2e-06',
                 VolDivide1_fgota0_nbias='2e-06',
                 VolDivide1_ota0_ibias='2e-06'):
        self.input = input
        self.num_instances = num_instances
        self.VolDivide1_ls = VolDivide1_ls
        self.VolDivide1_fgota0_ibias = VolDivide1_fgota0_ibias
        self.VolDivide1_fgota0_pbias = VolDivide1_fgota0_pbias
        self.VolDivide1_fgota0_nbias = VolDivide1_fgota0_nbias
        self.VolDivide1_ota0_ibias = VolDivide1_ota0_ibias


class HH_RG_3s:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 HH_RG_3s_ls='0',
                 HH_RG_3s_Nafb_ibias='5.000D-08',
                 HH_RG_3s_syn0_ibias='5.000D-08',
                 HH_RG_3s_syn1_ibias='5.000D-08',
                 HH_RG_3s_syn2_ibias='5.000D-08',
                 HH_RG_3s_pfet_ibias='5.000D-08',
                 HH_RG_3s_nmr_ibias='5.000D-08',
                 HH_RG_3s_Na_ibias='2e-06',
                 HH_RG_3s_Na_pbias='2e-06',
                 HH_RG_3s_Na_nbias='2e-06',
                 HH_RG_3s_K_ibias='2e-06',
                 HH_RG_3s_K_pbias='2e-06',
                 HH_RG_3s_K_nbias='2e-06',
                 HH_RG_3s_buf_ibias='2e-06',
                 HH_RG_3s_comp_ibias='2e-06',
                 HH_RG_3s_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.HH_RG_3s_ls = HH_RG_3s_ls
        self.HH_RG_3s_Nafb_ibias = HH_RG_3s_Nafb_ibias
        self.HH_RG_3s_syn0_ibias = HH_RG_3s_syn0_ibias
        self.HH_RG_3s_syn1_ibias = HH_RG_3s_syn1_ibias
        self.HH_RG_3s_syn2_ibias = HH_RG_3s_syn2_ibias
        self.HH_RG_3s_pfet_ibias = HH_RG_3s_pfet_ibias
        self.HH_RG_3s_nmr_ibias = HH_RG_3s_nmr_ibias
        self.HH_RG_3s_Na_ibias = HH_RG_3s_Na_ibias
        self.HH_RG_3s_Na_pbias = HH_RG_3s_Na_pbias
        self.HH_RG_3s_Na_nbias = HH_RG_3s_Na_nbias
        self.HH_RG_3s_K_ibias = HH_RG_3s_K_ibias
        self.HH_RG_3s_K_pbias = HH_RG_3s_K_pbias
        self.HH_RG_3s_K_nbias = HH_RG_3s_K_nbias
        self.HH_RG_3s_buf_ibias = HH_RG_3s_buf_ibias
        self.HH_RG_3s_comp_ibias = HH_RG_3s_comp_ibias
        self.HH_RG_3s_cap0_1x_cs = HH_RG_3s_cap0_1x_cs


class switchcapint1:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 switchcapint1_Bias='3e-06',
                 switchcapint1_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.switchcapint1_Bias = switchcapint1_Bias
        self.switchcapint1_cap0_1x_cs = switchcapint1_cap0_1x_cs


class switchAmplifier1:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 switchAmplifier1_ls='0',
                 switchAmplifier1_ota0_ibias='3e-06',
                 switchAmplifier1_cap0_1x_cs='1',
                 switchAmplifier1_cap1_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.switchAmplifier1_ls = switchAmplifier1_ls
        self.switchAmplifier1_ota0_ibias = switchAmplifier1_ota0_ibias
        self.switchAmplifier1_cap0_1x_cs = switchAmplifier1_cap0_1x_cs
        self.switchAmplifier1_cap1_1x_cs = switchAmplifier1_cap1_1x_cs


class SOSLPF:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 SOSLPF_ls='0',
                 SOSLPF_Ibias2='2e-07',
                 SOSLPF_FG2p='1e-06',
                 SOSLPF_FG2n='1e-06',
                 SOSLPF_Ibias1='2e-07',
                 SOSLPF_FG1p='1e-06',
                 SOSLPF_FG1n='1e-06',
                 SOSLPF_Feedback='4.000D-09',
                 SOSLPF_Buffer='1e-06'):
        self.input = input
        self.num_instances = num_instances
        self.SOSLPF_ls = SOSLPF_ls
        self.SOSLPF_Ibias2 = SOSLPF_Ibias2
        self.SOSLPF_FG2p = SOSLPF_FG2p
        self.SOSLPF_FG2n = SOSLPF_FG2n
        self.SOSLPF_Ibias1 = SOSLPF_Ibias1
        self.SOSLPF_FG1p = SOSLPF_FG1p
        self.SOSLPF_FG1n = SOSLPF_FG1n
        self.SOSLPF_Feedback = SOSLPF_Feedback
        self.SOSLPF_Buffer = SOSLPF_Buffer


class Max_detect:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 Max_detect_ls='0',
                 Max_detect_fgswc_ibias='5.000D-08',
                 Max_detect_ota0_ibias='2e-06'):
        self.input = input
        self.num_instances = num_instances
        self.Max_detect_ls = Max_detect_ls
        self.Max_detect_fgswc_ibias = Max_detect_fgswc_ibias
        self.Max_detect_ota0_ibias = Max_detect_ota0_ibias


class MSOS02:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 MSOS02_ls='0',
                 MSOS02_Ibias2='2e-07',
                 MSOS02_Wbp='1e-06',
                 MSOS02_Wbn='1e-06',
                 MSOS02_Ibias1='2e-07',
                 MSOS02_Wap='1e-06',
                 MSOS02_Wan='1e-06',
                 MSOS02_Feedback='4.000D-09',
                 MSOS02_Buffer='3e-06'):
        self.input = input
        self.num_instances = num_instances
        self.MSOS02_ls = MSOS02_ls
        self.MSOS02_Ibias2 = MSOS02_Ibias2
        self.MSOS02_Wbp = MSOS02_Wbp
        self.MSOS02_Wbn = MSOS02_Wbn
        self.MSOS02_Ibias1 = MSOS02_Ibias1
        self.MSOS02_Wap = MSOS02_Wap
        self.MSOS02_Wan = MSOS02_Wan
        self.MSOS02_Feedback = MSOS02_Feedback
        self.MSOS02_Buffer = MSOS02_Buffer


class c4_sp:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 Gain_Bias='3e-06',
                 Gain_Bias_n='1e-06',
                 Gain_Bias_p='1e-06',
                 Feedback_bias='3.000D-09',
                 Feedback_bias_n='1.000D-09',
                 Feedback_bias_p='1.000D-09',
                 num_caps='6'):
        self.input = input
        self.num_instances = num_instances
        self.Gain_Bias = Gain_Bias
        self.Gain_Bias_n = Gain_Bias_n
        self.Gain_Bias_p = Gain_Bias_p
        self.Feedback_bias = Feedback_bias
        self.Feedback_bias_n = Feedback_bias_n
        self.Feedback_bias_p = Feedback_bias_p
        self.num_caps = num_caps


class HH_RG:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 HH_RG_ls='0',
                 HH_RG_Nafb_ibias='5.000D-08',
                 HH_RG_in0_ibias='5.000D-08',
                 HH_RG_pfet_ibias='5.000D-08',
                 HH_RG_nmr_ibias='5.000D-08',
                 HH_RG_Na_ibias='2e-06',
                 HH_RG_Na_pbias='2e-06',
                 HH_RG_Na_nbias='2e-06',
                 HH_RG_K_ibias='2e-06',
                 HH_RG_K_pbias='2e-06',
                 HH_RG_K_nbias='2e-06',
                 HH_RG_buf_ibias='2e-06',
                 HH_RG_comp_ibias='2e-06',
                 HH_RG_cap0_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.HH_RG_ls = HH_RG_ls
        self.HH_RG_Nafb_ibias = HH_RG_Nafb_ibias
        self.HH_RG_in0_ibias = HH_RG_in0_ibias
        self.HH_RG_pfet_ibias = HH_RG_pfet_ibias
        self.HH_RG_nmr_ibias = HH_RG_nmr_ibias
        self.HH_RG_Na_ibias = HH_RG_Na_ibias
        self.HH_RG_Na_pbias = HH_RG_Na_pbias
        self.HH_RG_Na_nbias = HH_RG_Na_nbias
        self.HH_RG_K_ibias = HH_RG_K_ibias
        self.HH_RG_K_pbias = HH_RG_K_pbias
        self.HH_RG_K_nbias = HH_RG_K_nbias
        self.HH_RG_buf_ibias = HH_RG_buf_ibias
        self.HH_RG_comp_ibias = HH_RG_comp_ibias
        self.HH_RG_cap0_1x_cs = HH_RG_cap0_1x_cs


class gpio_in:
    def __init__(self):
        pass


class dc_in:
    def __init__(self, DC_value):
        self.DC_value = DC_value


class GENARB_f:
    def __init__(self, input):
        self.input = input


class meas_volt:
    def __init__(self, input):
        self.input = input


class cap:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 cap_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.cap_1x_cs = cap_1x_cs


class I_SenseAmp:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 I_SenseAmp_ls='0',
                 I_SenseAmp_fgota0_ibias='2e-06',
                 I_SenseAmp_fgota0_pbias='2e-06',
                 I_SenseAmp_fgota0_nbias='2e-06',
                 I_SenseAmp_ota0_ibias='2e-06',
                 I_SenseAmp_cap0_1x_cs='1',
                 I_SenseAmp_cap1_1x_cs='1'):
        self.input = input
        self.num_instances = num_instances
        self.I_SenseAmp_ls = I_SenseAmp_ls
        self.I_SenseAmp_fgota0_ibias = I_SenseAmp_fgota0_ibias
        self.I_SenseAmp_fgota0_pbias = I_SenseAmp_fgota0_pbias
        self.I_SenseAmp_fgota0_nbias = I_SenseAmp_fgota0_nbias
        self.I_SenseAmp_ota0_ibias = I_SenseAmp_ota0_ibias
        self.I_SenseAmp_cap0_1x_cs = I_SenseAmp_cap0_1x_cs
        self.I_SenseAmp_cap1_1x_cs = I_SenseAmp_cap1_1x_cs


class ota:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 ota_bias='1e-06'):
        self.input = input
        self.num_instances = num_instances
        self.ota_bias = ota_bias


class tgate2:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a']):
        self.input = input
        self.num_instances = num_instances


class pfet:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a']):
        self.input = input
        self.num_instances = num_instances


class nfet:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a']):
        self.input = input
        self.num_instances = num_instances


class mite_FG:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 mite_fg0='1.000D-07'):
        self.input = input
        self.num_instances = num_instances
        self.mite_fg0 = mite_fg0


class wta_new:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 wta_new_ls='0',
                 wta_new_wta_bias='1.000D-08',
                 wta_new_buf_bias='2e-06'):
        self.input = input
        self.num_instances = num_instances
        self.wta_new_ls = wta_new_ls
        self.wta_new_wta_bias = wta_new_wta_bias
        self.wta_new_buf_bias = wta_new_buf_bias


class vmm12x1_wowta:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 vmm12x1_wowta_fg='0',
                 vmm12x1_target=[
                     '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09',
                     '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09',
                     '1.000D-09', '1.000D-09', '1.000D-09', '1.000D-09'
                 ],
                 vmm12x1_offsetbias='5.000D-09'):
        self.input = input
        self.num_instances = num_instances
        self.vmm12x1_wowta_fg = vmm12x1_wowta_fg
        self.vmm12x1_target = vmm12x1_target
        self.vmm12x1_offsetbias = vmm12x1_offsetbias


class fgswitch:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 fgswitch_ls='0',
                 fgswitch_fgswc_ibias='5.000D-08'):
        self.input = input
        self.num_instances = num_instances
        self.fgswitch_ls = fgswitch_ls
        self.fgswitch_fgswc_ibias = fgswitch_fgswc_ibias


class fgota:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 fgota_bias='1.000D-08',
                 fgota_p_bias='1.9',
                 fgota_n_bias='1.9',
                 fgota_small_cap='1'):
        self.input = input
        self.num_instances = num_instances
        self.fgota_bias = fgota_bias
        self.fgota_p_bias = fgota_p_bias
        self.fgota_n_bias = fgota_n_bias
        self.fgota_small_cap = fgota_small_cap


class tgate:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a']):
        self.input = input
        self.num_instances = num_instances


class nmirror_w_bias:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 nmirror_w_bias_ls='0',
                 nmirror_w_bias_ibias='5.000D-08'):
        self.input = input
        self.num_instances = num_instances
        self.nmirror_w_bias_ls = nmirror_w_bias_ls
        self.nmirror_w_bias_ibias = nmirror_w_bias_ibias


class ota2:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 ota2_bias='1e-06'):
        self.input = input
        self.num_instances = num_instances
        self.ota2_bias = ota2_bias


class nmirror:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a']):
        self.input = input
        self.num_instances = num_instances


class vdd:
    def __init__(self):
        pass


class output_f:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a']):
        self.input = input
        self.num_instances = num_instances


class gnd:
    def __init__(self):
        pass


class sr_1i_16o:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 output_num='16'):
        self.input = input
        self.num_instances = num_instances
        self.output_num = output_num

    def __call__(self):
        return [self, self, self]


class delay_block:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 delay_block_ls='0',
                 delay_block_ota0_ibias='2e-06',
                 delay_block_ota1_ibias='2e-06'):
        self.input = input
        self.num_instances = num_instances
        self.delay_block_ls = delay_block_ls
        self.delay_block_ota0_ibias = delay_block_ota0_ibias
        self.delay_block_ota1_ibias = delay_block_ota1_ibias

    def __call__(self):
        return [self, self]


class vmm_12x4:
    def __init__(self,
                 input,
                 num_instances='1',
                 type='FPAA',
                 board=['3.0', '3.0a'],
                 vmm_12x4_ls='0',
                 vmm_12x4_in1=[
                     5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08,
                     5e-08, 5e-08, 5e-08, 5e-08
                 ],
                 vmm_12x4_in2=[
                     5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08,
                     5e-08, 5e-08, 5e-08, 5e-08
                 ],
                 vmm_12x4_in3=[
                     5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08,
                     5e-08, 5e-08, 5e-08, 5e-08
                 ],
                 vmm_12x4_in4=[
                     5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08, 5e-08,
                     5e-08, 5e-08, 5e-08, 5e-08
                 ]):
        self.input = input
        self.num_instances = num_instances
        self.vmm_12x4_ls = vmm_12x4_ls
        self.vmm_12x4_in1 = vmm_12x4_in1
        self.vmm_12x4_in2 = vmm_12x4_in2
        self.vmm_12x4_in3 = vmm_12x4_in3
        self.vmm_12x4_in4 = vmm_12x4_in4

    def __call__(self):
        return [self, self, self, self]


class AFE_big_DAC(std_cell):
	pass

class AFE_DAC(std_cell):
	pass

class AFE_row_2delays(std_cell):
	pass

class padframe_aug(frame):
	pass

class pads_bigframe(frame):
	pass

class pads_smallframe(frame):
	pass

class sky130_hilas_Alice_AmpDetect(std_cell):
	pass

class sky130_hilas_Alice_BPF(std_cell):
	pass

class sky130_hilas_Alice_DelayBlock(std_cell):
	pass

class sky130_hilas_Alice_DelayBlock_16out(std_cell):
	pass

class sky130_hilas_drainSelect01d3(std_cell):
	pass

class sky130_hilas_FGcharacterization01(std_cell):
	pass

class sky130_hilas_FourTgate_ThickOx(std_cell):
	pass

class sky130_hilas_ScannerVertical(std_cell):
	pass

class sky130_hilas_swc4x2celld3(std_cell):
	pass

class sky130_hilas_swc4x4_indirect(std_cell):
	pass

class sky130_hilas_TA2Cell_1FG(std_cell):
	pass

class sky130_hilas_TA2Cell_1FG_Strong(std_cell):
	pass

class sky130_hilas_TA2Cell_NoFG(std_cell):
	pass

class sky130_hilas_VinjDecode2to4(std_cell):
	pass

class sky130_hilas_VinjDecode2to4_AFE(std_cell):
	pass

class sky130_hilas_VinjDecode4to12_Gate(std_cell):
	pass

class sky130_hilas_VinjDecode4to16_Gate(std_cell):
	pass

class sky130_hilas_VinjDecode5to24(std_cell):
	pass

class sky130_hilas_VinjDecode5to32(std_cell):
	pass

class sky130_hilas_VMMWTA(std_cell):
	pass

class sky130_hilas_Voltage_DAC_6bit(std_cell):
	pass

class temp_cell(std_cell):
	pass

class tsmc65_arbgen_test(std_cell):
	pass

class tsmc65_stdcell_AFE_drainSelect_2rows(std_cell):
	pass

class tsmc65_stdcell_AFE_row_Gate_4to16_Decoders(std_cell):
	pass

class tsmc65_stdcell_AFE_row_Gate_BPFAMP_Decoders(std_cell):
	pass

class tsmc65_stdcell_ArbGen(std_cell):
	pass

class tsmc65_stdcell_DFFandTgate(std_cell):
	pass

class tsmc65_stdcell_DFFandTgate_Tile(std_cell):
	pass

class tsmc65_stdcell_GateMuxSwc(std_cell):
	pass

class tsmc65_stdcell_GateMuxSwc_AmpDetect(std_cell):
	pass

class tsmc65_stdcell_GateMuxSwc_BPF(std_cell):
	pass

class tsmc65_stdcell_GateMuxSwc_DelayLine(std_cell):
	pass

class tsmc65_stdcell_GateMuxSwc_Tile(std_cell):
	pass

class tsmc65_stdcell_GateMuxSwc_WTA(std_cell):
	pass

class tsmc65_stdcell_HopfieldRow_4Stack(std_cell):
	pass

class tsmc65_stdcell_Hopfield_BMatrix_WTA(std_cell):
	pass

class tsmc65_stdcell_nfetGroup(std_cell):
	pass

class tsmc65_stdcell_pfetGroup(std_cell):
	pass

class tsmc65_stdcell_WTAandSwitches(std_cell):
	pass

class VMM_big_DAC(std_cell):
	pass

class VMM_DAC(std_cell):
	pass

