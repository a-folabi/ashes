# Classes and functions for compilation of ASIC python to a Verilog Netlist

import os
import shutil
import numpy as np
from ashes_fg.asic import compile
#from ashes_fg.class_lib_mux import *


# Functions
# ---------------------------------------------------------------------------------------------------------------------------
def compile_asic(circuit,process="Process",fileName = "compiled",path = "./example_verilog", p_and_r = True):
    """
    Main ASIC compilation function
    - Makes Verilog netlist for a given Circuit
    - Creates directory for physical design
    - Calls P&R tools
    """

    filePathandName = os.path.join(path,fileName+".v")
    f = open(filePathandName, "w")
    f.write(circuit.print(process))
    f.close() # Close file so that P&R can access netlist

    test_project = fileName
    test_path = os.path.join('.', test_project, 'verilog_files')
    # create a working directory for project. 
    if not os.path.exists(test_path):
        os.makedirs(test_path)

    # copy over the verilog file
    shutil.copy(os.path.join('.', 'example_verilog', f'{test_project}.v'), test_path)

    # Run P&R if desired
    if p_and_r == True:
        compile(None, project_name=test_project)


def printPlacement(island,fileName = "island_placement",path = "./"):
    """
    Debug aid for placement
    Prints island placement array to a csv file
    """
    fileName += ".csv"
    filePathandName = os.path.join(path,fileName)
    f = open(filePathandName, "w")
    f.write(island.printPlacement())

def Bus(circuit,size):
    """
    Helper function to easily create vectors of nets
    """
    return Port(circuit,None,"Bus",None,size)

def Wire(circuit):
    """
    Helper function to easily create single net
    """
    wirePort = Port(circuit,None,"Bus",None,1)
    return wirePort.pins[0]


# Classes
# ---------------------------------------------------------------------------------------------------------------------------

class Circuit:
    """
    Holds top-level information for a group of instances including
    - List of instances
    - Nets between instances
    - Instance groupings (Islands)

    """
    def __init__(self, topCircuit = None):
        # Instances (vertices in hypergraph)
        self.Instances = []

        # Nets (hyper edges)
        self.Nets = []

        # Islands (grouping of instances for placement)
        self.Islands = []
        self.DefaultIsle = Island(self)

        if topCircuit != None:
            topCircuit.add(self)

    def createIsland(self,instances):
        newIsland = Island(self,instances=instances)

    def addIsland(self,island):
        self.Islands.append(island)

    def cleanIslands(self):
        """
        Removes empty islands
        Mostly used for removing the default island
        """
        for i in self.Islands:
            if i.instances == []:
                self.Islands.remove(i)

    def addInstance(self,instance,island):
        self.Instances.append(instance)

        # Adds instance to given island or default
        if island == None:
            self.DefaultIsle.addInstances(instance)
        else:
            island.addInstances(instance)

    def placeInstance(self,instance,loc):
        instance.island.placeInstance(instance,loc)

    def addNet(self,net):
        #TODO Check if nets pins are already in another net, merge if so or throw error
        self.Nets.append(net)

    def mergeNets(self,nets):
        """
        Merges a list of nets together
        """
        newNet = Net(self)
        for n in nets:
            # Update pins from old net to point to new
            # p.move handles net <-> pin 
            for p in n.pins:
                p.move(newNet)
            # Remove old net from Circuit
            self.Nets.remove(n)

        return newNet

    def nameNets(self):
        """
        Names nets 
        - Isolated nets get a unique number
        - Nets that are part of a vector find the dominant net and name the entire vector
        """
        for net in self.Nets:
            # If net has not been assigned
            if net.number == -1:

                if net.containsVector() == True:
                    largestDim = 0
                    largestPin = None
                    # Find the dominant pin
                    for pin in net.pins:
                        if pin.getVectorSize() > largestDim:
                            largestDim = pin.getVectorSize()
                            largestPin = pin
                            
                    # Name all nets attached to that pin
                    port = largestPin.port
                    idxNum = self.Nets.index(net)
                    idx = 0
                    for p in port:
                        p.net.number = idxNum
                        p.net.index = idx
                        idx += 1

                elif net.containsVector() == False:
                    net.number = self.Nets.index(net)

 
    def print(self,processPrefix):
        """
        Creates Verilog netlist from Circuit
        """
        # Remove redundant islands
        self.cleanIslands()
        # Assign a name to each net
        self.nameNets()


        text = "module TOP(port1);\n"

        # Print island by island
        for isle in self.Islands:
            islandNum = self.Islands.index(isle)
            text += "\n\n"
            text += "\t/* Island " + str(islandNum)  + " */" + "\n"
            islandNum = self.Islands.index(isle)
            text += isle.print(islandNum,processPrefix)

        text += "endmodule"
        return text


