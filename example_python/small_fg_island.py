import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *

from ashes_fg.asic.asic_systems import *

Top = Circuit()

FGIsland = Island(Top)
Drainlines = Bus(Top,4)

# Cells
VMM_Indirect = TSMC350nm_4x2_Indirect(Top,FGIsland,Vd_P = Drainlines)
VMM_Indirect.place([0,0])

VMM_Direct = TSMC350nm_4x2_Direct(Top,FGIsland,Vd = Drainlines)
VMM_Direct.place([0,1])

TA_NoFG = TSMC350nm_TA2Cell_NoFG(Top,FGIsland, VD_P = Drainlines[0:2])
TA_NoFG.place([0,2])

VMMWTA = TSMC350nm_VMMWTA(Top,FGIsland,Vd = Drainlines)
VMMWTA.place([0,3])

TA_Weak = TSMC350nm_TA2Cell_Weak(Top,FGIsland,VD_P = Drainlines[0:2])
TA_Weak.place([0,4])

TA_Strong = TSMC350nm_TA2Cell_Strong(Top,FGIsland,VD_P = Drainlines[0:2])
TA_Strong.place([0,5])

TA_LongL = TSMC350nm_TA2Cell_LongL_Cab(Top,FGIsland,VD_P= Drainlines[0:2])
TA_LongL.place([0,6])


# Programming Infrastructure
DrainDecoder = STD_DrainDecoder(Top,FGIsland,bits=2)
DrainSel = STD_DrainSelect(Top,FGIsland,num=1)
DrainSwitches = STD_DrainSwitch(Top,FGIsland,1)

GateDecoder = STD_IndirectGateDecoder(Top,FGIsland,bits=4)
GateSWC = STD_GateMuxSWC(Top,FGIsland,num=7)

for i in range(7):
    if i != 1:
         STD_IndirectGateSwitch(Top,FGIsland,col=i)

# Compilation
#-------------------------------------------------------------------------------
design_limits = [10e6, 610e5]
#location_islands = ((20600, 363500), (20600, 20000)) #<-location for tile v1
location_islands = None

compile_asic(Top,process="TSMC350nm",fileName="small_fg_island_python",p_and_r = True,design_limits = design_limits, location_islands = location_islands)