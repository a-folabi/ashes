from ashes_fg.asic.asic_compile import *


class TSMC350nm_volatile_swcs(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "TSMC350nm_volatile_swcs"
        
        self.out = Port(circuit,self,"out","N",2*self.dim[1])
        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.Vsel = Port(circuit,self,"Vsel","N",2*self.dim[1])
        self.Vg = Port(circuit,self,"Vg","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",1*self.dim[1])
        self.VTUN = Port(circuit,self,"VTUN","N",1*self.dim[1])
        self.D = Port(circuit,self,"D","W",1*self.dim[0])
        self.CLK = Port(circuit,self,"CLK","W",1*self.dim[0])
        self.Q = Port(circuit,self,"Q","E",1*self.dim[0])
        self.com = Port(circuit,self,"com","W",1*self.dim[0])
        self.VDD = Port(circuit,self,"VDD","W",1*self.dim[0])
        self.Vd_P = Port(circuit,self,"Vd_P","W",1*self.dim[0])
        self.Vd_in = Port(circuit,self,"Vd_in","W",8*self.dim[0])
        self.Vd_o = Port(circuit,self,"Vd_o","E",8*self.dim[0])
        
        
        circuit.addInstance(self,self.island)


# SBLOCK
#---------------------------------------------------------------------------------------------------
class S_Buffer(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_BUFFER"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_spaceUP(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_SPACE_UP_PINS"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class S_spaceDOWN(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_SPACE_DOWN_PINS"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class S_Conn12(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_CONN_PINS"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class S_Conn23(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_23CONN"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_SEC1(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_SEC1_PINS"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])
        self.VINJ_b = Port(circuit,self,"VINJ_b","S",1*self.dim[1])
        self.Vsel_b = Port(circuit,self,"Vsel_b","S",2*self.dim[1])
        self.Vg_b = Port(circuit,self,"Vg_b","S",2*self.dim[1])
        self.VTUN_b = Port(circuit,self,"VTUN_b","S",1*self.dim[1])
        self.GND_b = Port(circuit,self,"GND_b","S",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_SEC2(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_SEC2_PINS"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])
        self.VINJ_b = Port(circuit,self,"VINJ_b","S",1*self.dim[1])
        self.Vsel_b = Port(circuit,self,"Vsel_b","S",2*self.dim[1])
        self.Vg_b = Port(circuit,self,"Vg_b","S",2*self.dim[1])
        self.VTUN_b = Port(circuit,self,"VTUN_b","S",1*self.dim[1])
        self.GND_b = Port(circuit,self,"GND_b","S",2*self.dim[1])


        # Add cell to circuit
        circuit.addInstance(self,self.island)

class S_SEC3(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "S_BLOCK_SEC3_PINS"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])
        self.VINJ_b = Port(circuit,self,"VINJ_b","S",1*self.dim[1])
        self.Vsel_b = Port(circuit,self,"Vsel_b","S",2*self.dim[1])
        self.Vg_b = Port(circuit,self,"Vg_b","S",2*self.dim[1])
        self.VTUN_b = Port(circuit,self,"VTUN_b","S",1*self.dim[1])
        self.GND_b = Port(circuit,self,"GND_b","S",2*self.dim[1])


        # Add cell to circuit
        circuit.addInstance(self,self.island)

# SWITCHES
#---------------------------------------------------------------------------------------------------

class ST_BMatrix(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "TSMC350nm_4TGate_ST_BMatrix"

        self.In = Port(circuit,self,"Input","W",4*self.dim[0])
        self.P = Port(circuit,self,"P","E",4*self.dim[0])
        self.A = Port(circuit,self,"A","E",4*self.dim[0])

        # Add cell to circuit
        circuit.addInstance(self,self.island)
       
class ST_BMatrix_NoSwitch(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "TSMC350nm_4TGate_ST_BMatrix_NoSwitch"

        self.In = Port(circuit,self,"Input","W",4*self.dim[0])
        self.P = Port(circuit,self,"P","E",4*self.dim[0])
        self.A = Port(circuit,self,"A","E",4*self.dim[0])

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class DrainCutoff(MUX):
    def __init__(self,circuit,island=None,num=1):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (self.num,0)
        self.decoder = True
        self.type = "switch"
        self.switchType = "prog_switch"
 
        self.name = "TSMC350nm_4TGate_ST_draincutoff"
        
        self.PR = Port(circuit,self,"PR","E",4*self.dim[0])
        self.In = Port(circuit,self,"In","E",4*self.dim[0])

        # Add cell to circuit
        circuit.addInstance(self,self.island)


# Special FG Selects
#---------------------------------------------------------------------------------------------------
class BlockTop(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "TSMC350nm_4x2_Indirect_top_AorB_matrx"

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class B_bot(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim

        self.name = "TSMC350nm_4x2_Indirect_bot_B_matrx"

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class OutSwitch(StandardCell):
    def __init__(self,circuit,island=None,dim = (1,1)):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim
        
        self.Vgrun_r = Port(circuit,self,"Vgrun_r","E",1*self.dim[0])
        self.AVDD_r = Port(circuit,self,"AVDD_r","E",1*self.dim[0])
        self.run_r = Port(circuit,self,"run_r","E",1*self.dim[0])
        self.prog_r = Port(circuit,self,"prog_r","E",1*self.dim[0])

        self.name = "TSMC350nm_OutMtrx_IndrctSwcs"
        
        

        # Add cell to circuit
        circuit.addInstance(self,self.island)
