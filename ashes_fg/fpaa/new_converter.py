import ast
import inspect
import ashes_fg.fpaa.table_class as table_class
import re
import ashes_fg.class_lib_ext as fg
from typing import KeysView, List
import numpy as np
import sys
import os

custom_import = ["import ashes_fg.class_lib as fg"]
# to save v_code separately and eventually put them together in v_code
inout_module_list = []
module_v_code_list = []
v_code = ""

st = table_class.symbolTable()
# re
in_out_re = r"fg.inpad|fg.outpad|fg.dc_in|fg.gpio_in|fg.gnd"

# converting templates
inpad_pat = '''
module pad_in();
output %s;
assign pad_num = %s;
endmodule
'''

outpad_pat = '''
module pad_out();
input %s;
assign pad_num = %s;
endmodule
'''

outpada_pat = '''
module pad_outa();
input %s;
assign pad_num = %s;
endmodule
'''

## modified
dc_in_pat = '''
module dc_in();
output %s;
assign parameter = %s;
assign fix_loc_enabled = %s;
assign fix_loc_x = %s;
assign fix_loc_y = %s;
endmodule
'''

gpio_in_pat = '''
module goin_in();
output %s;
endmodule
'''
module_list = []


# pase root node recursively to construct verilog syntax
def parse_py(node):
    print("start parsing")
    if isinstance(node, ast.Module):
        for b in node.body:
        	print(ast.dump(b))
        	print("\n")
        	mod_obj = parse_py(b)
        return mod_obj
    if isinstance(node, ast.FunctionDef):
        mod_obj = table_class.module_ast(node.name, board_type="FPAA")
        for b in node.body:
            mod_obj = module_parse(b, mod_obj)
            print("mod_obj after module_parse in FunctionDef:\n\n", vars(mod_obj))
        return mod_obj
    # construct verilog code


def module_parse(node, mod):
    for lib in custom_import:
        exec(lib)
    code = ast.unparse(node)
    if isinstance(node, ast.Assign):
        target = ast.unparse(node.targets)
        # deal with none fg situation
        if 'nmirror_w_bias' in code:
            mod.submod[target] = fg.nmirror_w_bias(target)
            mod.executedVariable.append('%s=\'%s\'' % (target, target))
            add_net(target)

            return mod
        if "fg." not in code:  # not a object to convert to verilog
            if isinstance(node.value, ast.List):
                # this is to construct input list
                proess_list_value(mod, ast.unparse(node.targets),
                                  node.value.elts)
                t_exec = target + '=' + str(mod.submod[target])
                mod.executedVariable.append(t_exec)
            return mod
        # else:
        #     mod.executedVariable.append('%s=\'%s\'' % (target, target))
        # prepare target and already executed context
        for c in mod.executedVariable:
            exec(c)
        exec(code)
        # solve vector
        try:
            mod.vec_slice[target] = [
                ast.unparse(node.value.args[0].slice.upper),
                ast.unparse(node.value.args[0].slice.lower)
            ]
            exec('%s.input=%s' % (target, node.value.args[0].value.id))

        except BaseException:
            pass
        if re.findall(in_out_re, code):  # find in_out_module
            mod.in_out_submod[target] = eval(target)
            mod.submod[target] = eval(target)
        else:  # regular modules
            tar_ins = eval(target)
            if isinstance(tar_ins, list):
                all_net = []
                for i in node.targets[0].elts:
                    mod.executedVariable.append('%s=\'%s\'' % (i.id, i.id))
                    all_net.append(add_net(i.id))
                mod.submod[target] = tar_ins[0]
                st.net_table[target] = all_net

            else:
                mod.submod[target] = tar_ins
                add_net(target)
        if isinstance(eval(target), list):
            pass
        else:
            mod.executedVariable.append('%s=\'%s\'' % (target, target))
    elif isinstance(node, ast.Return):
        pass
    return mod


