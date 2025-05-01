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

TA2Cell_Strong__0 = TSMC350nm_TA2Cell_Strong(Top,CABIsland)
TA2Cell_Strong__0.place([4,19])
TA2Cell_Strong__0.markCABDevice()

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

TA2Cell_Strong__0.VD_P += Bswitch2.P[0:2]
TA2Cell_Strong__0.VIN1_PLUS += Bswitch2.A[0]
TA2Cell_Strong__0.VIN1_MINUS += Bswitch2.A[1]
TA2Cell_Strong__0.VIN2_PLUS += Bswitch2.A[2]
TA2Cell_Strong__0.VIN2_MINUS += Bswitch2.A[3]
TA2Cell_Strong__0.OUTPUT += CAB_GateSwitch.Input[21:23]
TA2Cell_Strong__0.Vsel += TA2Cell_Weak__1.Vsel_b[0:2]
TA2Cell_Strong__0.RUN += TA2Cell_Weak__1.RUN_b
TA2Cell_Strong__0.Vg += TA2Cell_Weak__1.Vg_b[0:2]
TA2Cell_Strong__0.PROG += TA2Cell_Weak__1.PROG_b
TA2Cell_Strong__0.VTUN += TA2Cell_Weak__1.VTUN_b
TA2Cell_Strong__0.VINJ += TA2Cell_Weak__1.VINJ_b
TA2Cell_Strong__0.GND += TA2Cell_Weak__1.GND_b
TA2Cell_Strong__0.VPWR += TA2Cell_Weak__1.VPWR_b

WTA_IndirectProg.VD_P += Bswitch3.P[0:4]
WTA_IndirectProg.Iin += Bswitch3.A[0:4]
WTA_IndirectProg.Vout += CAB_GateSwitch.Input[23:27]
WTA_IndirectProg.Vmid += CAB_GateSwitch.Input[27]
WTA_IndirectProg.Vbias += CAB_GateSwitch.Input[28]
WTA_IndirectProg.Vsel += CABElements_GateSwitch.CTRL_B[0]
WTA_IndirectProg.Vs += CABElements_GateSwitch.VDD[1]
WTA_IndirectProg.VINJ += TA2Cell_Strong__0.VINJ_b
WTA_IndirectProg.Vg += TA2Cell_Strong__0.Vg_b[0]
WTA_IndirectProg.VTUN += TA2Cell_Strong__0.VTUN_b
WTA_IndirectProg.GND += TA2Cell_Strong__0.GND_b
WTA_IndirectProg.PROG += TA2Cell_Strong__0.PROG_b

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