class Island:
    """
    Defines grouping of instances and their placement
    Contains
    - Instance list
    - Placement grid (array with relative instance placement)
    """
    def __init__(self,circuit, instances = None):
        self.instances = []

        self.circuit = circuit
        self.circuit.addIsland(self)
        self.placementGrid = np.array([[]], dtype=object)

        if instances != None:
            self.addInstances(instances)

    def addInstances(self,instances):
        if isinstance(instances,list) == False:
            instances = [instances]
        
        for i in instances:
            self.instances.append(i)
            currentIsland = i.island

            # Remove instance from its current island (if applicable)
            if currentIsland != None:
                if currentIsland != self:
                    i.island.removeInstance(i)
            i.island = self


    def removeInstance(self,instance):
        self.instances.remove(instance)
    
    def indexToRow(self,index):
        """
        Placement grid addressing conversion
        Python Index -> Row number
        """
        return index + (np.shape(self.placementGrid)[0] - 1)

    def addRows(self,array,rowNum=0,numNewRows=1):
        """
        Add rows to placement grid
        """
        newRow = np.zeros((numNewRows,1))
        return np.insert(array,rowNum,newRow,axis=0)

    def addCols(self,array,colNum=1,numNewCols=1):
        """
        Add columns to placement grid
        """
        newCol = np.zeros((numNewCols,1))
        return np.insert(array,colNum,newCol,axis=1)
    
    def getLocation(self,instance):
        """
        Find the location of an instance in the placement grid    
        """
        if instance.dim[0] > 0:
            return np.where(self.placementGrid == instance)
        else:
            return np.zeros([2,2])
        
    # TODO This is probably a terrible way to do this
    def isDecoder(self,instance):
        """
        Identifies special decoder cells
        """
        decoderList = ["VinjDecode2to4_htile","GateMuxSwcTile","VinjDecode2to4_vtile","drainSelect01d3","FourTgate_ThickOx_FG_MEM"]

        for i in decoderList:
            if instance.name == i:
                return True
        return False
        
    def print(self,islandNum,processPrefix):
        """
        Create Verilog netlist for island 
        """
        decoderText = "\n \t/*Programming Mux */ \n"
        text = ""
        i = 0

        # Create Verilog for each instance
        for instance in self.instances:

            # Check if instance is a decoder (has negative dimension as indicator)
            if self.isDecoder(instance) == False:
                # Get row and column number
                instanceLocation = self.getLocation(instance)
                placedRow = instanceLocation[0][0]
                placedCol = instanceLocation[1][0]
                text += "\t"
                text += instance.print(i,islandNum,placedRow,placedCol,processPrefix)
                text += ("\n")
            elif self.isDecoder(instance) == True:
                decoderText += "\t"
                decoderText += instance.print(i,islandNum,0,0,processPrefix)
                decoderText += ("\n")
            i += 1

        # If we had a decoder, put here
        if decoderText != "\n\n \t/*Programming Mux */ \n":
            text += decoderText
        return text

    def placeInstance(self,instance,location):
        """
        Place instance inside placement grid
        Rows/Cols start at 1
        Translates 0,0 from top left of array to bottom left
        """
        rowDim = instance.dim[0]
        colDim = instance.dim[1]

        row = location[0]
        col = location[1]

        numRows = np.shape(self.placementGrid)[0]
        numCols = np.shape(self.placementGrid)[1]

        # Expand placement grid size to fit new additions
        if numRows < row+1 + rowDim-1:
           self.placementGrid = self.addRows(self.placementGrid,rowNum=numRows,numNewRows=(row+1-numRows)+rowDim-1)
        if numCols < col+1 + colDim-1:
            self.placementGrid = self.addCols(self.placementGrid,colNum=numCols,numNewCols=(col+1-numCols)+colDim-1)

        # Fill in for matrix elements
        self.placementGrid[row:row+rowDim][col:col+colDim] = -1
        # Place instance at bottom left corner of matrix
        self.placementGrid[row][col] = instance

    def printPlacement(self):
        """
        Prints visual CSV file of island placement
        """
        text = ""
        numRows = np.shape(self.placementGrid)[0]
        numCols = np.shape(self.placementGrid)[1]

        i = numRows-1
        for row in range(numRows):
            for col in range(numCols):
                if isinstance(self.placementGrid[i-row,col],StandardCell):
                    text+= self.placementGrid[i-row,col].name
                else:
                    text+= str(self.placementGrid[i-row,col])
                text += ","
            text += "\n"
        
        return text

        

