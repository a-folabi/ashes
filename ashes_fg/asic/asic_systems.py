import ashes_fg.class_lib_ext as fg

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

def test_cells():
    # Frame should generate iopad objects with numbers 0 - (num_pads - 1) who all keep track of their frame name
    frame = fg.pads_smallframe(num_pads=93, cell_type='ASIC')
    iopads = frame()
    # Inputs to cells can be passed implicitly through the input array or explicitly by naming each pin and assigning a value to it
    scanner = fg.sky130_hilas_ScannerVertical([iopads[1], iopads[2], iopads[92], iopads[91], iopads[3], iopads[90], iopads[89], iopads[4]])
    nfets = fg.tsmc65_stdcell_nfetGroup([], small_src=iopads[5], med_src=iopads[6], large_src=iopads[7], gate=iopads[88], drain=iopads[87])
    pfets = fg.tsmc65_stdcell_pfetGroup([], small_src=iopads[8], med_src=iopads[9], large_src=iopads[10], gate=iopads[86], drain=iopads[85], body=iopads[84])
    amp_det = fg.sky130_hilas_Alice_AmpDetect([], select=iopads[11], gate=iopads[83], output=iopads[82])
    ta_1fg = fg.sky130_hilas_TA2Cell_1FG([], select=[iopads[14], iopads[12]], gate=[iopads[13], iopads[81]], output=[iopads[15], iopads[80]])
    ta_0fg = fg.sky130_hilas_TA2Cell_NoFG([], gate=iopads[16], select=iopads[79], output=[iopads[17], iopads[78]])
    ta_strong_fg = fg.sky130_hilas_TA2Cell_1FG_Strong([], select=[iopads[19], iopads[18]], gate=[iopads[76], iopads[77]], output=[iopads[75], iopads[20]])
    bpf = fg.sky130_hilas_Alice_BPF([], select=[iopads[21], iopads[73]], gate=[iopads[22], iopads[74]], output=iopads[23])
    vmmwta = fg.sky130_hilas_VMMWTA([], select=iopads[70], gate=[iopads[25], iopads[24], iopads[72]], output=[iopads[26], iopads[27], iopads[69], iopads[68]])
    fg_char = fg.sky130_hilas_FGcharacterization01([], src=iopads[32], drain=iopads[63],  gate=[iopads[28], iopads[67], iopads[29], iopads[66]], output=iopads[30], volt_bias=iopads[64], volt_ref=iopads[31], cap=iopads[65])
    vmm = fg.sky130_hilas_swc4x2celld3([], gate=[iopads[62], iopads[61]])
    vmm_indir = fg.sky130_hilas_swc4x4_indirect([], select=[iopads[35], iopads[57], iopads[37], iopads[55]], gate=[iopads[58], iopads[36], iopads[56], iopads[38]], run_drain=[iopads[54], iopads[53], iopads[40], iopads[39]])
    
    return (scanner, nfets, pfets, amp_det, ta_1fg, ta_0fg, ta_strong_fg, bpf, vmmwta, fg_char, vmm, vmm_indir, frame)


def IndirectVMM(circuit,dim=[4,2], island=None,decoderPlace=True,loc=[0,0]):
    if (dim[0] % 4) != 0:
            raise Exception("Error: VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
            raise Exception("Error: VMM columns must be divisible by 2")

    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)

    VMMIsland = island
    if island == None:
          VMMIsland = Island(circuit)

    # Create VMM and place in an island
    VMM = TSMC350nm_4x2_Indirect(circuit,dim=(numRows,numCols),island=VMMIsland)
    circuit.placeInstance(VMM,loc)

    if decoderPlace == True:
        # Add decoders
        gateBits = int(np.ceil(np.log2(dim[1])))
        GateDecoder = STD_IndirectGateDecoder(circuit,VMMIsland,gateBits)
        GateSwitches = STD_IndirectGateSwitch(circuit,VMMIsland,numCols)

        drainBits = int(np.ceil(np.log2(dim[0])))
        DrainDecoder = STD_DrainDecoder(circuit,VMMIsland,drainBits)
        DrainSel = STD_DrainSelect(circuit,VMMIsland,numRows)
        DrainSwitches = STD_DrainSwitch(circuit,VMMIsland,numRows)

    return VMM

def VMMWTA(circuit,dim=[4,2],island=None,decoderPlace=True,loc=[0,0],inputs=None):
    if (dim[0] % 4) != 0:
        raise Exception("Error: VMM rows must be divisible by 4")
    if (dim[1] % 2) != 0:
        raise Exception("Error: VMM columns must be divisible by 2")
    
    numRows = int(dim[0]/4)
    numCols = int(dim[1]/2)

    VMMWTAIsland = island
    if island == None:
          VMMWTAIsland = Island(circuit)

    VMMWTA = TSMC350nm_VMMWTA(circuit,island=VMMWTAIsland,dim=[numRows,1])
    VMMWTA.place([loc[0],loc[1]+numCols-1])
    
    VMM = None
    if numCols > 1:
         VMM = IndirectVMM(circuit,island=VMMWTAIsland,dim=[dim[0],dim[1]-2],decoderPlace=False)
         VMMWTA.markAbut()

         
    if decoderPlace == True:
        # Add decoders
        gateBits = int(np.ceil(np.log2(dim[1])))
        GateDecoder = STD_IndirectGateDecoder(circuit,VMMWTAIsland,gateBits)
        GateSwitches = STD_IndirectGateSwitch(circuit,VMMWTAIsland,numCols)


        if inputs != None:
            GateDecoder.VGRUN[0:numCols*2] += inputs

        drainBits = int(np.ceil(np.log2(dim[0])))
        DrainDecoder = STD_DrainDecoder(circuit,VMMWTAIsland,drainBits)
        DrainSel = STD_DrainSelect(circuit,VMMWTAIsland,numRows)
        DrainSwitches = STD_DrainSwitch(circuit,VMMWTAIsland,numRows)

    return VMMWTA.Vout