CAB_GateSwitch.Input[0] += CABElements_GateSwitch.VPWR[0]
CABElements_GateSwitch.VPWR[1] += CABElements_GateSwitch.VPWR[0]
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
CAB_GateSwitch.GND[0] += CAB_GateSwitch.Input[1]
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
SEC1.VTUN_b += CAB_GateSwitch.VTUN[7]
SEC1.GND_b[1] += CAB_GateSwitch.GND[7]
SEC1.Vsel_b[0] += CAB_GateSwitch.Vsel[15]
SEC1.Vsel_b[1] += CAB_GateSwitch.Vsel[14]
SEC1.Vg_b[0] += CAB_GateSwitch.Vg_global[15]
SEC1.Vg_b[1] += CAB_GateSwitch.Vg_global[14]
SEC2.VINJ_b += CAB_GateSwitch.VINJ[8]
SEC2.VTUN_b += CAB_GateSwitch.VTUN[8]
SEC2.GND_b[1] += CAB_GateSwitch.GND[8]
SEC2.Vsel_b[0] += CAB_GateSwitch.Vsel[17]
SEC2.Vsel_b[1] += CAB_GateSwitch.Vsel[16]
SEC2.Vg_b[0] += CAB_GateSwitch.Vg_global[17]
SEC2.Vg_b[1] += CAB_GateSwitch.Vg_global[16]
SEC3.VINJ_b += CAB_GateSwitch.VINJ[9]
SEC3.VTUN_b += CAB_GateSwitch.VTUN[9]
SEC3.GND_b[1] += CAB_GateSwitch.GND[9]
SEC3.Vsel_b[0] += CAB_GateSwitch.Vsel[19]
SEC3.Vsel_b[1] += CAB_GateSwitch.Vsel[18]
SEC3.Vg_b[0] += CAB_GateSwitch.Vg_global[19]
SEC3.Vg_b[1] += CAB_GateSwitch.Vg_global[18]
C_NS.VTUN_b[0] += CAB_GateSwitch.VTUN[10]
C_NS.VINJ_b[1] += CAB_GateSwitch.VINJ[10]
C_NS.GND_b[1] += CAB_GateSwitch.GND[10]
C_NS.Vsel_b[0] += CAB_GateSwitch.Vsel[20]
C_NS.Vg_b[0] += CAB_GateSwitch.Vg_global[20]
C_NS.Vsel_b[1] += CAB_GateSwitch.Vsel[21]
C_NS.Vg_b[1] += CAB_GateSwitch.Vg_global[21]
C_NS.VTUN_b[1] += CAB_GateSwitch.VTUN[11]
C_NS.VINJ_b[3] += CAB_GateSwitch.VINJ[11]
C_NS.GND_b[3] += CAB_GateSwitch.GND[11]
C_NS.Vsel_b[2] += CAB_GateSwitch.Vsel[22]
C_NS.Vg_b[2] += CAB_GateSwitch.Vg_global[22]
C_NS.Vsel_b[3] += CAB_GateSwitch.Vsel[23]
C_NS.Vg_b[3] += CAB_GateSwitch.Vg_global[23]
C_NS.VTUN_b[2] += CAB_GateSwitch.VTUN[12]
C_NS.VINJ_b[5] += CAB_GateSwitch.VINJ[12]
C_NS.GND_b[5] += CAB_GateSwitch.GND[12]
C_NS.Vsel_b[4] += CAB_GateSwitch.Vsel[24]
C_NS.Vg_b[4] += CAB_GateSwitch.Vg_global[24]
C_NS.Vsel_b[5] += CAB_GateSwitch.Vsel[25]
C_NS.Vg_b[5] += CAB_GateSwitch.Vg_global[25]
C_NS.VTUN_b[3] += CAB_GateSwitch.VTUN[13]
C_NS.VINJ_b[7] += CAB_GateSwitch.VINJ[13]
C_NS.GND_b[7] += CAB_GateSwitch.GND[13]
C_NS.Vsel_b[6] += CAB_GateSwitch.Vsel[26]
C_NS.Vg_b[6] += CAB_GateSwitch.Vg_global[26]
C_NS.Vsel_b[7] += CAB_GateSwitch.Vsel[27]
C_NS.Vg_b[7] += CAB_GateSwitch.Vg_global[27]
C_NS.VTUN_b[4] += CAB_GateSwitch.VTUN[14]
C_NS.VINJ_b[9] += CAB_GateSwitch.VINJ[14]
C_NS.GND_b[9] += CAB_GateSwitch.GND[14]
C_NS.Vsel_b[8] += CAB_GateSwitch.Vsel[28]
C_NS.Vg_b[8] += CAB_GateSwitch.Vg_global[28]
C_NS.Vsel_b[9] += CAB_GateSwitch.Vsel[29]
C_NS.Vg_b[9] += CAB_GateSwitch.Vg_global[29]
C_NS.VTUN_b[5] += CAB_GateSwitch.VTUN[15]
C_NS.VINJ_b[11] += CAB_GateSwitch.VINJ[15]
C_NS.GND_b[11] += CAB_GateSwitch.GND[15]
C_NS.Vsel_b[10] += CAB_GateSwitch.Vsel[30]
C_NS.Vg_b[10] += CAB_GateSwitch.Vg_global[30]
C_NS.Vsel_b[11] += CAB_GateSwitch.Vsel[31]
C_NS.Vg_b[11] += CAB_GateSwitch.Vg_global[31]
C_NS.VTUN_b[6] += CAB_GateSwitch.VTUN[16]
C_NS.VINJ_b[13] += CAB_GateSwitch.VINJ[16]
C_NS.GND_b[13] += CAB_GateSwitch.GND[16]
C_NS.Vsel_b[12] += CAB_GateSwitch.Vsel[32]
C_NS.Vg_b[12] += CAB_GateSwitch.Vg_global[32]
C_NS.Vsel_b[13] += CAB_GateSwitch.Vsel[33]
C_NS.Vg_b[13] += CAB_GateSwitch.Vg_global[33]
C_NS.VTUN_b[7] += CAB_GateSwitch.VTUN[17]
C_NS.VINJ_b[15] += CAB_GateSwitch.VINJ[17]
C_NS.GND_b[15] += CAB_GateSwitch.GND[17]
C_NS.Vsel_b[14] += CAB_GateSwitch.Vsel[34]
C_NS.Vg_b[14] += CAB_GateSwitch.Vg_global[34]
C_NS.Vsel_b[15] += CAB_GateSwitch.Vsel[35]
C_NS.Vg_b[15] += CAB_GateSwitch.Vg_global[35]
C_NS.VTUN_b[8] += CAB_GateSwitch.VTUN[18]
C_NS.VINJ_b[17] += CAB_GateSwitch.VINJ[18]
C_NS.GND_b[17] += CAB_GateSwitch.GND[18]
C_NS.Vsel_b[16] += CAB_GateSwitch.Vsel[36]
C_NS.Vg_b[16] += CAB_GateSwitch.Vg_global[36]
C_NS.Vsel_b[17] += CAB_GateSwitch.Vsel[37]
C_NS.Vg_b[17] += CAB_GateSwitch.Vg_global[37]
C_NS.Vs_b[0] += CAB_GateSwitch.Input[8]
C_NS.Vs_b[1] += CAB_GateSwitch.Input[9]
C_NS.Vs_b[2] += CAB_GateSwitch.Input[10]
C_NS.Vs_b[3] += CAB_GateSwitch.Input[11]
C_NS.Vs_b[4] += CAB_GateSwitch.Input[12]
C_NS.Vs_b[5] += CAB_GateSwitch.Input[13]
C_NS.Vs_b[6] += CAB_GateSwitch.Input[14]
C_NS.Vs_b[7] += CAB_GateSwitch.Input[15]
C_NS.Vsel_b[16] += CABElements_GateSwitch.decode[0]
C_NS.VTUN_b[8] += CABElements_GateSwitch.VTUN_T
C_NS.GND_b[17] += CABElements_GateSwitch.GND_T
C_NS.Vsel_b[17] += CABElements_GateSwitch.decode[1]
C_NS.VINJ_b[17] += CABElements_GateSwitch.VINJ_T
Block_GateDecode.VINJ_b[0] += Block_GateSwitch.VINJ_T[0]
Block_GateDecode.GND_b[0] += Block_GateSwitch.GND_T[0]
Block_GateDecode.OUT[0] += Block_GateSwitch.decode[0]
Block_GateDecode.OUT[1] += Block_GateSwitch.decode[1]
Block_GateDecode.RUN_OUT[0] += Block_GateSwitch.VPWR[0]
Block_GateDecode.RUN_OUT[1] += Block_GateSwitch.VPWR[1]
Block_GateDecode.VINJ_b[1] += Block_GateSwitch.VINJ_T[1]
Block_GateDecode.GND_b[1] += Block_GateSwitch.GND_T[1]
Block_GateDecode.OUT[2] += Block_GateSwitch.decode[2]
Block_GateDecode.OUT[3] += Block_GateSwitch.decode[3]
Block_GateDecode.RUN_OUT[2] += Block_GateSwitch.VPWR[2]
Block_GateDecode.RUN_OUT[3] += Block_GateSwitch.VPWR[3]
Block_GateDecode.VINJ_b[2] += Block_GateSwitch.VINJ_T[2]
Block_GateDecode.GND_b[2] += Block_GateSwitch.GND_T[2]
Block_GateDecode.OUT[4] += Block_GateSwitch.decode[4]
Block_GateDecode.OUT[5] += Block_GateSwitch.decode[5]
Block_GateDecode.RUN_OUT[4] += Block_GateSwitch.VPWR[4]
Block_GateDecode.RUN_OUT[5] += Block_GateSwitch.VPWR[5]
Block_GateDecode.VINJ_b[3] += Block_GateSwitch.VINJ_T[3]
Block_GateDecode.GND_b[3] += Block_GateSwitch.GND_T[3]
Block_GateDecode.OUT[6] += Block_GateSwitch.decode[6]
Block_GateDecode.OUT[7] += Block_GateSwitch.decode[7]
Block_GateDecode.RUN_OUT[6] += Block_GateSwitch.VPWR[6]
Block_GateDecode.RUN_OUT[7] += Block_GateSwitch.VPWR[7]
Block_GateDecode.VINJ_b[4] += Block_GateSwitch.VINJ_T[4]
Block_GateDecode.GND_b[4] += Block_GateSwitch.GND_T[4]
Block_GateDecode.OUT[8] += Block_GateSwitch.decode[8]
Block_GateDecode.OUT[9] += Block_GateSwitch.decode[9]
Block_GateDecode.RUN_OUT[8] += Block_GateSwitch.VPWR[8]
Block_GateDecode.RUN_OUT[9] += Block_GateSwitch.VPWR[9]
Block_GateDecode.VINJ_b[5] += Block_GateSwitch.VINJ_T[5]
Block_GateDecode.GND_b[5] += Block_GateSwitch.GND_T[5]
Block_GateDecode.OUT[10] += Block_GateSwitch.decode[10]
Block_GateDecode.OUT[11] += Block_GateSwitch.decode[11]
Block_GateDecode.RUN_OUT[10] += Block_GateSwitch.VPWR[10]
Block_GateDecode.RUN_OUT[11] += Block_GateSwitch.VPWR[11]
Block_GateDecode.VINJ_b[6] += Block_GateSwitch.VINJ_T[6]
Block_GateDecode.GND_b[6] += Block_GateSwitch.GND_T[6]
Block_GateDecode.OUT[12] += Block_GateSwitch.decode[12]
Block_GateDecode.OUT[13] += Block_GateSwitch.decode[13]
Block_GateDecode.RUN_OUT[12] += Block_GateSwitch.VPWR[12]
Block_GateDecode.RUN_OUT[13] += Block_GateSwitch.VPWR[13]
Block_GateDecode.VINJ_b[7] += Block_GateSwitch.VINJ_T[7]
Block_GateDecode.GND_b[7] += Block_GateSwitch.GND_T[7]
Block_GateDecode.OUT[14] += Block_GateSwitch.decode[14]
Block_GateDecode.OUT[15] += Block_GateSwitch.decode[15]
Block_GateDecode.RUN_OUT[14] += Block_GateSwitch.VPWR[14]
Block_GateDecode.RUN_OUT[15] += Block_GateSwitch.VPWR[15]
Block_GateDecode.VINJ_b[8] += Block_GateSwitch.VINJ_T[14]
Block_GateDecode.GND_b[8] += Block_GateSwitch.GND_T[14]
Block_GateDecode.OUT[16] += Block_GateSwitch.decode[28]
Block_GateDecode.OUT[17] += Block_GateSwitch.decode[29]
Block_GateDecode.VINJ_b[10] += Block_GateSwitch.VINJ_T[16]
Block_GateDecode.GND_b[10] += Block_GateSwitch.GND_T[16]
Block_GateDecode.OUT[20] += Block_GateSwitch.decode[32]
Block_GateDecode.OUT[21] += Block_GateSwitch.decode[33]
Block_GateDecode.VINJ_b[11] += Block_GateSwitch.VINJ_T[17]
Block_GateDecode.GND_b[11] += Block_GateSwitch.GND_T[17]
Block_GateDecode.OUT[22] += Block_GateSwitch.decode[34]
Block_GateDecode.OUT[23] += Block_GateSwitch.decode[35]
Block_GateDecode.VINJ_b[12] += Block_GateSwitch.VINJ_T[18]
Block_GateDecode.GND_b[12] += Block_GateSwitch.GND_T[18]
Block_GateDecode.OUT[24] += Block_GateSwitch.decode[36]
Block_GateDecode.OUT[25] += Block_GateSwitch.decode[37]
Block_GateDecode.VINJ_b[13] += Block_GateSwitch.VINJ_T[19]
Block_GateDecode.GND_b[13] += Block_GateSwitch.GND_T[19]
Block_GateDecode.OUT[26] += Block_GateSwitch.decode[38]
Block_GateDecode.OUT[27] += Block_GateSwitch.decode[39]
Block_GateDecode.VINJ_b[14] += Block_GateSwitch.VINJ_T[20]
Block_GateDecode.GND_b[14] += Block_GateSwitch.GND_T[20]
Block_GateDecode.OUT[28] += Block_GateSwitch.decode[40]
Block_GateDecode.OUT[29] += Block_GateSwitch.decode[41]
Block_GateDecode.VINJ_b[15] += Block_GateSwitch.VINJ_T[21]
Block_GateDecode.GND_b[15] += Block_GateSwitch.GND_T[21]
Block_GateDecode.OUT[30] += Block_GateSwitch.decode[42]
Block_GateDecode.OUT[31] += Block_GateSwitch.decode[43]
Block_GateDecode.VINJ_b[16] += Block_GateSwitch.VINJ_T[22]
Block_GateDecode.GND_b[16] += Block_GateSwitch.GND_T[22]
Block_GateDecode.OUT[32] += Block_GateSwitch.decode[44]
Block_GateDecode.OUT[33] += Block_GateSwitch.decode[45]
Block_GateDecode.VINJ_b[17] += Block_GateSwitch.VINJ_T[23]
Block_GateDecode.GND_b[17] += Block_GateSwitch.GND_T[23]
Block_GateDecode.OUT[34] += Block_GateSwitch.decode[46]
Block_GateDecode.OUT[35] += Block_GateSwitch.decode[47]
Block_GateDecode.VINJ_b[18] += Block_GateSwitch.VINJ_T[24]
Block_GateDecode.GND_b[18] += Block_GateSwitch.GND_T[24]
Block_GateDecode.OUT[36] += Block_GateSwitch.decode[48]
Block_GateDecode.OUT[37] += Block_GateSwitch.decode[49]
Block_GateDecode.VINJ_b[19] += Block_GateSwitch.VINJ_T[25]
Block_GateDecode.GND_b[19] += Block_GateSwitch.GND_T[25]
Block_GateDecode.OUT[38] += Block_GateSwitch.decode[50]
Block_GateDecode.OUT[39] += Block_GateSwitch.decode[51]

