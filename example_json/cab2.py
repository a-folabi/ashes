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
C_EW = IndirectVMM(Top,[20,12],island=BlockIsland,decoderPlace=False)
C_NS = IndirectVMM(Top,[20,12],island=BlockIsland,decoderPlace=False,loc = [0,16])

Block_Switch = ST_BMatrix(Top,BlockIsland,[5,1])
Block_Switch.place([0,22])

#SBLOCK
SEC1 = S_SEC1(Top,BlockIsland,[5,1])
SEC1.place([0,6])

SBuff = S_Buffer(Top,BlockIsland,[5,1])
SBuff.place([0,7])

SpaceUp_0 = S_spaceUP(Top,BlockIsland,[4,1])
SpaceUp_0.place([0,8])
Conn_0 = S_Conn12(Top,BlockIsland)
Conn_0.place([4,8])
Conn_0.markAbut()

SpaceUp_1 = S_spaceUP(Top,BlockIsland,[3,1])
SpaceUp_1.place([0,9])
Conn_1 = S_Conn12(Top,BlockIsland)
Conn_1.place([3,9])
Conn_1.markAbut()

SpaceDown_1 = S_spaceDOWN(Top,BlockIsland,[1,1])
SpaceDown_1.place([4,9])
SpaceDown_1.markAbut()

SpaceUp_2 = S_spaceUP(Top,BlockIsland,[2,1])
SpaceUp_2.place([0,10])
Conn_2 = S_Conn12(Top,BlockIsland)
Conn_2.place([2,10])
Conn_2.markAbut()

SpaceDown_2 = S_spaceDOWN(Top,BlockIsland,[2,1])
SpaceDown_2.place([3,10])
SpaceUp_3 = S_spaceUP(Top,BlockIsland,[1,1])
SpaceUp_3.place([0,11])
SpaceUp_3.markAbut()

Conn_3 = S_Conn12(Top,BlockIsland)
Conn_3.place([1,11])
Conn_3.markAbut()

SpaceDown_3 = S_spaceDOWN(Top,BlockIsland,[3,1])
SpaceDown_3.place([2,11])
Conn_4 = S_Conn12(Top,BlockIsland)
Conn_4.place([0,12])
Conn_4.markAbut()

SpaceDown_4 = S_spaceDOWN(Top,BlockIsland,[4,1])
SpaceDown_4.place([1,12])
SEC2 = S_SEC2(Top,BlockIsland,[5,1])
SEC2.place([0,13])

Conn_5 = S_Conn23(Top,BlockIsland,[5,1])
Conn_5.place([0,14])

SEC3 = S_SEC3(Top,BlockIsland,[5,1])
SEC3.place([0,15])

# Decoders
Block_GateDecode = STD_IndirectGateDecoder(Top,island=BlockIsland,bits=5)
Block_GateSwitch = STD_IndirectGateSwitch(Top,island=BlockIsland,num=22)

Block_DrainDecode = STD_DrainDecoder(Top,island=BlockIsland,bits=5)
Block_DrainSelect = RunDrainSwitch(Top,island=BlockIsland,num=5)
Block_DrainCutoff = DrainCutoff(Top,BlockIsland,num=5)
for i in range(7,13):
	ERASE_IndirectGateSwitch(Top,island=BlockIsland,col=i)
ERASE_IndirectGateSwitch(Top,island=BlockIsland,col=14)

# CAB
CABIsland = Island(Top)

# A matrix
Atop = BlockTop(Top,CABIsland,[1,7])
Atop.place([0,0])
Amatrix = IndirectVMM(Top,[20,14],island=CABIsland,decoderPlace=False,loc=[1,0])

# B matrix
Btop = BlockTop(Top,CABIsland,[1,7])
Btop.place([0,7])
Bmatrix = IndirectVMM(Top,[16,14],island=CABIsland,decoderPlace=False,loc=[1,7])
Bbot = B_bot(Top,CABIsland,[1,7])
Bbot.place([5,7])

Bswitch0 = ST_BMatrix(Top,CABIsland)
Bswitch0.place([0,14])
Bswitch0.markAbut()

Bswitch1 = ST_BMatrix(Top,CABIsland)
Bswitch1.place([1,14])
Bswitch1.markAbut()

