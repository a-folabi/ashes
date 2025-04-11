import ashes_fg as af
from ashes_fg.examples import the_small_asic_v2

import os
import shutil

test_project = 'small_fg_island'
test_path = os.path.join('.', test_project, 'verilog_files')
# create a working directory for project. 
if not os.path.exists(test_path):
    os.makedirs(test_path)

# copy over the verilog file
shutil.copy(os.path.join('.', 'example_verilog', f'{test_project}.v'), test_path)

# All units in nanometers
tech_process = 'vis350'
cell_pitch = 22000
dbu = 1000
track_spacing = 1400
# placement offset to make space for pin routing
x_offset, y_offset = 400*track_spacing, 2000*track_spacing 
location_islands = None

design_area = (0, 0, 1e6, 6.1e5, x_offset, y_offset)
location_islands = ((20600, 363500), (20600, 20000)) #<-location for tile v1

af.asic.compile(the_small_asic_v2, 
project_name=test_project, 
tech_process=tech_process, 
dbu=dbu, 
track_spacing=track_spacing,
cell_pitch=cell_pitch,
x_offset=x_offset, y_offset=y_offset,
design_area=design_area,
location_islands=location_islands)

