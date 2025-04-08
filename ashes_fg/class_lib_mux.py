from ashes_fg.asic.asic_compile import *


class STD_GateDecoder(StandardCell):
    def __init__(self,circuit,island=None,bits=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = 2**(bits-1)
        self.bits = bits
        self.dim = (self.num,1)

        self.name = "VinjDecode2to4_htile"

        self.VGRUN = Port(circuit,self,"VGRUN","N",2**bits)
        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = processPrefix + "_" + self.name + " decoder("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(horizontal), "
        text += ".bits(" + str(self.bits) + ")"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.print()
                i+=1
        text += ");"
        return text
    
class STD_IndirectGateSwitch(StandardCell):
    def __init__(self,circuit,island=None,bits=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = 2**(bits-1)
        self.dim = (self.num,1)

        self.name = "GateMuxSwcTile"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = processPrefix + "_" + self.name + " switch("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(horizontal), "
        text += ".num(" + str(self.num) + ")"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.print()
                i+=1
        text += ");"
        return text


class STD_DrainDecoder(StandardCell):
    def __init__(self,circuit,island=None,bits=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.bits = bits
        self.num = 2**(bits-2)
        self.dim = (1,self.num)

        self.name = "VinjDecode2to4_vtile"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = processPrefix + "_" + self.name + " decoder("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(vertical), "
        text += ".bits(" + str(self.bits) + ")"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.print()
                i+=1
        text += ");"
        return text

class STD_DrainSelect(StandardCell):
    def __init__(self,circuit,island=None,bits=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = 2**(bits-2)
        self.dim = (1,self.num)

        self.name = "drainSelect01d3"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = processPrefix + "_" + self.name + " switch("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(vertical), "
        text += ".num(" + str(self.num) + "), "
        text += ".type(drain_select)"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.print()
                i+=1
        text += ");"
        return text

class STD_DrainSwitch(StandardCell):
    def __init__(self,circuit,island=None,bits=0,VINJ=None,GND=None,Drainlines = None):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = 2**(bits-2)
        self.dim = (1,self.num)
 
        self.name = "FourTgate_ThickOx_FG_MEM"
        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])
        self.Drainlines = Port(circuit,self,"B","E",2**bits)

        # Initialize ports with given values
        portsInit = [VINJ,GND,Drainlines]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = processPrefix + "_" + self.name + " switch("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(vertical), "
        text += ".num(" + str(self.num) + "), "
        text += ".type(prog_switch)"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.print()
                i+=1
        text += ");"
        return text