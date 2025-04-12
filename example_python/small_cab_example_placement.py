import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *

from ashes_fg.asic.asic_systems import *


Top = Circuit()

# C,S,C Blocks
# -------------------------------------------------------------------------------
BlockIsland = Island(Top)

#VMM's
C_EW = IndirectVMM(Top,[20,12],island=BlockIsland,decoderPlace=False)
S = IndirectVMM(Top,[20,20],island=BlockIsland,decoderPlace=False,loc = [0,6])
C_NS = IndirectVMM(Top,[20,12],island=BlockIsland,decoderPlace=False,loc = [0,16])

#Gate Mux
Block_GateDecoder = STD_IndirectGateDecoder(Top,BlockIsland,6)
Block_GateSwitches = STD_IndirectGateSwitch(Top,BlockIsland,22)

#Drain Mux
Block_DrainDecoder = STD_DrainDecoder(Top,BlockIsland,5)
Block_DrainSel = STD_DrainSelect(Top,BlockIsland,5)
Block_DrainSwitches = STD_DrainSwitch(Top,BlockIsland,5)

# CAB
# -------------------------------------------------------------------------------
CABIsland = Island(Top)

#A
A = IndirectVMM(Top,[32,16],island=CABIsland,decoderPlace=False)
#B
B = IndirectVMM(Top,[32,18],island=CABIsland,decoderPlace=False,loc = [0,8])
#Output
Output = IndirectVMM(Top,[8,18],island=CABIsland,decoderPlace=False,loc = [8,8])

#Cells
TA_Strong = TSMC350nm_TA2Cell_Strong(Top,island=CABIsland)
TA_Strong.markCABDevice()
TA_Strong.place([2,17])

TA_LongL = TSMC350nm_TA2Cell_LongL_Cab(Top,island=CABIsland)
TA_LongL.markCABDevice()
TA_LongL.place([3,17])

TA_Weak = TSMC350nm_TA2Cell_Weak(Top,island=CABIsland)
TA_Weak.markCABDevice()
TA_Weak.place([4,17])

TA_NoFG = TSMC350nm_TA2Cell_NoFG(Top,island=CABIsland)
TA_NoFG.markCABDevice()
TA_NoFG.place([5,17])

WTA0 = TSMC350nm_4WTA(Top,island=CABIsland)
WTA0.markCABDevice()
WTA0.place([6,17])

WTA1 = TSMC350nm_4WTA(Top,island=CABIsland)
WTA1.markCABDevice()
WTA1.place([7,17])

#Drain Mux
CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,6)
CAB_DrainSel = STD_DrainSelect(Top,CABIsland,10)
CAB_DrainSwitches = STD_DrainSwitch(Top,CABIsland,10)

#Gate Mux
CAB_GateSwitches = STD_GorS_IndirectSwitches(Top,CABIsland,18)
CAB_GateIndirect = STD_IndirectGateSwitch(Top,CABIsland,col=17)


# Frame
# -------------------------------------------------------------------------------
cabFrame = frame(Top)
cabFrame.createPort("N")

design_limits = [1e6, 6.1e5]
location_islands = ((20600, 363500), (20600, 20000)) #<-location for tile v1

compile_asic(Top,process="TSMC350nm",fileName="small_cab_example_placement",p_and_r = True,design_limits = design_limits, location_islands = location_islands)