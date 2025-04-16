import ashes_fg as af

from ashes_fg.asic.asic_compile import *
from ashes_fg.class_lib_new import *
from ashes_fg.class_lib_mux import *
from ashes_fg.class_lib_cab import *

from ashes_fg.asic.asic_systems import *


Top = Circuit()

exec(open("./example_python/full_cab_example.py").read())

#exec(open("./example_python/small_cab_example.py").read())

#exec(open("./example_python/VMMWTA.py").read())