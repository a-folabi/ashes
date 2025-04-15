from ashes_fg.asic.asic_compile import *

class MUX(StandardCell):
    def __init__(self,circuit,island,num):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (0,self.num)
        self.decoder = True
        self.type = "MUX"
        self.switchType = "MUX"
        self.name = "MUX"

        # Add cell to circuit
        circuit.addInstance(self,self.island)

    def hasSwitchType(self):
        try:
            test = self.switchType
            return True
        except:
            return False

    def print(self,instanceNum,islandNum,row,col,processPrefix):

        text = self.name + " " + self.type + "("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(" + self.getDirection() + "), "

        if self.type == "decoder":
            text += ".bits(" + str(self.bits) + ")"
        elif self.type == "switch":
            text += ".num(" + str(self.num) + ")"
        elif self.type == "switch_ind":
            text += ".col(" + str(self.col) + ")"

        if self.hasSwitchType() == True:
            text += ", .type(" + self.switchType + ")"

        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                if self.type == "switch_ind":
                    text += port.print()
                else:
                    text += port.printFlat(type = self.type)
                i+=1
        text += ");"
        return text
    
    def getDirection(self):
        if self.dim[0] < 1:
            return "horizontal"
        else:
            return "vertical"
        

class STD_GorS_IndirectSwitches(MUX):
    def __init__(self,circuit,island=None,num=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (0,self.num)
        self.decoder = True
        self.type = "switch"

        self.name = "TSMC350nm_GorS_IndrctSwcs"

        self.In = Port(circuit,self,"Input","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class STD_IndirectGateDecoder(MUX):
    def __init__(self,circuit,island=None,bits=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = 2**(bits)/4
        self.bits = bits
        self.dim = (0,self.num)
        self.decoder = True
        self.type = "decoder"

        self.name = "TSMC350nm_VinjDecode2to4_htile"

        self.VGRUN = Port(circuit,self,"VGRUN","N",4*self.dim[1])
        self.Run_Out = Port(circuit,self,"RUN_OUT","S",4*self.dim[1])
        self.Out = Port(circuit,self,"OUT","S",4*self.dim[1])
        self.Enable = Port(circuit,self,"ENABLE","N",1,static=True)
        #self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        #self.GND = Port(circuit,self,"GND","N",2*self.dim[1])
        
        # Add cell to circuit
        circuit.addInstance(self,self.island)

class STD_GateMuxSWC(MUX):
    def __init__(self,circuit,island=None,num=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (0,self.num)
        self.decoder = True
        self.type = "switch"

        self.name = "TSMC350nm_GateMuxSwcTile"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class STD_IndirectGateSwitch(MUX):
    def __init__(self,circuit,island=None,num=0,col=-1):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (0,self.num)
        self.col = col
        self.decoder = True
        self.type = "switch_ind"
        if col < 0:
            self.type = "switch"

        self.name = "TSMC350nm_IndirectSwitches"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class STD_DrainDecoder(MUX):
    def __init__(self,circuit,island=None,bits=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.bits = bits
        self.num = 2**(bits-2)
        self.dim = (self.num,0)
        self.decoder = True
        self.type = "decoder"

        self.name = "TSMC350nm_VinjDecode2to4_vtile"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class STD_DrainSelect(MUX):
    def __init__(self,circuit,island=None,num=0):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (self.num,0)
        self.decoder = True
        self.type = "switch"
        self.switchType = "drain_select"

        self.name = "TSMC350nm_drainSelect01d3"

        self.VINJ = Port(circuit,self,"VINJ","N",2*self.dim[1])
        self.GND = Port(circuit,self,"GND","N",2*self.dim[1])

        # Add cell to circuit
        circuit.addInstance(self,self.island)


class STD_DrainSwitch(MUX):
    def __init__(self,circuit,island=None,num=0,VINJ=None,GND=None,Drainlines = None):
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.num = num
        self.dim = (1,self.num)
        self.decoder = True
        self.type = "switch"
        self.switchType = "prog_switch"
 
        self.name = "TSMC350nm_FourTgate_ThickOx_FG_MEM"
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
