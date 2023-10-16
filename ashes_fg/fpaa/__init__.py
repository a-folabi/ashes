# expose the function compile that pushes from python down to blif
import ashes_fg.fpaa.new_converter as nc
import ashes_fg.fpaa.verilog2blif as vb
import os

def compile(system):
    verilog = nc.fpaa_compile(system)
    vb.v2blif(verilog, '.')