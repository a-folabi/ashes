from ashes_fg.class_lib import *
from ashes_fg.asic.exceptions import *
import sys

class tsmc65_stdcell_nfetGroup(tsmc65_stdcell_nfetGroup):
    '''
    Input Order
    -------------------
    self.nfet_small_src = input[0]
    self.nfet_med_src = input[1]
    self.nfet_large_src = input[2]
    self.nfet_gate = input[3]
    self.nfet_drain = input[4]
    '''
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', small_src = None, med_src = None, large_src = None, gate = None, drain = None):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 5:
            self.nfet_small_src = input[0]
            self.nfet_med_src = input[1]
            self.nfet_large_src = input[2]
            self.nfet_gate = input[3]
            self.nfet_drain = input[4]
        else:
            self.nfet_small_src = small_src
            self.nfet_med_src = med_src
            self.nfet_large_src = large_src
            self.nfet_gate = gate
            self.nfet_drain = drain
            
class tsmc65_stdcell_pfetGroup(tsmc65_stdcell_pfetGroup):
    '''
    Input Order
    -------------------
    self.pfet_small_src = input[0]
    self.pfet_med_src = input[1]
    self.pfet_large_src = input[2]
    self.pfet_gate = input[3]
    self.pfet_drain = input[4]
    self.pfet_body = input[5]
    '''
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', small_src = None, med_src = None, large_src = None, gate = None, drain = None, body = None):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 6:
            self.pfet_small_src = input[0]
            self.pfet_med_src = input[1]
            self.pfet_large_src = input[2]
            self.pfet_gate = input[3]
            self.pfet_drain = input[4]
            self.pfet_body = input[5]
        else:
            self.pfet_small_src = small_src
            self.pfet_med_src = med_src
            self.pfet_large_src = large_src
            self.pfet_gate = gate
            self.pfet_drain = drain
            self.pfet_body = body

class scanner(sky130_hilas_ScannerVertical):
    '''
	Scanner cell tiles verically and uses a shift register to control up to 4 tgates that are connected to inputs. These tgates all feed the same output line and as a single high bit is moved through the shift register, a new input can be connected to the output line.
	'''
    
    cell_name = sky130_hilas_ScannerVertical.__name__
    def __init__(self, in0, in1, in2, in3, num_instances = 1, cell_type = 'ASIC'):
        super().__init__(input, num_instances, cell_type)
        self.island = sys._getframe(1).f_code.co_name
        self.num_outputs = 1
        self.INPUT1_1 = in0
        self.INPUT1_2 = in1
        self.INPUT1_3 = in2
        self.INPUT1_4 = in3
        self.RESET_B_1 = None
        self.OUTPUT = 'output'
        self.CLK1 = None
        self.D = None
        self.GND = None
        self.Q_out = None
        self.RESET_B_2 = None
        self.VPWR_DFF = None
        self.VPWR_TGATE = None
        
class amplitude_detect(sky130_hilas_Alice_AmpDetect):
    '''
    Amplitude detect asic cell
    '''
    
    cell_name = sky130_hilas_Alice_AmpDetect.__name__
    def __init__(self, amp_in, num_instances = 1, cell_type = 'ASIC'):
        super().__init__(input, num_instances, cell_type)
        self.vin = amp_in
        self.island = sys._getframe(1).f_code.co_name
        self.num_outputs = 1
        self.colsel = None
        self.gate = None
        self.ampdet_out = 'output'
        self.drain_one = None
        self.drain_two = None
        self.vgnd = None
        self.vinj = None
        self.vpwr = None
    def __call__(self):
        return self

class bandpass_filter(sky130_hilas_Alice_BPF):
    '''
    Bandpass filter asic cell
    '''
    
    cell_name = sky130_hilas_Alice_BPF.__name__
    def __init__(self, bpf_in, num_instances = 1, cell_type = 'ASIC'):
        super().__init__(input, num_instances, cell_type)
        self.bpf_in = bpf_in
        self.island = sys._getframe(1).f_code.co_name
        self.num_outputs = 1
        self.Vref = None
        self.colsel1 = None
        self.colsel2 = None
        self.drain_one = None
        self.drain_two = None
        self.gate1 = None
        self.gate2 = None
        self.gnd = None
        self.out = 'output'
        self.vinj1 = None
        self.vinj2 = None
        self.vpwr = None
        self.vtun = None
    def __call__(self):
        return self

class ladder_filter(sky130_hilas_Alice_DelayBlock):
    
    cell_name = sky130_hilas_Alice_DelayBlock.__name__
    def __init__(self, in1, in2, num_instances = 1, cell_type = 'ASIC'):
        super().__init__(input, num_instances, cell_type)
        self.VPREVOUT = in2
        self.VIN = in1
        self.island = sys._getframe(1).f_code.co_name
        self.num_outputs = 1
        self.DRAIN1 = None
        self.DRAIN2 = None
        self.Colsel1 = None
        self.ColSel2 = None
        self.ColSel3 = None
        self.ColSel4 = None
        self.Gate1 = None
        self.Gate2 = None
        self.Gate3 = None
        self.Gate4 = None
        self.GND = None
        self.Vinj = None
        self.Vnextin1 = 'output'
        self.Vnextout1 = None
        self.Voutbuff2 = None   
        self.Vpwr = None
        self.Vtun = None
    def __call__(self):
        return self

