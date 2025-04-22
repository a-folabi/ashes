import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *
from ashes_fg.asic.asic_systems import *



def MeadSOS(circuit,island=None,loc=[0,0],Vin=None):

    Top = circuit
    # Placement
    if island == None:
        island = Island(Top)

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


Top = Circuit()


numStages = 5

LPFIsland = Island(Top)

Vin = Wire(Top)
Vouts = [0]*5
Vout_Bufs = [0]*5
instances = [0]*5

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
drainBits = int(np.ceil(np.log2(2*numStages*4)))
CAB_DrainDecoder = STD_DrainDecoder(Top,LPFIsland,bits=drainBits)
CAB_DrainSelect = RunDrainSwitch(Top,LPFIsland,num=2*numStages)
CAB_DrainSwitch = DrainCutoff(Top,LPFIsland,num=2*numStages)

#GateDecoder = STD_IndirectGateDecoder(Top,LPFIsland,1)
GateSwitches0 = STD_IndirectGateSwitch(Top,LPFIsland,1)
GateSwitches = STD_IndirectGateSwitch(Top,LPFIsland,1,col=0)

# Pins
# -------------------------------------------------------------------------------
outerPins = frame(Top)
outerPins.createPort("W","Vin",connection = Vin)
outerPins.createPort("E","Vout",connection = Vout)


design_limits = [5e5, 5e5]
location_islands = ((20000,1000),(0,2000))#<-location for tile v1
#location_islands=None


compile_asic(Top,process="TSMC350nm",fileName="LPF_MeadSOS",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
