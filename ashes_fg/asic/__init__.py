from ashes_fg.asic.py_to_verilog import asic_compiler
from ashes_fg.asic.verilog_to_gds import gds_synthesis

def compile(system, project_name=None, tech_process='privA_65', dbu=1000, track_spacing=250, x_offset=None, y_offset=None, design_area=(0,0,1,1)):
    asic_compiler(system, project_name)
    
    # All units in nanometers
    tech_process = 'privA_65'
    dbu = 1000
    track_spacing = 250
    # placement offset to make space for pin routing
    x_offset = 500*2*track_spacing 
    y_offset = 15*2*track_spacing
    design_area = (20.5e4, 21.76e4, 120e4, 34e4, x_offset, y_offset)
    gds_synthesis(tech_process, dbu, track_spacing, x_offset, y_offset, design_area, project_name)
    