class Net:
    """
    Defines connections between pins
    Contains
    - List of pins connected to this net
    - Number (for naming)
    - Index (for  nets in a matrix)
    """
    def __init__(self,circuit,pins=None):
        self.pins = []
        self.number = -1
        self.index = -1
        if pins != None:
            self.addPins(pins)
   
        self.circuit = circuit
        self.circuit.addNet(self)

    def __call__(self):
        return self
    
    def __len__(self):
        return len(self.pins)
    
    def containsVector(self):
        for p in self.pins:
            if p.isVector:
                return True
            
        return False
    
    def getPins(self):
        return self.pins
    
    def isEmpty(self):
        """
        Checks if net has more than one pin
        """
        if len(self.pins) > 1:
            return True
        else:
            return False

    def connect(self,net):
        """
        Connects two nets together
        Uses merge function in Circuit class
        """
        newNet = self.circuit.mergeNets([self,net])
        return newNet

    def addPins(self,pins):
        if isinstance(pins,list):
            self.pins += pins
        else:
            self.pins.append(pins)

    def removePin(self,pin):
        self.pins.remove(pin)

    def print(self):
        """
        Returns Verilog text string for net
        """
        text = "net" + str(self.number)
        
        if self.index != -1:
            text += "[" + str(self.index) + "]"

        return text
       

class Pin:
    """
    Defines single connection between a port and net
    Contains
    - Net (single)
    - Port (single)
    - Cell (single)
    """
    def __init__(self,circuit,port=None,cell=None,net = None):
        self.net = net
        self.port = port
        self.cell = cell
        self.circuit = circuit

        if self.net == None:
            self.net = Net(self.circuit,pins=self)
        
    def isConnected(self):
        """
        Checks if connected net is empty
        """
        if self.net.isEmpty() == False:
            return False
        else:
            return True 
        
    def isVector(self):
        """
        Checks if pin is part of a vectorized port
        """
        if self.port.getVectorSize() > 1:
            return True
        else:
            return False
        
    def getVectorSize(self):
        """
        Returns size of pin vector
        """
        return self.port.getVectorSize()

    def getNet(self):
        return self.net
    
    def connect(self,connection):
        """
        Connets 
        - Pin to net
        or 
        - Pin to pin
        """
        if isinstance(connection,Net):
            self.net = self.net.connect(connection)
        elif isinstance(connection,Pin):
            self.net = self.net.connect(connection.getNet())

    def disconnect(self):
        """
        Removes pin from net
        """
        self.net.removePin(self)
        self.net = Net(self.circuit,pins=self)

    def move(self,net):
        """
        Points pin to new net
        """
        #self.net.removePin(self)
        net.addPins(self)
        self.net = net

    def print(self):
        """
        Returns Verilog text string for net
        """
        return self.net.print()
       
