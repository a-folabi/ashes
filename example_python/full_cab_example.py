import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *


Top = Circuit()

# C,S,C Blocks
# -------------------------------------------------------------------------------
BlockIsland = Island(Top)

#VMM's
C_EW = IndirectVMM(Top,[20,14],island=BlockIsland,decoderPlace=False)
C_NS = IndirectVMM(Top,[20,18],island=BlockIsland,decoderPlace=False,loc = [0,17])

Block_Switch = ST_BMatrix(Top,BlockIsland,[5,1])
Block_Switch.place([0,26])

#SBLOCK
SEC1 = S_SEC1(Top,BlockIsland,[5,1])
SEC1.place([0,7])

SBuff = S_Buffer(Top,BlockIsland,[5,1])
SBuff.place([0,8])

SPACEUP_0 = S_spaceUP(Top,BlockIsland,[4,1])
SPACEUP_0.place([0,9])

Conn_1 = S_Conn12(Top,BlockIsland)
Conn_1.place([4,9])
Conn_1.markAbut()

SpaceUp_0 = S_spaceUP(Top,BlockIsland,[3,1])
SpaceUp_0.place([0,10])

Conn_2 = S_Conn12(Top,BlockIsland)
Conn_2.place([3,10])
Conn_2.markAbut()

SpaceDown_0 = S_spaceDOWN(Top,BlockIsland)
SpaceDown_0.place([4,10])
SpaceDown_0.markAbut()

SpaceUp_1 = S_spaceUP(Top,BlockIsland,[2,1])
SpaceUp_1.place([0,11])

Conn_3 = S_Conn12(Top,BlockIsland)
Conn_3.place([2,11])
Conn_3.markAbut()

SpaceDown_1 = S_spaceDOWN(Top,BlockIsland,[2,1])
SpaceDown_1.place([3,11])

SpaceUp_2 = S_spaceUP(Top,BlockIsland)
SpaceUp_2.markAbut()
SpaceUp_2.place([0,12])

Conn_4 = S_Conn12(Top,BlockIsland)
Conn_4.markAbut()
Conn_4.place([1,12])

SpaceDown_2 = S_spaceDOWN(Top,BlockIsland,[3,1])
SpaceDown_2.place([2,12])

Conn_4 = S_Conn12(Top,BlockIsland)
Conn_4.markAbut()
Conn_4.place([0,13])

SpaceDown_3 = S_spaceDOWN(Top,BlockIsland,[4,1])
SpaceDown_3.place([1,13])

SEC2 = S_SEC2(Top,BlockIsland,[5,1])
SEC2.place([0,14])

Conn_5 = S_Conn23(Top,BlockIsland,[5,1])
Conn_5.place([0,15])

SEC3 = S_SEC3(Top,BlockIsland,[5,1])
SEC3.place([0,16])


# Decoders
Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=6)
Block_GateSwitch = STD_IndirectGateSwitch(Top,island=BlockIsland,num=26)

Block_DrainDecode = STD_DrainDecoder(Top,island=BlockIsland,bits=5)
Block_DrainSelect = STD_DrainSelect(Top,island=BlockIsland,num=5)
Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num=5)

for i in range(8,16):
    ERASE_IndirectGateSwitch(Top,island=BlockIsland,col=i)

# CAB
# -------------------------------------------------------------------------------
CABIsland = Island(Top)

# A matrix
Atop = BlockTop(Top,CABIsland,[1,8])
Atop.place([0,0])
Amatrix = IndirectVMM(Top,[28,16],island=CABIsland,decoderPlace=False,loc=[1,0])

# B matrix
Btop = BlockTop(Top,CABIsland,[1,9])
Btop.place([0,8])
Bmatrix = IndirectVMM(Top,[24,18],island=CABIsland,decoderPlace=False,loc=[1,8])
Bbot = B_bot(Top,CABIsland,[1,9])
Bbot.place([7,8])

Bswitch = ST_BMatrix(Top,CABIsland,[8,1])
Bswitch.place([0,17])

BtoOut = OutSwitch(Top,CABIsland,[1,9])
BtoOut.place([9,8])

# Output Matrix
Outmatrix = IndirectVMM(Top,[8,18],island=CABIsland,decoderPlace=False,loc=[10,8])
Oswitch = ST_BMatrix(Top,CABIsland,[2,1])
Oswitch.place([10,17])

