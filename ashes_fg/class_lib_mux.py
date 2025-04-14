from ashes_fg.asic.asic_compile import *



class frame(StandardCell):
    def __init__(self,circuit):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.pinLayer = "METAL3"

        self.name = "tile_analog_frame"

    def createPort(self,direction,name = None,metal = None,connection=None):
        newPort = Port(self.circuit,self,name,direction,1,static=True)

        if connection != None:
            newPort.connect(connection)
       
    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = self.name + " " + "cab_frame("
        text += ".pin_layer()" + self.pinLayer + ")"
        pNum = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ","
                text += "." + port.direction + "_" 
                if port.name == None:
                    text += "p" + str(pNum)
                    pNum += 1
                else:
                    text += port.name
                text += "("
                text += port.pin[0].print()
                text += ")"
        text += ");"
        
        return text



class STD_GorS_IndirectSwitches(StandardCell):
    def __init__(self,circuit,island=None,num=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (1,self.num)
        self.decoder = True

        self.name = "TSMC350nm_GorS_IndrctSwcs"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = self.name + " switch("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(horizontal), "
        text += ".num(" + str(self.num) + ")"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.printFlat(type = "switch")
                i+=1
        text += ");"
        return text


class STD_IndirectGateDecoder(StandardCell):
    def __init__(self,circuit,island=None,bits=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = 2**(bits)/4
        self.bits = bits
        self.dim = (1,self.num)
        self.decoder = True

        self.name = "TSMC350nm_VinjDecode2to4_htile"

        self.VGRUN = Port(circuit,self,"VGRUN","N",4*self.dim[1])
        self.Run_Out = Port(circuit,self,"RUN_OUT","S",4*self.dim[1])
        self.Out = Port(circuit,self,"OUT","S",4*self.dim[1])
        self.Enable = Port(circuit,self,"ENABLE","N",1,static=True)
        #self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        #self.GND = Port(circuit,self,"GND","N",2*self.dim[1])
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = self.name + " decoder("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(horizontal), "
        text += ".bits(" + str(self.bits) + ")"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.printFlat()
                i+=1
        text += ");"
        return text
    
class STD_GateMuxSWC(StandardCell):
    def __init__(self,circuit,island=None,num=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (1,self.num)
        self.decoder = True

        self.name = "TSMC350nm_GateMuxSwcTile"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = self.name

        text += " switch("
 
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

    
class STD_IndirectGateSwitch(StandardCell):
    def __init__(self,circuit,island=None,num=0,col=-1):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (1,self.num)
        self.col = col
        self.decoder = True

        self.name = "TSMC350nm_IndirectSwitches"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def print(self,instanceNum,islandNum,row,col,processPrefix):
        text = self.name
        if self.col < 0:
            text += " switch("
        else:
            text += " switch_ind("

        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(horizontal), "

        if self.col < 0:
            text += ".num(" + str(self.num) + ")"
        else:
            text += ".col(" + str(self.col) + ")"

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
        self.decoder = True

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
    def __init__(self,circuit,island=None,num=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (1,self.num)
        self.decoder = True

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
    def __init__(self,circuit,island=None,num=0,VINJ=None,GND=None,Drainlines = None):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (1,self.num)
        self.decoder = True
 
        self.name = "FourTgate_ThickOx_FG_MEM"
        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])
        self.Drainlines = Port(circuit,self,"B","E",4*num)

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