class vector_matrix_multiply(sky130_hilas_swc4x2celld3):
    '''
    4x2 Vector Matrix Multiply cell
    - Supply the input vector as an array. minimum two inputs.
    - To vary matrix size, must provide tuple to dims. 
    e.g. dims = (1, 6) creates (1*4 = 4) rows and (2*6 = 12) columns 
    '''
    
    cell_name = sky130_hilas_swc4x2celld3.__name__
    vector_in = []
    def __init__(self, vector_in, cell_type = 'ASIC', dims=(None, None)):
        num_instances = 1
        super().__init__(None, num_instances, cell_type)
        self.island = sys._getframe(1).f_code.co_name
        self.num_outputs = 4
        if dims:
            self.matrix_row = dims[0]
            self.matrix_column = dims[1]
        self.GND = None
        self.Vgate1 = 'input1'
        self.Vgate2 = 'input2'
        self.Vinj = None
        self.Vtun = None
        self.drain1 = 'output1'
        self.drain2 = 'output2'   
        self.drain3 = 'output3'
        self.drain4 = 'output4'
        # Flatten out vector inputs and assign single inputs to the vmm gates
        # For efficiency, store inputs as a tuple of (obj, num_copies) in the order they connect to the vmm
        if isinstance(vector_in, list):
            total_inputs = 0
            for item in vector_in:
                if isinstance(item, std_cell) and item.num_instances > 1:
                    total_inputs += item.num_instances
                    vals = [(item, item.num_instances)]
                    self.vector_in += vals
                elif isinstance(item, std_cell) and item.num_instances == 1 and item.num_outputs == 1:
                    total_inputs += 1
                    self.vector_in + [item]
                elif isinstance(item, std_cell) and item.num_instances == 1 and item.num_outputs > 1:
                    total_inputs += item.num_outputs
                    self.vector_in += [(item, item.num_instances)]
            if total_inputs != self.matrix_column*2:
                raise ParsingError(f'VMM ERROR- Inputs provided ({total_inputs}) do not align with specified column dimension {self.matrix_column*2}')
        else:
            raise ParsingError(f'VMM cell needs an input specified as a list, instead {vector_in} was provided')

    def __call__(self):
        return self

class wta_direct_vmm(tsmc65_stdcell_WTAandSwitches):
    '''
    4-input winner take all cell. Designed to interface with a VMM made up of direct floating gates.
    '''
    
    cell_name = tsmc65_stdcell_WTAandSwitches.__name__
    def __init__(self, drain0, drain1, drain2, drain3, num_instances=1, cell_type='ASIC'):
        super().__init__(input, num_instances, cell_type)
        self.island = sys._getframe(1).f_code.co_name
        self.num_outputs = 4
        self.drain_0 = drain0
        self.drain_1 = drain1
        self.drain_2 = drain2
        self.drain_3 = drain3
        self.Colsel = None
        self.GND = None
        self.Out_0 = 'output1'
        self.Out_1 = 'output2'
        self.Out_2 = 'output3'
        self.Out_3 = 'output4'
        self.Prog = None
        self.Run1 = None
        self.Run2 = None
        self.Vinj = None
        self.Vtun = None
        self.WTAMiddle = None
        self.run_source = None
    def __call__(self):
        return self

class fixed_size_afe(AFE_DAC):
    cell_name = AFE_DAC.__name__
    def __init__(self, input=None, num_instances=1, cell_type='ASIC'):
        super().__init__(input, num_instances, cell_type)
        self.island = sys._getframe(1).f_code.co_name
        self.num_outputs = 12
        self.sigout0 = 'output'
        self.sigout1 = 'output'
        self.sigout2 = 'output'
        self.sigout3 = 'output'
        self.sigout4 = 'output'
        self.sigout5 = 'output'
        self.sigout6 = 'output'
        self.sigout7 = 'output'
        self.sigout8 = 'output'
        self.sigout9 = 'output'
        self.sigout10 = 'output'
        self.sigout11 = 'output'
    def __call__(self):
        return self

class sky130_hilas_VMMWTA(sky130_hilas_VMMWTA):
   
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', gate = None, select = None, output = None):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 8:
            self.vgate = input[0]
            self.vgate1 = input[1]
            self.vgate2 = input[2]
            self.col_sel = input[3]
            self.output1 = input[4]
            self.output2 = input[5]
            self.output3 = input[6]
            self.output4 = input[7]
        else:
            self.vgate = gate[0]
            self.vgate1 = gate[1]
            self.vgate2 = gate[2]
            self.col_sel = select
            self.output1 = output[0]
            self.output2 = output[1]
            self.output3 = output[2]
            self.output4 = output[3]