VolSwitch.out += Amatrix.Vs_b[0:12]
VolSwitch.VINJ += Amatrix.VINJ_b[0:12]
VolSwitch.Vsel += Amatrix.Vsel_b[0:12]
VolSwitch.Vg += Amatrix.Vg_b[0:12]
VolSwitch.GND += Amatrix.GND_b[0:6]
VolSwitch.VTUN += Amatrix.VTUN_b[0:6]
VolSwitch.D += C_EW.Vs_b[12]
VolSwitch.CLK += C_EW.Vs_b[13]
VolSwitch.Q += C_NS.Vs_b[13]
VolSwitch.com += CAB_GateSwitch.Input[16]
CABElements_GateSwitch.VDD[1] += VolSwitch.VDD
VolSwitch.Vd_P += CAB_DrainSwitch.PR[35]
VolSwitch.Vd_in[0] += CAB_DrainSwitch.In[32]
VolSwitch.Vd_in[4] += CAB_DrainSwitch.PR[32]
VolSwitch.Vd_o[0] += Outmatrix.Vd_Rl[0]
VolSwitch.Vd_o[4] += Outmatrix.Vd_Pl[0]
VolSwitch.Vd_in[1] += CAB_DrainSwitch.In[33]
VolSwitch.Vd_in[5] += CAB_DrainSwitch.PR[33]
VolSwitch.Vd_o[1] += Outmatrix.Vd_Rl[1]
VolSwitch.Vd_o[5] += Outmatrix.Vd_Pl[1]
VolSwitch.Vd_in[2] += CAB_DrainSwitch.In[34]
VolSwitch.Vd_in[6] += CAB_DrainSwitch.PR[34]
VolSwitch.Vd_o[2] += Outmatrix.Vd_Rl[2]
VolSwitch.Vd_o[6] += Outmatrix.Vd_Pl[2]
VolSwitch.Vd_in[3] += CAB_DrainSwitch.In[35]
VolSwitch.Vd_in[7] += CAB_DrainSwitch.PR[35]
VolSwitch.Vd_o[3] += Outmatrix.Vd_Rl[3]
VolSwitch.Vd_o[7] += Outmatrix.Vd_Pl[3]
CABElements_GateSwitch.VDD[1] += CAB_GateSwitch.AVDD_r
CABElements_GateSwitch.PROG += CAB_GateSwitch.prog_r
CABElements_GateSwitch.RUN += CAB_GateSwitch.run_r
CABElements_GateSwitch.prog_r += Block_Switch.Prog_b
Block_Switch.GND_b += CABElements_GateSwitch.GND_T
Block_Switch.VDD_b += CABElements_GateSwitch.VPWR[1]
Bswitch7.GND_b += CABElements_GateSwitch.GND_T
Bswitch7.VDD_b += CABElements_GateSwitch.VPWR[1]
Bswitch7.Prog_b += CABElements_GateSwitch.PROG
Oswitch.GND_b += CABElements_GateSwitch.GND_T
Oswitch.VDD_b += CABElements_GateSwitch.VPWR[1]
Oswitch.Prog_b += CABElements_GateSwitch.PROG
CABElements_GateSwitch.RUN_IN[1] += CAB_GateSwitch.Vgrun_r
CABElements_GateSwitch.RUN_IN[0] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[0] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[1] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[2] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[3] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[4] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[5] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[6] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[7] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[8] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[9] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[10] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[11] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[12] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[13] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[14] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[15] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[28] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[29] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[32] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[33] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[34] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[35] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[36] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[37] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[38] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[39] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[40] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[41] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[42] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[43] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[44] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[45] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[46] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[47] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[48] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[49] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[50] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[51] += CAB_GateSwitch.Vgrun_r

