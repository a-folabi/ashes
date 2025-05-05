# -*- coding: utf-8 -*-
"""
Created on Fri May  2 19:06:07 2025

@author: lyang
"""

import json
import os

with open('cell2cell_350nm.json','r') as file:
    data = json.load(file)
    
cab_list = []
for general_info in data:
    foundry=data["foundry"]
    process_node=data["process_node"]
    if "cab" in general_info and "_" not in general_info:
        cab_list.append(general_info)
        
        
for cab in cab_list:
    src = os.path.expanduser(f"~/ashes/{cab}/{cab}_merged.gds")
    dst = os.path.expanduser(f"~/ashes/{cab}/{cab}.gds")
    os.rename(src, dst)
    source_file = "~/ashes/"+cab+"/"+cab+".gds"
    dest_file = "~/ashes/ashes_fg/asic/lib/gds/vis350/"+cab+".gds"
    os.system(f"cp {source_file} {dest_file}")
    
    
f = open('Fabric.py','w')
f.write("import ashes_fg as af\n")
f.write("from ashes_fg.asic.asic_compile import *\n")
f.write("from ashes_fg.class_lib_new import *\n")
f.write("from ashes_fg.class_lib_mux import *\n")
f.write("from ashes_fg.class_lib_cab import *\n")
f.write("from ashes_fg.asic.asic_systems import *\n")
f.write("Top = Circuit()\n")
f.write("FabricIsland = Island(Top)\n")


for cab in cab_list:
    for i in data["col_"+cab]:
        f.write("col"+str(i)+" = "+cab+"(Top,FabricIsland,[7,1])\n")
        f.write("col"+str(i)+".place([0,"+str(i-1)+"])\n")
        
f.write("design_limits = [1e7, 6.1e6]\n")
f.write("location_islands = None\n")
f.write('compile_asic(Top,process="TSMC350nm",fileName="Fabric",p_and_r = True,design_limits = design_limits, location_islands = location_islands)\n')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

