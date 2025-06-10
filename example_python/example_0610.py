import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *


Top = Circuit()

C4Island = Island(Top)
C4 = TSMC350nm_C4(Top,C4Island,[12,1])
C4.place([0,0])


AmpDetectIsland = Island(Top)
AmpDetect = TSMC350nm_Ampdet_NoFG(Top,AmpDetectIsland,[12,1])
AmpDetect.place([0,0])

LadderIsland = Island(Top)
Ladder = TSMC350nm_DelayBlock_3stage_new(Top,LadderIsland,[12,1])
Ladder.place([0,0])

C4.OUTPUT += AmpDetect.VIN
AmpDetect.OUTPUT += Ladder.VIN

#Classifier = VMMWTA(Top,[36,36],inputs = Ladder.VOUT)

outerPins = frame(Top)
outerPins.createPort("N","Vg_0",connection=C4.Vg[0])
C4.Vg[0] += AmpDetect.Vg
outerPins.createPort("N","C4_in0",connection=C4.VIN[0])
outerPins.createPort("N","C4_ref0",connection=C4.VREF[0])
outerPins.createPort("N","C4_in1",connection=C4.VIN[1])
outerPins.createPort("N","C4_ref1",connection=C4.VREF[1])

# Compilation
#-------------------------------------------------------------------------------
design_limits = [2e6, 2e6]
island_space = 250000
location_islands = ((1000, 500000), (1000+island_space, 500000), (1000+2*island_space,500000)) #<-location for tile v1
#location_islands=None


compile_asic(Top,process="TSMC350nm",fileName="example_0610",p_and_r = True,design_limits = design_limits, location_islands = location_islands)