Bswitch2 = ST_BMatrix(Top,CABIsland)
Bswitch2.place([2,14])
Bswitch2.markAbut()

Bswitch3 = ST_BMatrix_NoSwitch(Top,CABIsland)
Bswitch3.place([3,14])
Bswitch3.markAbut()

Bswitch4 = ST_BMatrix(Top,CABIsland)
Bswitch4.place([4,14])
Bswitch4.markAbut()

Bswitch5 = ST_BMatrix(Top,CABIsland)
Bswitch5.place([5,14])
Bswitch5.markAbut()

BtoOut = OutSwitch(Top,CABIsland,[1,7])
BtoOut.place([7,7])

# Output Matrix
Outmatrix = IndirectVMM(Top,[8,14],island=CABIsland,decoderPlace=False,loc=[8,7])
Oswitch = ST_BMatrix(Top,CABIsland,[2,1])
Oswitch.place([8,14])

# CAB Elements
TA2Cell_Weak = TSMC350nm_TA2Cell_Weak(Top,CABIsland)
TA2Cell_Weak.place([2,15])
TA2Cell_Weak.markCABDevice()

TA2Cell_Strong = TSMC350nm_TA2Cell_Strong(Top,CABIsland)
TA2Cell_Strong.place([3,15])
TA2Cell_Strong.markCABDevice()

Cap_Bank = TSMC350nm_Cap_Bank(Top,CABIsland)
Cap_Bank.place([4,15])
Cap_Bank.markCABDevice()

WTA_IndirectProg = TSMC350nm_4WTA_IndirectProg(Top,CABIsland)
WTA_IndirectProg.place([5,15])
WTA_IndirectProg.markCABDevice()

NandPfets = TSMC350nm_NandPfets(Top,CABIsland)
NandPfets.place([6,15])
NandPfets.markCABDevice()

VolSwitchIsland = Island(Top)

VolSwitch = TSMC350nm_volatile_swcs(Top,VolSwitchIsland,[1,6])
VolSwitch.place([0,0])

# Decoders
CAB_DrainDecoder = STD_DrainDecoder(Top,CABIsland,bits=6)
CAB_DrainSelect = RunDrainSwitch(Top,CABIsland,num=10)
CAB_DrainSwitch = DrainCutoff(Top,CABIsland,num=10)

CAB_GateSwitch = STD_GorS_IndirectSwitches(Top,CABIsland,num=16)
ERASE_IndirectGateSwitch(Top,CABIsland,col=14)
CABElements_GateSwitch = STD_IndirectGateSwitch(Top,CABIsland,col=15)

# Bmatrix <--> CAB Elements Connections


TA2Cell_Weak.VD_P += Bswitch0.P[0:2]
TA2Cell_Weak.VIN1_PLUS += Bswitch0.A[0]
TA2Cell_Weak.VIN1_MINUS += Bswitch0.A[1]
TA2Cell_Weak.VIN2_PLUS += Bswitch0.A[2]
TA2Cell_Weak.VIN2_MINUS += Bswitch0.A[3]
TA2Cell_Weak.OUTPUT += CAB_GateSwitch.Input[14:16]
TA2Cell_Weak.Vsel += CABElements_GateSwitch.CTRL_B
TA2Cell_Weak.RUN += CABElements_GateSwitch.run_r
TA2Cell_Weak.Vg += CABElements_GateSwitch.Vg
TA2Cell_Weak.PROG += CABElements_GateSwitch.prog_r
TA2Cell_Weak.VTUN += CABElements_GateSwitch.VTUN
TA2Cell_Weak.VINJ += CABElements_GateSwitch.VINJ
TA2Cell_Weak.GND += CABElements_GateSwitch.GND[0]
TA2Cell_Weak.VPWR += CABElements_GateSwitch.VDD[1]

