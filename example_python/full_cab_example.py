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

C_EW = IndirectVMM(Top,[20,14],island=BlockIsland,decoderPlace=False)

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


C_NS = IndirectVMM(Top,[20,18],island=BlockIsland,decoderPlace=False,loc = [0,17])


# Compilation
#-------------------------------------------------------------------------------
design_limits = [1e6, 6.1e5]
#location_islands = ((20600, 363500), (20600, 20000)) #<-location for tile v1
location_islands=None


compile_asic(Top,process="TSMC350nm",fileName="full_cab_python",p_and_r = True,design_limits = design_limits, location_islands = location_islands)