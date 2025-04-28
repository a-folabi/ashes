import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *



#exec(open("./example_json/full_cab_python_two.py").read())

#exec(open("./example_python/small_cab_example.py").read())

#exec(open("./example_python/VMMWTA.py").read())

#exec(open("./example_python/ALICE_Example.py").read())

#exec(open("./example_python/small_fg_island.py").read())

#exec(open("./example_python/LPF_MeadSOS.py").read())

Top = Circuit()
testIsland = Island(Top)
testVMM = IndirectVMM(Top,[4,4],testIsland,decoderPlace=False)
swc = STD_GorS_IndirectSwitches(Top,testIsland,num=2)

testIsland2 = Island(Top)
testVMM2 = TSMC350nm_4x2_Indirect(Top,testIsland2,(1,2))
testVMM2.place((0,0))

testVMM2.VTUN += swc.VTUN
testVMM2.Vd_R += swc.Input

# Compilation
#-------------------------------------------------------------------------------
design_limits = [1e6, 6.1e5]
location_islands=None


compile_asic(Top,process="TSMC350nm",fileName="test_code",p_and_r = True,design_limits = design_limits, location_islands = location_islands)