TA2Cell_Strong.VD_P += Bswitch1.P[0:2]
TA2Cell_Strong.VIN1_PLUS += Bswitch1.A[0]
TA2Cell_Strong.VIN1_MINUS += Bswitch1.A[1]
TA2Cell_Strong.VIN2_PLUS += Bswitch1.A[2]
TA2Cell_Strong.VIN2_MINUS += Bswitch1.A[3]
TA2Cell_Strong.OUTPUT += CAB_GateSwitch.Input[16:18]
TA2Cell_Strong.Vsel += TA2Cell_Weak.Vsel_b
TA2Cell_Strong.RUN += TA2Cell_Weak.RUN_b
TA2Cell_Strong.Vg += TA2Cell_Weak.Vg_b
TA2Cell_Strong.PROG += TA2Cell_Weak.PROG_b
TA2Cell_Strong.VTUN += TA2Cell_Weak.VTUN_b
TA2Cell_Strong.VINJ += TA2Cell_Weak.VINJ_b
TA2Cell_Strong.GND += TA2Cell_Weak.GND_b
TA2Cell_Strong.VPWR += TA2Cell_Weak.VPWR_b

Cap_Bank.VD_P += Bswitch2.P[0:4]
Cap_Bank.VIN += Bswitch2.A[0:2]
Cap_Bank.OUT += CAB_GateSwitch.Input[18:20]
Cap_Bank.VINJ += TA2Cell_Strong.VINJ_b
Cap_Bank.Vsel += TA2Cell_Strong.Vsel_b
Cap_Bank.Vg += TA2Cell_Strong.Vg_b
Cap_Bank.GND += TA2Cell_Strong.GND_b
Cap_Bank.VTUN += TA2Cell_Strong.VTUN_b

WTA_IndirectProg.VD_P += Bswitch3.P[0:4]
WTA_IndirectProg.Iin += Bswitch3.A[0:4]
WTA_IndirectProg.Vout += CAB_GateSwitch.Input[20:24]
WTA_IndirectProg.Vmid += CAB_GateSwitch.Input[24]
WTA_IndirectProg.Vbias += CAB_GateSwitch.Input[25]
WTA_IndirectProg.Vsel += CABElements_GateSwitch.CTRL_B[0]
WTA_IndirectProg.Vs += CABElements_GateSwitch.VDD[1]
WTA_IndirectProg.VINJ += Cap_Bank.VINJ_b
WTA_IndirectProg.Vg += Cap_Bank.Vg_b[0]
WTA_IndirectProg.VTUN += Cap_Bank.VTUN_b
WTA_IndirectProg.GND += Cap_Bank.GND_b
WTA_IndirectProg.PROG += CABElements_GateSwitch.prog_r

NandPfets.GATE_N += Bswitch4.A[0]
NandPfets.SOURCE_N += Bswitch4.A[1]
NandPfets.GATE_P += Bswitch4.A[2]
NandPfets.SOURCE_P += Bswitch4.A[3]
NandPfets.DRAIN_N += CAB_GateSwitch.Input[26]
NandPfets.DRAIN_P += CAB_GateSwitch.Input[27]
NandPfets.VPWR += CABElements_GateSwitch.VDD[1]
NandPfets.GND += WTA_IndirectProg.GND_b