class Port:
    """
    Logical grouping of pins
    Contains
    - Pins (list)
    - Cell (single)
    """
    def __init__(self,circuit,cell,name,location,pinNumber):
        self.circuit = circuit
        self.name = name
        self.location = location
        self.cell = cell

        #Generate pins equal to pinNumber
        self.pins = []
        for i in range(pinNumber):
            self.pins.append(Pin(circuit,self,cell))

        #If port belongs to a cell
        if cell != None:
            # Add pins to cell's list
            self.cell.addPins(self.pins)
            # Add self to cell's list
            self.cell.addPort(self)

    def getPins(self):
        return self.pins
    
    def assignPin(self,num,connection):
        self.pins[num].connect(connection)

    def shortPins(self,net):
        pinnets = [net]
        for p in self.pins:
            pinnets.append(p.net)

        self.circuit.mergeNets(pinnets)


    def connectPort(self,connection):
        """
        Connects port nets
        - Port  <-> Port 
        - List of nets <-> Port
        - List of pins <-> Port
        - Single net <-> Port net (short)
        """

        # Port <-> Port
        if isinstance(connection,Port):
            # Make sure sizes match
            if len(connection) == len(self.pins):
                for i in range(0,len(connection)):
                    self.assignPin(i,connection[i])
            else:
                raise Exception("Mismatched net sizes assigned together")
        # Short Pin <-> Port
        elif isinstance(connection,Pin):
            self.shortPins(connection.net)
        # List
        elif isinstance(connection,list):
            # List of nets <-> Port or List of pins <-> Port
            if isinstance(connection[0],Net) or isinstance(connection[0],Pin):
                # Make sure sizes match
                if len(connection) == len(self.pins):
                    for i in range(0,len(connection)):
                        self.assignPin(i,connection[i])
                else:
                    raise Exception("Mismatched net sizes assigned together")
            else:
                raise Exception("Invalid Assignment")
        else:
                raise Exception("Invalid Assignment")


    def isEmpty(self):
        for p in self.pins:
            if p.isConnected():
                return False
        return True
    
    def __len__(self):
        return len(self.pins)

    def __getitem__(self,key):
        return self.pins[key]
    
    def __setitem__(self,key,net):
        self.pins[key] = net
    
    def __call__(self):
        return self.pins
    
    def numPins(self):
        """
        Returns number of physical pins per instance
        Keeps matrix routing in mind

        len(pins) = pinNum * dimension
        """
        pinNum = 0
        if self.location == "E" or self.location == "W":
            pinNum = len(self.pins)/self.cell.dim[0]
        elif self.location == "N" or self.location == "S":
            pinNum = len(self.pins)/self.cell.dim[1]
        else:
            pinNum = len(self.pins)

        return pinNum
    
    def getVectorSize(self):
        """
        Returns size of pin vector for matrix routing

        dimension = len(pins) / pinNum
        """
        return len(self.pins)/self.numPins()

    def print(self):
        """
        Returns Verilog text for each pin in port
        Collapses vectors into original pin dimensions
        """
       
        line = ""
        for i in range(int(self.numPins())):
            pin = self.pins[i]
            if pin.isConnected():

                if i != 0:
                    line+= ","

                line += "." + self.name + "_" + str(i) + "_("
                
                if pin.isVector() == True:
                    pinVector = self.pins[i::int(self.numPins())]
                    idxStart = pinVector[0].net.index
                    idxEnd = pinVector[-1].net.index
                    idxJump = pinVector[1].net.index - idxStart

                    pinVectorText = "[" + str(idxStart) + ":" + str(idxEnd) + ":" + str(idxJump) + "]"
                    line += "net" + str(pin.net.number) + pinVectorText

                elif pin.isVector() == False:
                    line += pin.print()

                line += ")"
            

        return line
        

class StandardCell:
    """
    Defines single/array instance of a standard cell
    Contains
    - Ports (list)
    - Pins (list)
    - Island (single)
    """
    def __init__(self,circuit,island):
        # Add cell to circuit
        circuit.addInstance(self)

        # Add cell to Island
        self.island = island

        # Define cell information
    
        # Attach nets if given
        self.circuit = circuit
        self.pins = []
        self.ports = []

        # Dimensions
        self.dim = (1,1)

    def addPins(self,pins):
        self.pins += pins

    def addPort(self,port):
        self.ports.append(port)
        
    def __setitem__(self,key,net):
        for i in self:
            if i.name == key:
                i.net = net
        
    def __getitem__(self,key):
        for i in self:
            if i.name == key:
                return i.net

    def __call__(self):
        return self.outputs
    
    def assignPort(self,port,connection):
        """
        Assigns port to nets
        - Port nets <-> Port nets
        - List of nets <-> Port
        - Single net <-> Port net (short)
        """
        if connection != None:
            port.connectPort(connection)



    
    def print(self,instanceNum,islandNum,row,col,processPrefix):
        """
        Returns Verilog text for instance
        """

        # Prefixes and placement
        #text = processPrefix + "_" + self.name + " I__" + str(instanceNum) + " ("

        #TODO Remove process prefix from auto-generated class library
        text = self.name + " I__" + str(instanceNum) + " ("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".row(" + str(row) + "), "
        text += ".col(" + str(col) + ")"

        # Matrix definition
        if self.dim[0] > 1 or self.dim[1] > 1:
            text += ", .matrix_row(" + str(self.dim[0]) + "), "
            text += ".matrix_col(" + str(self.dim[1]) + ")"

        # Pins
        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += ", "
                text += port.print()
                i+=1
        text += ");"
        return text
    