outerFrame = frame(Top)
outerFrame.createPort("N","gateEN",connection = Block_GateDecode.ENABLE)
outerFrame.createPort("N","programdrain",connection = Block_DrainSelect.prog_drainrail)
Block_DrainSelect.prog_drainrail += CAB_DrainSelect.prog_drainrail
outerFrame.createPort("N","rundrain",connection = Block_DrainSelect.run_drainrail)
Block_DrainSelect.run_drainrail += CAB_DrainSelect.run_drainrail
outerFrame.createPort("N","cew0",connection = Block_GateDecode.VGRUN[8])
outerFrame.createPort("N","cew1",connection = Block_GateDecode.VGRUN[9])
outerFrame.createPort("N","cew2",connection = Block_GateDecode.VGRUN[10])
outerFrame.createPort("N","cew3",connection = Block_GateDecode.VGRUN[11])
outerFrame.createPort("N","vtun",connection = Block_GateSwitch.VTUN_T[0])
VINJN = outerFrame.createPort("N","vinj",dimension=3)
VINJN[0] += Block_GateDecode.VINJV
VINJN[1] += Block_DrainSelect.VINJ
Block_DrainSelect.VINJ += Block_DrainCutoff.VDD
VINJN[2] += CABElements_GateSwitch.VINJ_T
GNDN = outerFrame.createPort("N","gnd",dimension=3)
GNDN[0] += Block_GateDecode.GNDV
GNDN[1] += Block_DrainSelect.GND
Block_DrainSelect.GND += Block_DrainCutoff.GND
GNDN[2] += CABElements_GateSwitch.GND_T
outerFrame.createPort("N","avdd",connection = CAB_GateSwitch.Input[0])
outerFrame.createPort("N","s0",connection = SpaceUp_0.n[0])
outerFrame.createPort("N","s1",connection = SpaceUp_0.n[1])
outerFrame.createPort("N","s2",connection = SpaceUp_0.n[2])
outerFrame.createPort("N","s3",connection = SpaceUp_0.n[3])
outerFrame.createPort("N","s4",connection = SpaceUp_1.n[0])
outerFrame.createPort("N","s5",connection = SpaceUp_1.n[1])
outerFrame.createPort("N","s6",connection = SpaceUp_1.n[2])
outerFrame.createPort("N","s7",connection = SpaceUp_1.n[3])
outerFrame.createPort("N","s8",connection = SpaceUp_2.n[0])
outerFrame.createPort("N","s9",connection = SpaceUp_2.n[1])
outerFrame.createPort("N","s10",connection = SpaceUp_2.n[2])
outerFrame.createPort("N","s11",connection = SpaceUp_2.n[3])
outerFrame.createPort("N","s12",connection = SpaceUp_3.n[0])
outerFrame.createPort("N","s13",connection = SpaceUp_3.n[1])
outerFrame.createPort("N","s14",connection = SpaceUp_3.n[2])
outerFrame.createPort("N","s15",connection = SpaceUp_3.n[3])
outerFrame.createPort("N","s16",connection = Conn_4.n[0])
outerFrame.createPort("N","s17",connection = Conn_4.n[1])
outerFrame.createPort("N","s18",connection = Conn_4.n[2])
outerFrame.createPort("N","s19",connection = Conn_4.n[3])
outerFrame.createPort("N","prog",connection = CABElements_GateSwitch.prog_r)
CABElements_GateSwitch.prog_r += Block_Switch.Prog
outerFrame.createPort("N","run",connection = Block_GateSwitch.RUN)
Block_GateSwitch.RUN += Block_DrainCutoff.RUN
Block_GateSwitch.RUN += CAB_GateSwitch.run
CAB_GateSwitch.run += CAB_DrainSwitch.RUN
outerFrame.createPort("N","vgsel",connection = CABElements_GateSwitch.Vgsel)
CABElements_GateSwitch.Vgsel += Block_GateSwitch.vgsel_r
outerFrame.createPort("S","gateEN",connection = Block_GateDecode.ENABLE)
outerFrame.createPort("S","programdrain",connection = Block_DrainSelect.prog_drainrail)
outerFrame.createPort("S","rundrain",connection = Block_DrainSelect.run_drainrail)
outerFrame.createPort("S","cew0",connection = Oswitch.A[0])
outerFrame.createPort("S","cew1",connection = Oswitch.A[1])
outerFrame.createPort("S","cew2",connection = Oswitch.A[2])
outerFrame.createPort("S","cew3",connection = Oswitch.A[3])
outerFrame.createPort("S","vtun",connection = Block_GateSwitch.VTUN_T[0])
VINJS = outerFrame.createPort("S","vinj",dimension=3)
VINJS[0] += Block_GateDecode.VINJV
VINJS[1] += Block_DrainSelect.VINJ
VINJS[2] += CABElements_GateSwitch.VINJ_T
GNDS = outerFrame.createPort("S","gnd",dimension=3)
GNDS[0] += Block_GateDecode.GNDV
GNDS[1] += Block_DrainSelect.GND
GNDS[2] += CABElements_GateSwitch.GND_T
outerFrame.createPort("S","avdd",connection = CAB_GateSwitch.Input[0])
outerFrame.createPort("S","s0",connection = Conn_0.s[0])
outerFrame.createPort("S","s1",connection = Conn_0.s[1])
outerFrame.createPort("S","s2",connection = Conn_0.s[2])
outerFrame.createPort("S","s3",connection = Conn_0.s[3])
outerFrame.createPort("S","s4",connection = SpaceDown_1.s[0])
outerFrame.createPort("S","s5",connection = SpaceDown_1.s[1])
outerFrame.createPort("S","s6",connection = SpaceDown_1.s[2])
outerFrame.createPort("S","s7",connection = SpaceDown_1.s[3])
outerFrame.createPort("S","s8",connection = SpaceDown_2.s[0])
outerFrame.createPort("S","s9",connection = SpaceDown_2.s[1])
outerFrame.createPort("S","s10",connection = SpaceDown_2.s[2])
outerFrame.createPort("S","s11",connection = SpaceDown_2.s[3])
outerFrame.createPort("S","s12",connection = SpaceDown_3.s[0])
outerFrame.createPort("S","s13",connection = SpaceDown_3.s[1])
outerFrame.createPort("S","s14",connection = SpaceDown_3.s[2])
outerFrame.createPort("S","s15",connection = SpaceDown_3.s[3])
outerFrame.createPort("S","s16",connection = SpaceDown_4.s[0])
outerFrame.createPort("S","s17",connection = SpaceDown_4.s[1])
outerFrame.createPort("S","s18",connection = SpaceDown_4.s[2])
outerFrame.createPort("S","s19",connection = SpaceDown_4.s[3])
outerFrame.createPort("S","prog",connection = CABElements_GateSwitch.prog_r)
outerFrame.createPort("S","run",connection = Block_GateSwitch.RUN)
outerFrame.createPort("S","vgsel",connection = CABElements_GateSwitch.Vgsel)
outerFrame.createPort("W","cns0",connection = Oswitch.A[4])
outerFrame.createPort("W","cns1",connection = Oswitch.A[5])
outerFrame.createPort("W","cns2",connection = Oswitch.A[6])
outerFrame.createPort("W","cns3",connection = Oswitch.A[7])
outerFrame.createPort("W","vgrun",connection = CABElements_GateSwitch.RUN_IN[0])
outerFrame.createPort("W","vtun",connection = Block_GateSwitch.VTUN_T[0])
outerFrame.createPort("W","vinj",connection = CABElements_GateSwitch.VINJ_T)
outerFrame.createPort("W","gnd",connection = CABElements_GateSwitch.GND_T)
outerFrame.createPort("W","avdd",connection = CABElements_GateSwitch.VDD[1])
outerFrame.createPort("W","drainbit4",connection = Block_DrainDecode.IN[4])
outerFrame.createPort("W","drainbit3",connection = Block_DrainDecode.IN[3])
outerFrame.createPort("W","drainbit2",connection = Block_DrainDecode.IN[2])
outerFrame.createPort("W","drainbit1",connection = Block_DrainDecode.IN[1])
outerFrame.createPort("W","drainbit0",connection = Block_DrainDecode.IN[0])
outerFrame.createPort("W","s0",connection = Block_DrainCutoff.In[0])
outerFrame.createPort("W","s1",connection = Block_DrainCutoff.In[1])
outerFrame.createPort("W","s2",connection = Block_DrainCutoff.In[2])
outerFrame.createPort("W","s3",connection = Block_DrainCutoff.In[3])
outerFrame.createPort("W","s4",connection = Block_DrainCutoff.In[4])
outerFrame.createPort("W","s5",connection = Block_DrainCutoff.In[5])
outerFrame.createPort("W","s6",connection = Block_DrainCutoff.In[6])
outerFrame.createPort("W","s7",connection = Block_DrainCutoff.In[7])
outerFrame.createPort("W","s8",connection = Block_DrainCutoff.In[8])
outerFrame.createPort("W","s9",connection = Block_DrainCutoff.In[9])
outerFrame.createPort("W","s10",connection = Block_DrainCutoff.In[10])
outerFrame.createPort("W","s11",connection = Block_DrainCutoff.In[11])
outerFrame.createPort("W","s12",connection = Block_DrainCutoff.In[12])
outerFrame.createPort("W","s13",connection = Block_DrainCutoff.In[13])
outerFrame.createPort("W","s14",connection = Block_DrainCutoff.In[14])
outerFrame.createPort("W","s15",connection = Block_DrainCutoff.In[15])
outerFrame.createPort("W","s16",connection = Block_DrainCutoff.In[16])
outerFrame.createPort("W","s17",connection = Block_DrainCutoff.In[17])
outerFrame.createPort("W","s18",connection = Block_DrainCutoff.In[18])
outerFrame.createPort("W","s19",connection = Block_DrainCutoff.In[19])
outerFrame.createPort("W","drainbit10",connection = CAB_DrainDecoder.IN[5])
outerFrame.createPort("W","drainbit9",connection = CAB_DrainDecoder.IN[4])
outerFrame.createPort("W","drainbit8",connection = CAB_DrainDecoder.IN[3])
outerFrame.createPort("W","drainbit7",connection = CAB_DrainDecoder.IN[2])
outerFrame.createPort("W","drainbit6",connection = CAB_DrainDecoder.IN[1])
outerFrame.createPort("W","drainbit5",connection = CAB_DrainDecoder.IN[0])
outerFrame.createPort("W","drainEN",connection = CAB_DrainDecoder.ENABLE)
outerFrame.createPort("E","cns0",connection = Block_GateDecode.VGRUN[30])
outerFrame.createPort("E","cns1",connection = Block_GateDecode.VGRUN[31])
outerFrame.createPort("E","cns2",connection = Block_GateDecode.VGRUN[32])
outerFrame.createPort("E","cns3",connection = Block_GateDecode.VGRUN[33])
outerFrame.createPort("E","vgrun",connection = CABElements_GateSwitch.RUN_IN[0])
outerFrame.createPort("E","vtun",connection = Block_GateSwitch.VTUN_T[0])
outerFrame.createPort("E","vinj",connection = CABElements_GateSwitch.VINJ_T)
outerFrame.createPort("E","gnd",connection = CABElements_GateSwitch.GND_T)
outerFrame.createPort("E","avdd",connection = CABElements_GateSwitch.VDD[1])
outerFrame.createPort("E","drainbit4",connection = Block_DrainDecode.IN[4])
outerFrame.createPort("E","drainbit3",connection = Block_DrainDecode.IN[3])
outerFrame.createPort("E","drainbit2",connection = Block_DrainDecode.IN[2])
outerFrame.createPort("E","drainbit1",connection = Block_DrainDecode.IN[1])
outerFrame.createPort("E","drainbit0",connection = Block_DrainDecode.IN[0])
outerFrame.createPort("E","s0",connection = Block_Switch.A[0])
outerFrame.createPort("E","s1",connection = Block_Switch.A[1])
outerFrame.createPort("E","s2",connection = Block_Switch.A[2])
outerFrame.createPort("E","s3",connection = Block_Switch.A[3])
outerFrame.createPort("E","s4",connection = Block_Switch.A[4])
outerFrame.createPort("E","s5",connection = Block_Switch.A[5])
outerFrame.createPort("E","s6",connection = Block_Switch.A[6])
outerFrame.createPort("E","s7",connection = Block_Switch.A[7])
outerFrame.createPort("E","s8",connection = Block_Switch.A[8])
outerFrame.createPort("E","s9",connection = Block_Switch.A[9])
outerFrame.createPort("E","s10",connection = Block_Switch.A[10])
outerFrame.createPort("E","s11",connection = Block_Switch.A[11])
outerFrame.createPort("E","s12",connection = Block_Switch.A[12])
outerFrame.createPort("E","s13",connection = Block_Switch.A[13])
outerFrame.createPort("E","s14",connection = Block_Switch.A[14])
outerFrame.createPort("E","s15",connection = Block_Switch.A[15])
outerFrame.createPort("E","s16",connection = Block_Switch.A[16])
outerFrame.createPort("E","s17",connection = Block_Switch.A[17])
outerFrame.createPort("E","s18",connection = Block_Switch.A[18])
outerFrame.createPort("E","s19",connection = Block_Switch.A[19])
outerFrame.createPort("E","drainbit10",connection = CAB_DrainDecoder.IN[5])
outerFrame.createPort("E","drainbit9",connection = CAB_DrainDecoder.IN[4])
outerFrame.createPort("E","drainbit8",connection = CAB_DrainDecoder.IN[3])
outerFrame.createPort("E","drainbit7",connection = CAB_DrainDecoder.IN[2])
outerFrame.createPort("E","drainbit6",connection = CAB_DrainDecoder.IN[1])
outerFrame.createPort("E","drainbit5",connection = CAB_DrainDecoder.IN[0])
outerFrame.createPort("E","drainEN",connection = CAB_DrainDecoder.ENABLE)
CAB_DrainDecoder.ENABLE += Block_DrainDecode.ENABLE

# Compilation
design_limits = [1e6, 6.6e5]
location_islands = ((20600, 400000), (20600, 20000), (160000,20000))
compile_asic(Top,process="TSMC350nm",fileName="full_cab_python",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