CAB_GateSwitch.Input[0] += CABElements_GateSwitch.VPWR[0]
CABElements_GateSwitch.VPWR[1] += CABElements_GateSwitch.VPWR[0]
C_EW.Vsel_b += CAB_GateSwitch.Vsel[0:12]
C_EW.Vg_b += CAB_GateSwitch.Vg_global[0:12]
C_EW.VTUN_b += CAB_GateSwitch.VTUN[0:6]
C_EW.GND_b[1] += CAB_GateSwitch.GND[0]
C_EW.GND_b[3] += CAB_GateSwitch.GND[1]
C_EW.GND_b[5] += CAB_GateSwitch.GND[2]
C_EW.GND_b[7] += CAB_GateSwitch.GND[3]
C_EW.GND_b[9] += CAB_GateSwitch.GND[4]
C_EW.GND_b[11] += CAB_GateSwitch.GND[5]
CAB_GateSwitch.GND[0] += CAB_GateSwitch.Input[1]
C_EW.VINJ_b[1] += CAB_GateSwitch.VINJ[0]
C_EW.VINJ_b[3] += CAB_GateSwitch.VINJ[1]
C_EW.VINJ_b[5] += CAB_GateSwitch.VINJ[2]
C_EW.VINJ_b[7] += CAB_GateSwitch.VINJ[3]
C_EW.VINJ_b[9] += CAB_GateSwitch.VINJ[4]
C_EW.VINJ_b[11] += CAB_GateSwitch.VINJ[5]
C_EW.Vs_b[2] += CAB_GateSwitch.Input[2]
C_EW.Vs_b[3] += CAB_GateSwitch.Input[3]
C_EW.Vs_b[4] += CAB_GateSwitch.Input[4]
C_EW.Vs_b[5] += CAB_GateSwitch.Input[5]
SEC1.VINJ_b += CAB_GateSwitch.VINJ[6]
SEC1.VTUN_b += CAB_GateSwitch.VTUN[6]
SEC1.GND_b[1] += CAB_GateSwitch.GND[6]
SEC1.Vsel_b[0] += CAB_GateSwitch.Vsel[13]
SEC1.Vsel_b[1] += CAB_GateSwitch.Vsel[12]
SEC1.Vg_b[0] += CAB_GateSwitch.Vg_global[13]
SEC1.Vg_b[1] += CAB_GateSwitch.Vg_global[12]
SEC2.VINJ_b += CAB_GateSwitch.VINJ[7]
SEC2.VTUN_b += CAB_GateSwitch.VTUN[7]
SEC2.GND_b[1] += CAB_GateSwitch.GND[7]
SEC2.Vsel_b[0] += CAB_GateSwitch.Vsel[15]
SEC2.Vsel_b[1] += CAB_GateSwitch.Vsel[14]
SEC2.Vg_b[0] += CAB_GateSwitch.Vg_global[15]
SEC2.Vg_b[1] += CAB_GateSwitch.Vg_global[14]
SEC3.VINJ_b += CAB_GateSwitch.VINJ[8]
SEC3.VTUN_b += CAB_GateSwitch.VTUN[8]
SEC3.GND_b[1] += CAB_GateSwitch.GND[8]
SEC3.Vsel_b[0] += CAB_GateSwitch.Vsel[17]
SEC3.Vsel_b[1] += CAB_GateSwitch.Vsel[16]
SEC3.Vg_b[0] += CAB_GateSwitch.Vg_global[17]
SEC3.Vg_b[1] += CAB_GateSwitch.Vg_global[16]
C_NS.VTUN_b[0] += CAB_GateSwitch.VTUN[9]
C_NS.VINJ_b[1] += CAB_GateSwitch.VINJ[9]
C_NS.GND_b[1] += CAB_GateSwitch.GND[9]
C_NS.Vsel_b[0] += CAB_GateSwitch.Vsel[18]
C_NS.Vg_b[0] += CAB_GateSwitch.Vg_global[18]
C_NS.Vsel_b[1] += CAB_GateSwitch.Vsel[19]
C_NS.Vg_b[1] += CAB_GateSwitch.Vg_global[19]
C_NS.VTUN_b[1] += CAB_GateSwitch.VTUN[10]
C_NS.VINJ_b[3] += CAB_GateSwitch.VINJ[10]
C_NS.GND_b[3] += CAB_GateSwitch.GND[10]
C_NS.Vsel_b[2] += CAB_GateSwitch.Vsel[20]
C_NS.Vg_b[2] += CAB_GateSwitch.Vg_global[20]
C_NS.Vsel_b[3] += CAB_GateSwitch.Vsel[21]
C_NS.Vg_b[3] += CAB_GateSwitch.Vg_global[21]
C_NS.VTUN_b[2] += CAB_GateSwitch.VTUN[11]
C_NS.VINJ_b[5] += CAB_GateSwitch.VINJ[11]
C_NS.GND_b[5] += CAB_GateSwitch.GND[11]
C_NS.Vsel_b[4] += CAB_GateSwitch.Vsel[22]
C_NS.Vg_b[4] += CAB_GateSwitch.Vg_global[22]
C_NS.Vsel_b[5] += CAB_GateSwitch.Vsel[23]
C_NS.Vg_b[5] += CAB_GateSwitch.Vg_global[23]
C_NS.VTUN_b[3] += CAB_GateSwitch.VTUN[12]
C_NS.VINJ_b[7] += CAB_GateSwitch.VINJ[12]
C_NS.GND_b[7] += CAB_GateSwitch.GND[12]
C_NS.Vsel_b[6] += CAB_GateSwitch.Vsel[24]
C_NS.Vg_b[6] += CAB_GateSwitch.Vg_global[24]
C_NS.Vsel_b[7] += CAB_GateSwitch.Vsel[25]
C_NS.Vg_b[7] += CAB_GateSwitch.Vg_global[25]
C_NS.VTUN_b[4] += CAB_GateSwitch.VTUN[13]
C_NS.VINJ_b[9] += CAB_GateSwitch.VINJ[13]
C_NS.GND_b[9] += CAB_GateSwitch.GND[13]
C_NS.Vsel_b[8] += CAB_GateSwitch.Vsel[26]
C_NS.Vg_b[8] += CAB_GateSwitch.Vg_global[26]
C_NS.Vsel_b[9] += CAB_GateSwitch.Vsel[27]
C_NS.Vg_b[9] += CAB_GateSwitch.Vg_global[27]
C_NS.VTUN_b[5] += CAB_GateSwitch.VTUN[14]
C_NS.VINJ_b[11] += CAB_GateSwitch.VINJ[14]
C_NS.GND_b[11] += CAB_GateSwitch.GND[14]
C_NS.Vsel_b[10] += CAB_GateSwitch.Vsel[28]
C_NS.Vg_b[10] += CAB_GateSwitch.Vg_global[28]
C_NS.Vsel_b[11] += CAB_GateSwitch.Vsel[29]
C_NS.Vg_b[11] += CAB_GateSwitch.Vg_global[29]
C_NS.Vs_b[0] += CAB_GateSwitch.Input[6]
C_NS.Vsel_b[10] += CABElements_GateSwitch.decode[0]
C_NS.VTUN_b[5] += CABElements_GateSwitch.VTUN_T
C_NS.GND_b[11] += CABElements_GateSwitch.GND_T
C_NS.Vsel_b[11] += CABElements_GateSwitch.decode[1]
C_NS.VINJ_b[11] += CABElements_GateSwitch.VINJ_T
Block_GateDecode.VINJ_b[0] += Block_GateSwitch.VINJ_T[0]
Block_GateDecode.GND_b[0] += Block_GateSwitch.GND_T[0]
Block_GateDecode.OUT[0] += Block_GateSwitch.decode[0]
Block_GateDecode.OUT[1] += Block_GateSwitch.decode[1]
Block_GateDecode.VINJ_b[1] += Block_GateSwitch.VINJ_T[1]
Block_GateDecode.GND_b[1] += Block_GateSwitch.GND_T[1]
Block_GateDecode.OUT[2] += Block_GateSwitch.decode[2]
Block_GateDecode.OUT[3] += Block_GateSwitch.decode[3]
Block_GateDecode.VINJ_b[2] += Block_GateSwitch.VINJ_T[2]
Block_GateDecode.GND_b[2] += Block_GateSwitch.GND_T[2]
Block_GateDecode.OUT[4] += Block_GateSwitch.decode[4]
Block_GateDecode.OUT[5] += Block_GateSwitch.decode[5]
Block_GateDecode.VINJ_b[3] += Block_GateSwitch.VINJ_T[3]
Block_GateDecode.GND_b[3] += Block_GateSwitch.GND_T[3]
Block_GateDecode.OUT[6] += Block_GateSwitch.decode[6]
Block_GateDecode.OUT[7] += Block_GateSwitch.decode[7]
Block_GateDecode.VINJ_b[4] += Block_GateSwitch.VINJ_T[4]
Block_GateDecode.GND_b[4] += Block_GateSwitch.GND_T[4]
Block_GateDecode.OUT[8] += Block_GateSwitch.decode[8]
Block_GateDecode.OUT[9] += Block_GateSwitch.decode[9]
Block_GateDecode.VINJ_b[5] += Block_GateSwitch.VINJ_T[5]
Block_GateDecode.GND_b[5] += Block_GateSwitch.GND_T[5]
Block_GateDecode.OUT[10] += Block_GateSwitch.decode[10]
Block_GateDecode.OUT[11] += Block_GateSwitch.decode[11]
Block_GateDecode.VINJ_b[6] += Block_GateSwitch.VINJ_T[6]
Block_GateDecode.GND_b[6] += Block_GateSwitch.GND_T[6]
Block_GateDecode.OUT[12] += Block_GateSwitch.decode[12]
Block_GateDecode.OUT[13] += Block_GateSwitch.decode[13]
Block_GateDecode.VINJ_b[8] += Block_GateSwitch.VINJ_T[14]
Block_GateDecode.GND_b[8] += Block_GateSwitch.GND_T[14]
Block_GateDecode.OUT[16] += Block_GateSwitch.decode[28]
Block_GateDecode.OUT[17] += Block_GateSwitch.decode[29]
Block_GateDecode.VINJ_b[9] += Block_GateSwitch.VINJ_T[15]
Block_GateDecode.GND_b[9] += Block_GateSwitch.GND_T[15]
Block_GateDecode.OUT[18] += Block_GateSwitch.decode[30]
Block_GateDecode.OUT[19] += Block_GateSwitch.decode[31]
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
Block_GateDecode.RUN_OUT[6] += Block_GateSwitch.VPWR[6]
Block_GateDecode.RUN_OUT[7] += Block_GateSwitch.VPWR[7]
Block_GateDecode.RUN_OUT[8] += Block_GateSwitch.VPWR[8]
Block_GateDecode.RUN_OUT[9] += Block_GateSwitch.VPWR[9]
Block_GateDecode.RUN_OUT[22] += Block_GateSwitch.VPWR[34]
Block_GateDecode.RUN_OUT[23] += Block_GateSwitch.VPWR[35]
Block_GateDecode.RUN_OUT[24] += Block_GateSwitch.VPWR[36]
Block_GateDecode.RUN_OUT[25] += Block_GateSwitch.VPWR[37]
FakeCell0 = FakeCell(Top,CABIsland)
FakeCell0.place([50,50])
Block_GateDecode.RUN_OUT[0] += FakeCell0.FakePort
FakeCell1 = FakeCell(Top,CABIsland)
FakeCell1.place([50,51])
Block_GateDecode.RUN_OUT[1] += FakeCell1.FakePort
FakeCell2 = FakeCell(Top,CABIsland)
FakeCell2.place([50,52])
Block_GateDecode.RUN_OUT[2] += FakeCell2.FakePort
FakeCell3 = FakeCell(Top,CABIsland)
FakeCell3.place([50,53])
Block_GateDecode.RUN_OUT[3] += FakeCell3.FakePort
FakeCell4 = FakeCell(Top,CABIsland)
FakeCell4.place([50,54])
Block_GateDecode.RUN_OUT[4] += FakeCell4.FakePort
FakeCell5 = FakeCell(Top,CABIsland)
FakeCell5.place([50,55])
Block_GateDecode.RUN_OUT[5] += FakeCell5.FakePort
FakeCell10 = FakeCell(Top,CABIsland)
FakeCell10.place([50,60])
Block_GateDecode.RUN_OUT[10] += FakeCell10.FakePort
FakeCell11 = FakeCell(Top,CABIsland)
FakeCell11.place([50,61])
Block_GateDecode.RUN_OUT[11] += FakeCell11.FakePort
FakeCell12 = FakeCell(Top,CABIsland)
FakeCell12.place([50,62])
Block_GateDecode.RUN_OUT[12] += FakeCell12.FakePort
FakeCell13 = FakeCell(Top,CABIsland)
FakeCell13.place([50,63])
Block_GateDecode.RUN_OUT[13] += FakeCell13.FakePort
FakeCell14 = FakeCell(Top,CABIsland)
FakeCell14.place([50,64])
Block_GateDecode.RUN_OUT[14] += FakeCell14.FakePort
FakeCell15 = FakeCell(Top,CABIsland)
FakeCell15.place([50,65])
Block_GateDecode.RUN_OUT[15] += FakeCell15.FakePort
FakeCell16 = FakeCell(Top,CABIsland)
FakeCell16.place([50,66])
Block_GateDecode.RUN_OUT[16] += FakeCell16.FakePort
FakeCell17 = FakeCell(Top,CABIsland)
FakeCell17.place([50,67])
Block_GateDecode.RUN_OUT[17] += FakeCell17.FakePort
FakeCell18 = FakeCell(Top,CABIsland)
FakeCell18.place([50,68])
Block_GateDecode.RUN_OUT[18] += FakeCell18.FakePort
FakeCell19 = FakeCell(Top,CABIsland)
FakeCell19.place([50,69])
Block_GateDecode.RUN_OUT[19] += FakeCell19.FakePort
FakeCell20 = FakeCell(Top,CABIsland)
FakeCell20.place([50,70])
Block_GateDecode.RUN_OUT[20] += FakeCell20.FakePort
FakeCell21 = FakeCell(Top,CABIsland)
FakeCell21.place([50,71])
Block_GateDecode.RUN_OUT[21] += FakeCell21.FakePort
FakeCell26 = FakeCell(Top,CABIsland)
FakeCell26.place([50,76])
Block_GateDecode.RUN_OUT[26] += FakeCell26.FakePort
FakeCell27 = FakeCell(Top,CABIsland)
FakeCell27.place([50,77])
Block_GateDecode.RUN_OUT[27] += FakeCell27.FakePort
FakeCell28 = FakeCell(Top,CABIsland)
FakeCell28.place([50,78])
Block_GateDecode.RUN_OUT[28] += FakeCell28.FakePort
FakeCell29 = FakeCell(Top,CABIsland)
FakeCell29.place([50,79])
Block_GateDecode.RUN_OUT[29] += FakeCell29.FakePort
FakeCell30 = FakeCell(Top,CABIsland)
FakeCell30.place([50,80])
Block_GateDecode.RUN_OUT[30] += FakeCell30.FakePort
FakeCell31 = FakeCell(Top,CABIsland)
FakeCell31.place([50,81])
Block_GateDecode.RUN_OUT[31] += FakeCell31.FakePort
Block_DrainCutoff.PR += C_EW.Vd_Pl
Block_DrainCutoff.In += C_EW.Vd_Rl

