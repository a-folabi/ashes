import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *


Top = Circuit()

VMMWTACircuit = VMMWTA(Top,[16,16])


design_limits = [1e6, 6.1e5]
location_islands=None

compile_asic(Top,process="TSMC350nm",fileName="VMMWTA_Example",p_and_r = True,design_limits = design_limits, location_islands = location_islands)