class sky130_hilas_TA2Cell_1FG(sky130_hilas_TA2Cell_1FG):
    '''
    Input Order
    -------------------
    self.colsel2 = input[0]
    self.gate1 = input[1]
    self.colsel1 = input[2]
    self.out_one = input[3]
    self.gate2 = input[4]
    self.out_two = input[5]
    '''
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', select = None, gate = None, output = None):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 6:
            self.colsel2 = input[0]
            self.gate1 = input[1]
            self.colsel1 = input[2]
            self.out_one = input[3]
            self.gate2 = input[4]
            self.out_two = input[5]
        else:
            self.colsel2 = select[1]
            self.gate1 = gate[0]
            self.colsel1 = select[0]
            self.out_one = output[0]
            self.gate2 = gate[1]
            self.out_two = output[1]

class sky130_hilas_TA2Cell_NoFG(sky130_hilas_TA2Cell_NoFG):
    '''
    Input Order
    -------------------
    self.colsel = input[0]
    self.gate = input[1]
    self.out_one = input[2]
    self.out_two = input[3]
    '''
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', select = None, gate = None, output = None):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 4:
            self.colsel = input[0]
            self.gate = input[1]
            self.out_one = input[2]
            self.out_two = input[3]
        else:
            self.colsel = select
            self.gate = gate
            self.out_one = output[0]
            self.out_two = output[1]

class sky130_hilas_TA2Cell_1FG_Strong(sky130_hilas_TA2Cell_1FG_Strong):
    '''
    Input Order
    -------------------
    self.colsel2 = input[0]
    self.gate1 = input[1]
    self.colsel1 = input[2]
    self.out_one = input[3]
    self.gate2 = input[4]
    self.out_two = input[5]
    '''
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', select = None, gate = None, output = None):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 6:
            self.colsel2 = input[0]
            self.gate1 = input[1]
            self.colsel1 = input[2]
            self.out_one = input[3]
            self.gate2 = input[4]
            self.out_two = input[5]
        else:
            self.colsel2 = select[0]
            self.gate1 = gate[0]
            self.colsel1 = select[1]
            self.out_one = output[0]
            self.gate2 = gate[1]
            self.out_two = output[1]


class sky130_hilas_FGcharacterization01(sky130_hilas_FGcharacterization01):
    '''
    Input Order
    --------------------
    self.Gate1 = input[0]
    self.Gate2 = input[1]
    self.Gate3 = input[2]
    self.Gate4 = input[3]
    self.Vref = input[4]
    self.Vbias = input[5]
    self.SOURCE = input[6]
    self.DRAIN = input[7]
    self.LargeCapacitor = input[8]
    self.Output = input[9]
    '''
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', gate = None, volt_ref = None, src = None, drain = None, cap =  None, volt_bias = None, output = None ):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 10:
            self.Gate1 = input[0]
            self.Gate2 = input[1]
            self.Gate3 = input[2]
            self.Gate4 = input[3]
            self.Vref = input[4]
            self.Vbias = input[5]
            self.SOURCE = input[6]
            self.DRAIN = input[7]
            self.LargeCapacitor = input[8]
            self.Output = input[9]
        else:
            self.Gate1 = gate[0]
            self.Gate2 = gate[1]
            self.Gate3 = gate[2]
            self.Gate4 = gate[3]
            self.Vref = volt_ref
            self.Vbias = volt_bias
            self.SOURCE = src
            self.DRAIN = drain
            self.LargeCapacitor = cap
            self.Output = output



class sky130_hilas_swc4x4_indirect(sky130_hilas_swc4x4_indirect):
    '''
    Input Order
    --------------------
    self.gate1 = input[0]
    self.gate2 = input[1]
    self.gate3 = input[2]
    self.gate4 = input[3]
    self.col_sel1 = input[4]
    self.col_sel2 = input[5]
    self.col_sel3 = input[6]
    self.col_sel4 = input[7]
    self.run_drain1 = input[8]
    self.run_drain2 = input[9]
    self.run_drain3 = input[10]
    self.run_drain4 = input[11]
    '''
    def __init__(self, input, num_instances = 1, cell_type = 'ASIC', gate = None, select = None, run_drain = None):
        super().__init__(input, num_instances, cell_type)
        if len(input) == 12:
            self.gate1 = input[0]
            self.gate2 = input[1]
            self.gate3 = input[2]
            self.gate4 = input[3]
            self.col_sel1 = input[4]
            self.col_sel2 = input[5]
            self.col_sel3 = input[6]
            self.col_sel4 = input[7]
            self.run_drain1 = input[8]
            self.run_drain2 = input[9]
            self.run_drain3 = input[10]
            self.run_drain4 = input[11]
        else:
            self.gate1 = gate[0]
            self.gate2 = gate[1]
            self.gate3 = gate[2]
            self.gate4 = gate[3]
            self.col_sel1 = select[0]
            self.col_sel2 = select[1]
            self.col_sel3 = select[2]
            self.col_sel4 = select[3]
            self.run_drain1 = run_drain[0]
            self.run_drain2 = run_drain[1]
            self.run_drain3 = run_drain[2]
            self.run_drain4 = run_drain[3]