VolSwitch.out += Amatrix.Vs_b[0:12]
VolSwitch.VINJ += Amatrix.VINJ_b[0:12]
VolSwitch.Vsel += Amatrix.Vsel_b[0:12]
VolSwitch.Vg += Amatrix.Vg_b[0:12]
VolSwitch.GND += Amatrix.GND_b[0:6]
VolSwitch.VTUN += Amatrix.VTUN_b[0:6]
VolSwitch.D += C_EW.Vs_b[10]
VolSwitch.CLK += C_EW.Vs_b[11]
VolSwitch.Q += C_NS.Vs_b[7]
VolSwitch.com += CAB_GateSwitch.Input[13]
CABElements_GateSwitch.VDD[1] += VolSwitch.VDD
VolSwitch.Vd_P += CAB_DrainSwitch.PR[27]
VolSwitch.Vd_in[0] += CAB_DrainSwitch.In[24]
VolSwitch.Vd_in[4] += CAB_DrainSwitch.PR[24]
VolSwitch.Vd_o[0] += Outmatrix.Vd_Rl[0]
VolSwitch.Vd_o[4] += Outmatrix.Vd_Pl[0]
VolSwitch.Vd_in[1] += CAB_DrainSwitch.In[25]
VolSwitch.Vd_in[5] += CAB_DrainSwitch.PR[25]
VolSwitch.Vd_o[1] += Outmatrix.Vd_Rl[1]
VolSwitch.Vd_o[5] += Outmatrix.Vd_Pl[1]
VolSwitch.Vd_in[2] += CAB_DrainSwitch.In[26]
VolSwitch.Vd_in[6] += CAB_DrainSwitch.PR[26]
VolSwitch.Vd_o[2] += Outmatrix.Vd_Rl[2]
VolSwitch.Vd_o[6] += Outmatrix.Vd_Pl[2]
VolSwitch.Vd_in[3] += CAB_DrainSwitch.In[27]
VolSwitch.Vd_in[7] += CAB_DrainSwitch.PR[27]
VolSwitch.Vd_o[3] += Outmatrix.Vd_Rl[3]
VolSwitch.Vd_o[7] += Outmatrix.Vd_Pl[3]
CABElements_GateSwitch.VDD[1] += CAB_GateSwitch.AVDD_r
CABElements_GateSwitch.PROG += CAB_GateSwitch.prog_r
CABElements_GateSwitch.RUN += CAB_GateSwitch.run_r
CABElements_GateSwitch.prog_r += Block_Switch.Prog_b
Block_Switch.GND_b += CABElements_GateSwitch.GND_T
Block_Switch.VDD_b += CABElements_GateSwitch.VPWR[1]
Bswitch0.GND += CABElements_GateSwitch.GND_T
Bswitch0.VDD += CABElements_GateSwitch.VPWR[1]
Bswitch0.Prog += CABElements_GateSwitch.PROG
Oswitch.GND += Bswitch5.GND_b
Oswitch.VDD += Bswitch5.VDD_b
Oswitch.Prog += Bswitch5.Prog_b
CABElements_GateSwitch.RUN_IN[1] += CAB_GateSwitch.Vgrun_r
CABElements_GateSwitch.RUN_IN[0] += CAB_GateSwitch.Vgrun_r
Block_GateSwitch.RUN_IN[0] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[1] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[2] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[3] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[4] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[5] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[6] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[7] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[8] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[9] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[10] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[11] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[12] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[13] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[26] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[27] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[30] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[31] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[32] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[33] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[34] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[35] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[36] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[37] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[38] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[39] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[40] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[41] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[42] += CAB_GateSwitch.Vgrun
Block_GateSwitch.RUN_IN[43] += CAB_GateSwitch.Vgrun

