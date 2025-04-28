import ashes_fg as af
from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *

Top = Circuit()

# C,S,C Blocks
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

SpaceUp_0 = S_spaceUP(Top,BlockIsland,[4,1])
SpaceUp_0.place([0,9])
Conn_0 = S_Conn12(Top,BlockIsland)
Conn_0.place([4,9])
Conn_0.markAbut()

SpaceUp_1 = S_spaceUP(Top,BlockIsland,[3,1])
SpaceUp_1.place([0,10])
Conn_1 = S_Conn12(Top,BlockIsland)
Conn_1.place([3,10])
Conn_1.markAbut()

SpaceDown_1 = S_spaceDOWN(Top,BlockIsland,[1,1])
SpaceDown_1.place([4,10])
SpaceDown_1.markAbut()

SpaceUp_2 = S_spaceUP(Top,BlockIsland,[2,1])
SpaceUp_2.place([0,11])
Conn_2 = S_Conn12(Top,BlockIsland)
Conn_2.place([2,11])
Conn_2.markAbut()

SpaceDown_2 = S_spaceDOWN(Top,BlockIsland,[2,1])
SpaceDown_2.place([3,11])
SpaceUp_3 = S_spaceUP(Top,BlockIsland,[1,1])
SpaceUp_3.place([0,12])
SpaceUp_3.markAbut()

Conn_3 = S_Conn12(Top,BlockIsland)
Conn_3.place([1,12])
Conn_3.markAbut()

SpaceDown_3 = S_spaceDOWN(Top,BlockIsland,[3,1])
SpaceDown_3.place([2,12])
Conn_4 = S_Conn12(Top,BlockIsland)
Conn_4.place([0,13])
Conn_4.markAbut()

SpaceDown_4 = S_spaceDOWN(Top,BlockIsland,[4,1])
SpaceDown_4.place([1,13])
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
Block_DrainSelect = RunDrainSwitch(Top,island=BlockIsland,num=5)
Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num=5)
for i in range(8,14):
	ERASE_IndirectGateSwitch(Top,island=BlockIsland,col=i)
ERASE_IndirectGateSwitch(Top,island=BlockIsland,col=15)

# CAB
CABIsland = Island(Top)

# A matrix
Atop = BlockTop(Top,CABIsland,[1,8])
Atop.place([0,0])
Amatrix = IndirectVMM(Top,[28,16],island=CABIsland,decoderPlace=False,loc=[1,0])

# B matrix
Btop = BlockTop(Top,CABIsland,[1,10])
Btop.place([0,8])
Bmatrix = IndirectVMM(Top,[24,20],island=CABIsland,decoderPlace=False,loc=[1,8])
Bbot = B_bot(Top,CABIsland,[1,10])
Bbot.place([7,8])

Bswitch0 = ST_BMatrix(Top,CABIsland)
Bswitch0.place([0,18])
Bswitch0.markAbut()

Bswitch1 = ST_BMatrix(Top,CABIsland)
Bswitch1.place([1,18])
Bswitch1.markAbut()

Bswitch2 = ST_BMatrix(Top,CABIsland)
Bswitch2.place([2,18])
Bswitch2.markAbut()

Bswitch3 = ST_BMatrix_NoSwitch(Top,CABIsland)
Bswitch3.place([3,18])
Bswitch3.markAbut()

Bswitch4 = ST_BMatrix(Top,CABIsland)
Bswitch4.place([4,18])
Bswitch4.markAbut()

Bswitch5 = ST_BMatrix(Top,CABIsland)
Bswitch5.place([5,18])
Bswitch5.markAbut()

Bswitch6 = ST_BMatrix(Top,CABIsland)
Bswitch6.place([6,18])
Bswitch6.markAbut()

Bswitch7 = ST_BMatrix(Top,CABIsland)
Bswitch7.place([7,18])
Bswitch7.markAbut()

BtoOut = OutSwitch(Top,CABIsland,[1,10])
BtoOut.place([9,8])

# Output Matrix
Outmatrix = IndirectVMM(Top,[8,20],island=CABIsland,decoderPlace=False,loc=[10,8])
Oswitch = ST_BMatrix(Top,CABIsland,[2,1])
Oswitch.place([10,18])

# CAB Elements
TA2Cell_Weak__0 = TSMC350nm_TA2Cell_Weak(Top,CABIsland)
TA2Cell_Weak__0.place([2,19])
TA2Cell_Weak__0.markCABDevice()

TA2Cell_Weak__1 = TSMC350nm_TA2Cell_Weak(Top,CABIsland)
TA2Cell_Weak__1.place([3,19])
TA2Cell_Weak__1.markCABDevice()

TA2Cell_Strong = TSMC350nm_TA2Cell_Strong(Top,CABIsland)
TA2Cell_Strong.place([4,19])
TA2Cell_Strong.markCABDevice()

WTA_IndirectProg = TSMC350nm_4WTA_IndirectProg(Top,CABIsland)
WTA_IndirectProg.place([5,19])
WTA_IndirectProg.markCABDevice()

