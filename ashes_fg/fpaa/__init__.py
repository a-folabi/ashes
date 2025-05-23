# expose the function compile that pushes from python down to blif
import ashes_fg.fpaa.new_converter as nc
import ashes_fg.fpaa.verilog2blif as vb
import ashes_fg.fpaa.gen_pads_30a
import ashes_fg.fpaa.gen_pads_30
import ashes_fg.fpaa.blif_to_switches as bs
import ashes_fg.fpaa.program_fpaa as pf
from ashes_fg.fpaa.Make_ProgramList_CompileAssembly import compile as ca

import os

def compile(system, project_name, chip_num, board_type = '3.0a'):
    out_path = os.path.join('.', project_name)
    if not os.path.exists(out_path): os.mkdir(out_path)
    verilog = nc.fpaa_compile(system)
    vb.v2blif(verilog, out_path)
    sys_name = os.path.join(out_path, system.__name__)
    if board_type == '3.0a':
    	gen_pads_30a.gen_pads_30a(sys_name,verilog,project_name)
    elif board_type == '3.0':
    	gen_pads_30.gen_pads_30(sys_name,project_name)
    bs.blif2swcs(sys_name, project_name, board_type, out_path)
    ca(project_name, board_type, chip_num)
    os.chdir(f'{out_path}')
    pf.main()
