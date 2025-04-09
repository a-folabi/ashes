import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *

from ashes_fg.asic.asic_systems import *


Top = Circuit()

Vd0 = DirectVMM(Top,16,16)
Vd1 = DirectVMM(Top,16,16,inputs=Vd0)
#Vd1 = DirectVMM(Top,16,16)


compile_asic(Top,process="TSMC350nm",fileName="py2asic_test",p_and_r = True)

