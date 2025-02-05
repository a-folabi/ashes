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

af.asic.compile(the_small_asic_v2, project_name=test_project)