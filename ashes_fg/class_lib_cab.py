from ashes_fg.asic.asic_compile import *


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

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)