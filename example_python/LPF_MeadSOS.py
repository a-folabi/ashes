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

LPFIsland = Island(Top)

Vout0,Vout_Buf0,instances0 = MeadSOS(Top,LPFIsland)
Vout1,Vout_Buf1,instances1 = MeadSOS(Top,LPFIsland,[2,0],Vout0)

# Decoders
# -------------------------------------------------------------------------------

design_limits = [1e6, 1e6]
#location_islands = ((20600, 363500), (20600, 20000)) #<-location for tile v1
location_islands=None


compile_asic(Top,process="TSMC350nm",fileName="LPF_MeadSOS",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