def construct_in_out_module(mod):
    for sub_m in mod.in_out_submod:
        if isinstance(mod.in_out_submod[sub_m], fg.inpad):
            t_net = add_net(sub_m)
            if isinstance(mod.in_out_submod[sub_m].pad_number, list):
                if len(mod.in_out_submod[sub_m].pad_number) > 1:
                    st.net_table[sub_m] = t_net
                    net_to_rep = "[%s:0] %s" % (
                        len(mod.in_out_submod[sub_m].pad_number) - 1, t_net)
                    module_v_code_list.append(
                        inpad_pat %
                        (net_to_rep, str(
                            mod.in_out_submod[sub_m].pad_number).replace(
                                ' ', '')))
                else:
                    module_v_code_list.append(inpad_pat % (t_net, '%s' % str(
                        mod.in_out_submod[sub_m].pad_number).replace(' ', '')))
            else:
                module_v_code_list.append(inpad_pat % (t_net, '[%d]' % str(
                    mod.in_out_submod[sub_m].pad_number).replace(' ', '')))

        elif isinstance(mod.in_out_submod[sub_m], fg.outpad) or isinstance(
                mod.in_out_submod[sub_m], fg.outpada):
            if isinstance(mod.in_out_submod[sub_m], fg.outpad):
                t_pat = outpad_pat
            else:
                t_pat = outpada_pat
            outpad_input = mod.in_out_submod[sub_m].input
            t_net = add_net(outpad_input)
            if isinstance(mod.in_out_submod[sub_m].pad_number, list):
                if len(mod.in_out_submod[sub_m].pad_number) > 1:
                    st.net_table[sub_m] = t_net
                    net_to_rep = "[%s:0] %s" % (
                        len(mod.in_out_submod[sub_m].pad_number) - 1, t_net)
                else:
                    net_to_rep = t_net
                module_v_code_list.append(
                    t_pat %
                    (net_to_rep, str(
                        mod.in_out_submod[sub_m].pad_number).replace(' ', '')))
            else:
                module_v_code_list.append(t_pat % (t_net, "[%d]" % str(
                    mod.in_out_submod[sub_m].pad_number).replace(' ', '')))
        elif isinstance(mod.in_out_submod[sub_m], fg.dc_in):
            t_net = add_net(sub_m)
            module_v_code_list.append(
                dc_in_pat % (t_net, mod.in_out_submod[sub_m].DC_value, mod.in_out_submod[sub_m].fix_loc_enabled, mod.in_out_submod[sub_m].fix_loc_x, mod.in_out_submod[sub_m].fix_loc_y)) ## modified ##
        elif isinstance(mod.submod[sub_m], fg.gpio_in):
            t_net = add_net(sub_m)
            module_v_code_list.append(gpio_in_pat % (t_net))


def construct_module(mod):
    for (i, sub_m) in enumerate(mod.submod):
        try:
            num_ins = int(mod.submod[sub_m].num_instances)
        except AttributeError:
            num_ins = 1
        inputalias = ''
        if sub_m in mod.in_out_submod:
            continue  # if sub_m also in in_out_submod, we already constructed before, so continue
        if isinstance(mod.submod[sub_m], list) or isinstance(
                mod.submod[sub_m], fg.gnd):
            pass
        else:
            # module input generation
            module_v_code_list.append('\nmodule ' +
                                      mod.submod[sub_m].__class__.__name__ +
                                      '();\n')
            inputalias = construct_module_input(mod, sub_m, num_ins)
            module_v_code_list.append(inputalias)
            # module output generation:
            construct_module_output(mod, sub_m, num_ins)

            for key in mod.submod[sub_m].__dict__.keys():
                if key == 'input':
                    pass
                elif key == 'num_instances':
                    module_v_code_list.append(
                        "assign block_num = " +
                        str(eval('mod.submod[sub_m].%s' % key)) + ';\n')
                else:
                    to_assign = eval('mod.submod[sub_m].%s' % key)
                    # if a vector but this assign is default value(only one not a list)
                    if isinstance(to_assign, str) and num_ins > 1:
                        broadCast_assign = []
                        for i in range(num_ins):
                            broadCast_assign.append(to_assign)
                        to_assign = broadCast_assign
                    module_v_code_list.append("assign " + key + ' = ' +
                                              str(to_assign).replace(' ', '') +
                                              ';\n')

            module_v_code_list.append('endmodule\n')
    return v_code


def add_net(name):
    if name in st.net_table:  # already exsist
        return st.net_table[name]
    else:
        st.net_table[name] = 'net%i' % (st.netnum)
        st.netnum += 1
        return st.net_table[name]