Cap_Bank = TSMC350nm_Cap_Bank(Top,CABIsland)
Cap_Bank.place([6,19])
Cap_Bank.markCABDevice()

NandPfets = TSMC350nm_NandPfets(Top,CABIsland)
NandPfets.place([7,19])
NandPfets.markCABDevice()

TGate_2nMirror = TSMC350nm_TGate_2nMirror(Top,CABIsland)
TGate_2nMirror.place([8,19])
TGate_2nMirror.markCABDevice()

VolSwitchIsland = Island(Top)

VolSwitch = TSMC350nm_volatile_swcs(Top,VolSwitchIsland,[1,6])
VolSwitch.place([0,0])

# Decoders
CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=6)
CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num=12)
CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num=12)

CAB_GateSwitch = STD_GorS_IndirectSwitches(Top,CABIsland,num=20)
ERASE_IndirectGateSwitch(Top,CABIsland,col=18)
CABElements_GateSwitch = STD_IndirectGateSwitch(Top,CABIsland,col=19)

# Bmatrix <--> CAB Elements Connections


TA2Cell_Weak__0.VD_P += Bswitch0.P[0:2]
TA2Cell_Weak__0.VIN1_PLUS += Bswitch0.A[0]
TA2Cell_Weak__0.VIN1_MINUS += Bswitch0.A[1]
TA2Cell_Weak__0.VIN2_PLUS += Bswitch0.A[2]
TA2Cell_Weak__0.VIN2_MINUS += Bswitch0.A[3]
TA2Cell_Weak__0.OUTPUT += CAB_GateSwitch.Input[17:19]
TA2Cell_Weak__0.Vsel += CABElements_GateSwitch.CTRL_B[0:2]
TA2Cell_Weak__0.RUN += CABElements_GateSwitch.run_r
TA2Cell_Weak__0.Vg += CABElements_GateSwitch.Vg[0:2]
TA2Cell_Weak__0.PROG += CABElements_GateSwitch.prog_r
TA2Cell_Weak__0.VTUN += CABElements_GateSwitch.VTUN
TA2Cell_Weak__0.VINJ += CABElements_GateSwitch.VINJ
TA2Cell_Weak__0.GND += CABElements_GateSwitch.GND[0]
TA2Cell_Weak__0.VPWR += CABElements_GateSwitch.VDD[1]

TA2Cell_Weak__1.VD_P += Bswitch1.P[0:2]
TA2Cell_Weak__1.VIN1_PLUS += Bswitch1.A[0]
TA2Cell_Weak__1.VIN1_MINUS += Bswitch1.A[1]
TA2Cell_Weak__1.VIN2_PLUS += Bswitch1.A[2]
TA2Cell_Weak__1.VIN2_MINUS += Bswitch1.A[3]
TA2Cell_Weak__1.OUTPUT += CAB_GateSwitch.Input[19:21]
TA2Cell_Weak__1.Vsel += TA2Cell_Weak__0.Vsel_b[0:2]
TA2Cell_Weak__1.RUN += TA2Cell_Weak__0.RUN_b
TA2Cell_Weak__1.Vg += TA2Cell_Weak__0.Vg_b[0:2]
TA2Cell_Weak__1.PROG += TA2Cell_Weak__0.PROG_b
TA2Cell_Weak__1.VTUN += TA2Cell_Weak__0.VTUN_b
TA2Cell_Weak__1.VINJ += TA2Cell_Weak__0.VINJ_b
TA2Cell_Weak__1.GND += TA2Cell_Weak__0.GND_b
TA2Cell_Weak__1.VPWR += TA2Cell_Weak__0.VPWR_b

TA2Cell_Strong.VD_P += Bswitch2.P[0:2]
TA2Cell_Strong.VIN1_PLUS += Bswitch2.A[0]
TA2Cell_Strong.VIN1_MINUS += Bswitch2.A[1]
TA2Cell_Strong.VIN2_PLUS += Bswitch2.A[2]
TA2Cell_Strong.VIN2_MINUS += Bswitch2.A[3]
TA2Cell_Strong.OUTPUT += CAB_GateSwitch.Input[21:23]
TA2Cell_Strong.Vsel += TA2Cell_Weak__1.Vsel_b[0:2]
TA2Cell_Strong.RUN += TA2Cell_Weak__1.RUN_b
TA2Cell_Strong.Vg += TA2Cell_Weak__1.Vg_b[0:2]
TA2Cell_Strong.PROG += TA2Cell_Weak__1.PROG_b
TA2Cell_Strong.VTUN += TA2Cell_Weak__1.VTUN_b
TA2Cell_Strong.VINJ += TA2Cell_Weak__1.VINJ_b
TA2Cell_Strong.GND += TA2Cell_Weak__1.GND_b
TA2Cell_Strong.VPWR += TA2Cell_Weak__1.VPWR_b