# CAB Elements
TA_Weak0 = TSMC350nm_TA2Cell_Weak(Top,CABIsland)
TA_Weak0.place([2,18])
TA_Weak0.markCABDevice()

TA_Weak1 = TSMC350nm_TA2Cell_Weak(Top,CABIsland)
TA_Weak1.place([3,18])
TA_Weak1.markCABDevice()

TA_Strong = TSMC350nm_TA2Cell_Strong(Top,CABIsland)
TA_Strong.place([4,18])
TA_Strong.markCABDevice()

WTA = TSMC350nm_4WTA(Top,CABIsland)
WTA.place([5,18])
WTA.markCABDevice()

CapBank = TSMC350nm_Cap_Bank(Top,CABIsland)
CapBank.place([6,18])
CapBank.markCABDevice()

FETs = TSMC350nm_NandPfets(Top,CABIsland)
FETs.place([7,18])
FETs.markCABDevice()

Nmirror = TSMC350nm_TGate_2nMirror(Top,CABIsland)
Nmirror.place([8,18])
Nmirror.markCABDevice()

# Decoders
CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=6)
CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num=12)
CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num=12)

CAB_GateSwitch = STD_GorS_IndirectSwitches(Top,CABIsland,num=19)
ERASE_IndirectGateSwitch(Top,CABIsland,col=17)
CABElements_GateSwitch = STD_IndirectGateSwitch(Top,CABIsland,col=18)

# Bmatrix <--> CAB Elements Connections
# -------------------------------------------------------------------------------

TA_Weak0.VD_P += Bswitch.P[0:2]
TA_Weak0.VIN1_MINUS += Bswitch.A[0]
TA_Weak0.VIN1_PLUS += Bswitch.A[1]
TA_Weak0.VIN2_PLUS += Bswitch.A[2]
TA_Weak0.VIN2_MINUS += Bswitch.A[3]

TA_Weak1.VD_P += Bswitch.P[4:6]
TA_Weak1.VIN1_MINUS += Bswitch.A[4]
TA_Weak1.VIN1_PLUS += Bswitch.A[5]
TA_Weak1.VIN2_PLUS += Bswitch.A[6]
TA_Weak1.VIN2_MINUS += Bswitch.A[7]

# Need new WTA Indirect block
WTA.Iin  += Bswitch.A[8:12]

CapBank.VD_P += Bswitch.P[12:16]
CapBank.VIN += Bswitch.A[12:14]

FETs.GATE_N += Bswitch.A[14]
FETs.SOURCE_N += Bswitch.A[15]
FETs.GATE_P += Bswitch.A[16]
FETs.SOURCE_P += Bswitch.A[17]

Nmirror.IN_CM += Bswitch.A[18:20]
Nmirror.SelN += Bswitch.A[20]
Nmirror.IN_TG += Bswitch.A[21]


# Feedback Connections
# -------------------------------------------------------------------------------
TA_Weak0.OUTPUT += CAB_GateSwitch.In[17:19]
TA_Weak1.OUTPUT += CAB_GateSwitch.In[19:21]
TA_Strong.OUTPUT += CAB_GateSwitch.In[21:23]
WTA.Vout += CAB_GateSwitch.In[23:27]
CapBank.OUT += CAB_GateSwitch.In[27:29]
FETs.DRAIN_P += CAB_GateSwitch.In[29]
FETs.DRAIN_N += CAB_GateSwitch.In[30]
Nmirror.OUT_CM += CAB_GateSwitch.In[31:33]
Nmirror.OUT_TG += CAB_GateSwitch.In[33]

# Power Connections

# Frame
# -------------------------------------------------------------------------------
outerFrame = frame(Top)
outerFrame.createPort("N","testPin",connection = CAB_GateSwitch.In[16])

# Compilation
#-------------------------------------------------------------------------------
design_limits = [1e6, 6.1e5]
location_islands = ((20600, 363500), (20600, 20000)) #<-location for tile v1
#location_islands=None


compile_asic(Top,process="TSMC350nm",fileName="full_cab_python",p_and_r = True,design_limits = design_limits, location_islands = location_islands)