def proess_list_value(mod, tar_name, node_list):
    mod.submod[tar_name] = []
    for i in node_list:
        for key in mod.in_out_submod.keys():
            if i.id == key:
                mod.submod[tar_name].append(key)
                break
        for key in st.net_table.keys():
            if i.id == key:
                mod.submod[tar_name].append(key)
                break


def construct_module_input(mod, sub_m, num_ins=1):
    inputalias = ''
    if isinstance(mod.submod[sub_m].input, list):
        for i in mod.submod[sub_m].input:
            if i == 'gnd':
                if num_ins != 1:
                    inputalias += 'input [%d:%d] gnd;\n' % (num_ins - 1, 0)
                else:
                    inputalias += 'input gnd;\n'
                continue
            if isinstance(mod.submod[sub_m], fg.vmm_12x4):
                inputalias += 'input [%d:%d] %s;\n' % (3, 0, st.net_table[i])
            elif num_ins == 1 or isinstance(mod.submod[sub_m], fg.c4_sp):
                inputalias += 'input %s;\n' % st.net_table[i]

            elif num_ins > 1:
                inputalias += 'input [%d:%d] %s;\n' % (num_ins - 1, 0,
                                                       st.net_table[i])

    else:
        nn = add_net(mod.submod[sub_m].input)
        try:  # try if the modue has num_instances
            if num_ins > 1:
                inputalias += 'input [%s:0] %s;\n' % (num_ins - 1, nn)
            else:
                try:
                    slice = mod.vec_slice[sub_m]
                    inputalias += 'input [%d:%s] %s;\n' % (int(slice[0]) - 1,
                                                           slice[1], nn)
                except BaseException:
                    inputalias += 'input %s;\n' % nn
        except BaseException:
            inputalias += 'input %s;\n' % nn

        if isinstance(mod.submod[sub_m], fg.nmirror_w_bias):
            inputalias += inputalias
    return inputalias


def construct_module_output(mod, sub_m, num_ins):
    if sub_m in st.net_table:
        if isinstance(st.net_table[sub_m], list):
            for i in st.net_table[sub_m]:
                if num_ins > 1:
                    module_v_code_list.append("output [%s:0] %s;\n" %
                                              (num_ins - 1, i))
                else:
                    module_v_code_list.append("output %s;\n" % i)
        else:
            try:
                if isinstance(mod.submod[sub_m], fg.vmm_12x4):
                    module_v_code_list.append('output [%d:%d] %s;\n' %
                                              (3, 0, st.net_table[sub_m]))
                elif num_ins > 1:
                    module_v_code_list.append(
                        "output [%s:0] %s;\n" %
                        (num_ins - 1, st.net_table[sub_m]))
                else:
                    module_v_code_list.append("output %s;\n" %
                                              st.net_table[sub_m])
            except:
                module_v_code_list.append("output %s;\n" % st.net_table[sub_m])


def fpaa_compile(funcName):
    """
    Returns the verilog code after conversion.
    
    The entry function of the system-level compiler.
    """
    global v_code, inout_module_list, module_v_code_list
    inout_module_list = []
    module_v_code_list = []
    v_code = ""
    try:
        func = inspect.getsource(funcName)
    except TypeError:
        with open(funcName, 'r') as f:
            func = f.read()
    if "flag_std_lib." in func:
        func = func.replace("flag_std_lib.", "fg.")
    root = ast.parse(func)
    print("PARSED MODULE\n\n")
    print(ast.dump(root))
    print("END PARSED MODULE\n\n")
    m = parse_py(root)
    v_code += "module %s();\n" % (m.mod_name)
    construct_in_out_module(m)
    construct_module(m)
    v_code += "endmodule\n"
    for i in module_v_code_list:
        v_code += i
    v_code += '\n'
    print("V code is... \n\n")
    print(v_code)
    return v_code

if __name__ == "__main__":
    n = len(sys.argv)

    assert n == 3, "Should pass in at least 3 args, format should be: python new_converter.py $inputFileName $outputPath "
    ifFile=1
    fpaa_compile(sys.argv[1], sys.argv[2], ifFile)
