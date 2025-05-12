import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *



def MeadSOS(circuit,LPFIsland=None,loc=[0,0],Vin=None):

    Top = circuit
    # Placement
    if LPFIsland == None:
        LPFIsland = Island(Top)

    TAWeak0 = TSMC350nm_TA2Cell_Weak(Top,LPFIsland)
    TAWeak1 = TSMC350nm_TA2Cell_Weak(Top,LPFIsland)

    TAWeak0.markAbut()
    TAWeak1.markAbut()

    TAWeak0.place([loc[0],loc[1]])
    TAWeak1.place([loc[0]+1,loc[1]])
    # Connections
	# V1 = TA Weak
    # -------------------------------------------------------------------------------
    if Vin != None:
        TAWeak0.VIN1_PLUS += Vin
    # Feedback Buffer Connections
    Vmid = Wire(Top)
    # TA1
    TAWeak0.OUTPUT[0] += Vmid
    TAWeak0.VIN1_MINUS += Vmid
    # TA2
    TAWeak1.VIN1_PLUS += Vmid
    # TA3
    TAWeak0.VIN2_PLUS += Vmid
    TAWeak0.OUTPUT[1] += Vmid
    # Output Connections
    Vout = Wire(Top)
    # TA2
    TAWeak1.OUTPUT[0] += Vout
    TAWeak1.VIN1_MINUS += Vout
    # TA3
    TAWeak0.VIN2_MINUS += Vout
    #Buffer
    TAWeak1.VIN2_PLUS += Vout
    # Buffer Feedback
    Vout_Buf = Wire(Top)
    TAWeak1.VIN2_MINUS += Vout_Buf
    TAWeak1.OUTPUT[1] += Vout_Buf

    return Vout,Vout_Buf,[TAWeak0,TAWeak1]

def LPF_MeadSOS(Top,numStages=1,Vin=None):
    LPFIsland = Island(Top)

    if Vin == None:
        Vin = Wire(Top)

    Vouts = [0]*numStages
    Vout_Bufs = [0]*numStages
    instances = [0]*numStages

    for i in range(numStages):  
        MeadVin = None
        if i == 0:
            MeadVin = Vin
        else:
            MeadVin = Vouts[i-1]
            
        Vouts[i],Vout_Bufs[i],instances[i] = MeadSOS(Top,LPFIsland,Vin=MeadVin,loc=[2*(i),0])

    Vout = Vouts[numStages-1]

    # FG Programming
    # -------------------------------------------------------------------------------
    drainBits = int(np.ceil(np.log2(numStages*4)))
    DrainDecoder = STD_DrainDecoder(Top,LPFIsland,bits=drainBits)
    DrainSelect = RunDrainSwitch(Top,LPFIsland,num=numStages)
    DrainSwitch = DrainCutoff(Top,LPFIsland,num=numStages)

    # Connect program drains to drain switch
    for i in range(numStages):
        DrainSwitch.PR[4*i] += instances[i][0].VD_P[0]
        DrainSwitch.PR[(4*i)+1] += instances[i][0].VD_P[1]
        
        DrainSwitch.PR[(4*i)+2] += instances[i][1].VD_P[0]
        DrainSwitch.PR[(4*i)+3] += instances[i][1].VD_P[1]
        
    GateDecoder = STD_IndirectGateDecoder(Top,LPFIsland,2)
    GateSwitches0 = STD_IndirectGateSwitch(Top,LPFIsland,1)
    GateSwitches = STD_IndirectGateSwitch(Top,LPFIsland,1,col=0)

    GateSwitches0.Vg[0] += instances[0][0].Vg[0]
    GateSwitches0.Vg[1] += instances[0][0].Vg[1]
    GateSwitches0.CTRL_B += instances[0][0].Vsel

    # Pins
    # -------------------------------------------------------------------------------
    outerPins = frame(Top)
    outerPins.createPort("W","Vin",connection = Vin)
    VOUT = outerPins.createPort("E","Vout",connection = Vout)

    PIN_Vout_Buf = outerPins.createPort("E","Vout_Buf",dimension=numStages)
    for i in range(numStages):
        Vout_Bufs[i] += PIN_Vout_Buf[i]

    PROG = outerPins.createPort("N","Prog")
    RUN = outerPins.createPort("N","Run")
    VGRUN = outerPins.createPort("N","VGRUN")
    VGPROG = outerPins.createPort("N","VGPROG")

    VTUN = outerPins.createPort("N","VTUN")
    AVDD = outerPins.createPort("N","AVDD")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    Drainline = outerPins.createPort("S","Drainline_Prog")

    GateEnable = outerPins.createPort("N","GateEnable")
    GateB = outerPins.createPort("W","GateB",dimension=2)

    DrainEnable = outerPins.createPort("W","DrainEnable")
    DrainB = outerPins.createPort("W","DrainB",dimension=drainBits)

    # Pin Connections
    # -------------------------------------------------------------------------------
    GateSwitches.RUN_IN += VGRUN[0]
    GateSwitches0.VINJ_T += GateDecoder.VINJ_b[0]
    GateSwitches0.GND_T += GND_N
    GateSwitches.Vgsel += VGPROG
    GateSwitches.PROG += PROG
    GateSwitches.RUN += RUN

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateB

    DrainSwitch.VDD += VINJ_S
    DrainSwitch.GND += GND_S
    DrainSwitch.RUN += RUN

    DrainSelect.VINJ += VINJ_S
    DrainSelect.GND += GND_S
    DrainSelect.prog_drainrail += Drainline

    DrainDecoder.VINJ += VINJ_S
    DrainDecoder.GND += GND_S
    DrainDecoder.IN += DrainB
    DrainDecoder.ENABLE += DrainEnable


    instances[numStages-1][1].GND_b += GND_S
    instances[numStages-1][1].VINJ_b += VINJ_S
    instances[0][0].VINJ += VINJ_N
    instances[0][0].GND += GND_N
    instances[0][0].VTUN += VTUN
    instances[0][0].VPWR += AVDD[0]
    instances[0][0].PROG += PROG
    instances[0][0].RUN += RUN

    return VOUT

Top = Circuit()
LPF_MeadSOS(Top,5)

design_limits = [5e5, 5e5]
location_islands = ((50000,25000),(0,0))


compile_asic(Top,process="TSMC350nm",fileName="LPF_MeadSOS",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 15,gateSpaceIdx=0,gateSpace=10)
