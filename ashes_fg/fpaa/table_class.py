# - first prototype (9/26/2022)
# 1. modules, should be inherited from a basic class, say: std_block.
# they all have an in order argument input: (input,cell_type,instance.num)
# 2. if it's inpad or outpad, the argument list will be different.
# and should be calling a function: inpad.makepad(inpadnumber,padvalue),
#  output(outputvalue,outsize,'fpaa' or 'asic')
# 3. to ask, are we still keeping "fpaa" and 'asic'?


class module_ast():
    def __init__(self, mod_name, board_type='FPAA'):
        self.mod_name = mod_name
        self.board_type = board_type
        self.submod = {}
        self.in_out_submod = {}
        self.executedVariable = []
        self.vec_slice = {}


# symbol table
class symbolTable():
    def __init__(self):
        self.module_list = []
        self.module_v_code_list = []
        self.import_lib = {}
        self.net_table = {}
        self.temp_var = {}
        self.netnum = 1  # accumulative net number, from 0
