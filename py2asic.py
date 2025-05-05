import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *

#------------------------------CAB merge procedure:
#------------------------------cd into example_json and "python json2py.py" (to make cab1 and cab2 python files)
#------------------------------cd .., uncomment line 17 and 18, comment line 20, "python py2asic.py" (to make cab1 and cab2 gds files)
#------------------------------cd into example_json and "python cab_merge.py" (copy the gds into vis350 library as a cell, then produce Fabric.py)
#------------------------------cd .., comment line 17 and 18, uncomment line 20, "python py2asic.py" (place Fabric.py to make a final fabric)


exec(open("./example_json/cab1.py").read())
exec(open("./example_json/cab2.py").read())
#exec(open("~/ashes/example_json/cab_merge.py").read())
#exec(open("./example_json/Fabric.py").read())

#exec(open("./example_python/small_cab_example.py").read())

#exec(open("./example_python/VMMWTA.py").read())

#exec(open("./example_python/ALICE_Example.py").read())

#exec(open("./example_python/small_fg_island.py").read())

#exec(open("./example_python/LPF_MeadSOS.py").read())

"""
Top = Circuit()
testIsland = Island(Top)
C_EW = IndirectVMM(Top,dim=[4,4],island=testIsland,decoderPlace=False)

testIsland2 = Island(Top)
testVMM2 = IndirectVMM(Top,dim=[4,4],island=testIsland2,decoderPlace=False)
CAB_GateSwitch = STD_GorS_IndirectSwitches(Top,testIsland2,num=2)

C_EW.GND_b[0] += CAB_GateSwitch.Input[1]

#C_EW.Vs[0] += CAB_GateSwitch.Input[3]
C_EW.Vs_b[2] += CAB_GateSwitch.Input[3]


# Compilation
#-------------------------------------------------------------------------------
design_limits = [1e6, 6.1e5]
location_islands = ((20600, 363500), (20600, 20000))


compile_asic(Top,process="TSMC350nm",fileName="test_code",p_and_r = True,design_limits = design_limits, location_islands = location_islands)

"""