WTA_IndirectProg.VD_P += Bswitch3.P[0:4]
WTA_IndirectProg.Iin += Bswitch3.A[0:4]
WTA_IndirectProg.Vout += CAB_GateSwitch.Input[23:27]
WTA_IndirectProg.Vmid += CAB_GateSwitch.Input[27]
WTA_IndirectProg.Vbias += CAB_GateSwitch.Input[28]
WTA_IndirectProg.Vsel += CABElements_GateSwitch.CTRL_B[0]
WTA_IndirectProg.Vs += CABElements_GateSwitch.VDD[1]
WTA_IndirectProg.VINJ += TA2Cell_Strong.VINJ_b
WTA_IndirectProg.Vg += TA2Cell_Strong.Vg_b[0]
WTA_IndirectProg.VTUN += TA2Cell_Strong.VTUN_b
WTA_IndirectProg.GND += TA2Cell_Strong.GND_b
WTA_IndirectProg.PROG += TA2Cell_Strong.PROG_b

Cap_Bank.VD_P += Bswitch4.P[0:4]
Cap_Bank.VIN += Bswitch4.A[0:2]
Cap_Bank.OUT += CAB_GateSwitch.Input[29:31]
Cap_Bank.VINJ += WTA_IndirectProg.VINJ_b
Cap_Bank.Vsel += CABElements_GateSwitch.CTRL_B[0:2]
Cap_Bank.Vg += CABElements_GateSwitch.Vg[0:2]
Cap_Bank.GND += WTA_IndirectProg.GND_b
Cap_Bank.VTUN += WTA_IndirectProg.VTUN_b

NandPfets.GATE_N += Bswitch5.A[0]
NandPfets.SOURCE_N += Bswitch5.A[1]
NandPfets.GATE_P += Bswitch5.A[2]
NandPfets.SOURCE_P += Bswitch5.A[3]
NandPfets.DRAIN_N += CAB_GateSwitch.Input[31]
NandPfets.DRAIN_P += CAB_GateSwitch.Input[32]
NandPfets.VPWR += CABElements_GateSwitch.VDD[1]
NandPfets.GND += Cap_Bank.GND_b

TGate_2nMirror.IN_CM += Bswitch6.A[0:2]
TGate_2nMirror.SelN += Bswitch6.A[2]
TGate_2nMirror.IN_TG += Bswitch6.A[3]
TGate_2nMirror.OUT_CM += CAB_GateSwitch.Input[33:35]
TGate_2nMirror.OUT_TG += CAB_GateSwitch.Input[35]
TGate_2nMirror.VPWR += NandPfets.VPWR_b
TGate_2nMirror.GND += NandPfets.GND_b

C_EW.Vsel_b += CAB_GateSwitch.Vsel[0:14]
C_EW.Vg_b += CAB_GateSwitch.Vg_global[0:14]
C_EW.VTUN_b += CAB_GateSwitch.VTUN[0:7]
C_EW.GND_b[1] += CAB_GateSwitch.GND[0]
C_EW.GND_b[3] += CAB_GateSwitch.GND[1]
C_EW.GND_b[5] += CAB_GateSwitch.GND[2]
C_EW.GND_b[7] += CAB_GateSwitch.GND[3]
C_EW.GND_b[9] += CAB_GateSwitch.GND[4]
C_EW.GND_b[11] += CAB_GateSwitch.GND[5]
C_EW.GND_b[13] += CAB_GateSwitch.GND[6]
CAB_GateSwitch.Input[1] += CAB_GateSwitch.GND[0]
C_EW.VINJ_b[1] += CAB_GateSwitch.VINJ[0]
C_EW.VINJ_b[3] += CAB_GateSwitch.VINJ[1]
C_EW.VINJ_b[5] += CAB_GateSwitch.VINJ[2]
C_EW.VINJ_b[7] += CAB_GateSwitch.VINJ[3]
C_EW.VINJ_b[9] += CAB_GateSwitch.VINJ[4]
C_EW.VINJ_b[11] += CAB_GateSwitch.VINJ[5]
C_EW.VINJ_b[13] += CAB_GateSwitch.VINJ[6]
C_EW.Vs_b[2] += CAB_GateSwitch.Input[2]
C_EW.Vs_b[3] += CAB_GateSwitch.Input[3]
C_EW.Vs_b[4] += CAB_GateSwitch.Input[4]
C_EW.Vs_b[5] += CAB_GateSwitch.Input[5]
C_EW.Vs_b[6] += CAB_GateSwitch.Input[6]
C_EW.Vs_b[7] += CAB_GateSwitch.Input[7]
SEC1.VINJ_b += CAB_GateSwitch.VINJ[7]
SEC1.Vsel_b += CAB_GateSwitch.Vsel[14:16]
SEC1.Vg_b += CAB_GateSwitch.Vg_global[14:16]
SEC1.VTUN_b += CAB_GateSwitch.VTUN[7]
SEC1.GND_b[1] += CAB_GateSwitch.GND[7]

# Compilation
design_limits = [1e6, 6.1e5]
location_islands = ((20600, 363500), (20600, 20000), (160000,20000))
compile_asic(Top,process="TSMC350nm",fileName="full_cab_python",p_and_r = True,design_limits = design_limits, location_islands = location_islands)