outerFrame = frame(Top)
outerFrame.createPort("N","gateEN",connection = Block_GateDecode.ENABLE)
outerFrame.createPort("N","programdrain",connection = Block_DrainSelect.prog_drainrail)
Block_DrainSelect.prog_drainrail += CAB_DrainSelect.prog_drainrail
outerFrame.createPort("N","rundrain",connection = Block_DrainSelect.run_drainrail)
Block_DrainSelect.run_drainrail += CAB_DrainSelect.run_drainrail
outerFrame.createPort("N","cew0",connection = Block_GateDecode.VGRUN[6])
outerFrame.createPort("N","cew1",connection = Block_GateDecode.VGRUN[7])
outerFrame.createPort("N","cew2",connection = Block_GateDecode.VGRUN[8])
outerFrame.createPort("N","cew3",connection = Block_GateDecode.VGRUN[9])
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
outerFrame.createPort("W","drainbit9",connection = CAB_DrainDecoder.IN[4])
outerFrame.createPort("W","drainbit8",connection = CAB_DrainDecoder.IN[3])
outerFrame.createPort("W","drainbit7",connection = CAB_DrainDecoder.IN[2])
outerFrame.createPort("W","drainbit6",connection = CAB_DrainDecoder.IN[1])
outerFrame.createPort("W","drainbit5",connection = CAB_DrainDecoder.IN[0])
outerFrame.createPort("W","drainEN",connection = CAB_DrainDecoder.ENABLE)
outerFrame.createPort("E","cns0",connection = Block_GateDecode.VGRUN[22])
outerFrame.createPort("E","cns1",connection = Block_GateDecode.VGRUN[23])
outerFrame.createPort("E","cns2",connection = Block_GateDecode.VGRUN[24])
outerFrame.createPort("E","cns3",connection = Block_GateDecode.VGRUN[25])
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
outerFrame.createPort("E","drainbit9",connection = CAB_DrainDecoder.IN[4])
outerFrame.createPort("E","drainbit8",connection = CAB_DrainDecoder.IN[3])
outerFrame.createPort("E","drainbit7",connection = CAB_DrainDecoder.IN[2])
outerFrame.createPort("E","drainbit6",connection = CAB_DrainDecoder.IN[1])
outerFrame.createPort("E","drainbit5",connection = CAB_DrainDecoder.IN[0])
outerFrame.createPort("E","drainEN",connection = CAB_DrainDecoder.ENABLE)
CAB_DrainDecoder.ENABLE += Block_DrainDecode.ENABLE

# Compilation
design_limits = [1e6, 6.1e5]
location_islands = ((20600, 363500), (20600, 20000), (162500,20000))
compile_asic(Top,process="TSMC350nm",fileName="cab2",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
