# Classes and functions for compilation of ASIC python to a Verilog Netlist

import os
import shutil
import numpy as np
from ashes_fg.asic import compile
#from ashes_fg.class_lib_mux import *


# Functions
# ---------------------------------------------------------------------------------------------------------------------------
def compile_asic(circuit,process="Process",fileName = "compiled",path = "./example_verilog", p_and_r = True, location_islands=None, design_limits = [1e6, 6.1e5],drainSpaceIdx=None,drainSpace=10,gateSpaceIdx=None,gateSpace=10):
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

    # All units in nanometers
    tech_process = 'vis350'
    cell_pitch = 22000
    dbu = 1000
    track_spacing = 1400
    # placement offset to make space for pin routing
    x_offset, y_offset = 400*track_spacing, 2000*track_spacing 

    design_area = (0, 0, design_limits[0], design_limits[1], x_offset, y_offset)

    # Run P&R if desired
    if p_and_r == True:
        compile(None, 
        project_name=test_project, 
        tech_process=tech_process, 
        dbu=dbu, 
        track_spacing=track_spacing,
        cell_pitch=cell_pitch,
        x_offset=x_offset, y_offset=y_offset,
        design_area=design_area,
        location_islands=location_islands,
        drainmux_space_isle_idx=drainSpaceIdx,
        drainmux_space = drainSpace,
        gatemux_space_isle_idx=gateSpaceIdx,
        gatemux_space = gateSpace)




def printPlacement(island,fileName = "island_placement",path = "./"):
    """
    Debug aid for placement
    Prints island placement array to a csv file
    """
    fileName += ".csv"
    filePathandName = os.path.join(path,fileName)
    f = open(filePathandName, "w")
    f.write(island.printPlacement())

def Bus(circuit,size,busElements = None):
    """
    Helper function to easily create vectors of nets
    """
    if busElements == None:
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

        # Circuit frame (defines new outer pins)
        self.frame = None

        # Nets (hyper edges)
        self.Nets = []

        # Islands (grouping of instances for placement)
        self.Islands = []
        self.DefaultIsle = Island(self)

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
                        # Ignore decoder cells (because they print flat, so their vector doesn't count)
                        if pin.cell.isDecoder() == False:
                            if pin.getVectorSize() > largestDim:
                                largestDim = pin.getVectorSize()
                                largestPin = pin
                            
                    # If the net only contain a decoder, it will mistakenly trigger containsVector() but 
                    # will never pick up a largestPin because of the decoder ignore check
                    if largestPin != None:
                        # Name all nets attached to that pin
                        port = largestPin.port
                        idxNum = self.Nets.index(net)
                        idx = 0
                        physicalPinIdx = largestPin.getPhysicalPin()

            
                        for i in range(port.getVectorSize()):
                            p = port.pins[physicalPinIdx + i*port.numPins()]
                            p.net.number = idxNum
                            p.net.index = idx
                            idx += 1
                    else:
                       net.number = self.Nets.index(net) 

                elif net.containsVector() == False:
                    net.number = self.Nets.index(net)

                    # Check for non-decoder matrix
                    for p in net.pins:
                        if p.cell != None:
                            if p.cell.isMatrix() and isinstance(p.cell,MUX) == False:
                                net.index = 0

        for net in self.Nets:
            if net.number == -1:
                wrongPort = net.pins[0].port.name
                raise Exception("Error: Not all nets named (" + wrongPort + ")")

 
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

        # Print frame, if applicable
        if self.frame != None:
            text += "\n\n"
            text += "\t/* Frame */ \n"
            text += self.frame.print()

        text += "\n endmodule"
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
            if instance.isDecoder() == False:
                # Get row and column number
                instanceLocation = self.getLocation(instance)
                try:
                    placedRow = instanceLocation[0][0]
                except:
                    raise Exception("Error: Instance " + instance.name + " not placed")
                placedCol = instanceLocation[1][0]
                text += "\t"
                text += instance.print(i,islandNum,placedRow,placedCol)
                text += ("\n")
            # Decoder doesn't have placement information
            elif instance.isDecoder() == True:
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

        # Check for placement errors
        for i in range(rowDim):
            for j in range(colDim):
                if self.placementGrid[row+i,col+j] != 0:
                    raise Exception("Placement collision when attempting to place  " + instance.name)   

        # Fill in for matrix elements
        self.placementGrid[row:row+rowDim,col:col+colDim] = instance.name
        # Place instance at bottom left corner of matrix
        self.placementGrid[row][col] = instance

    def printPlacement(self):
        """
        Prints visual CSV file of island placement
        """
        text = ""
        numRows = np.shape(self.placementGrid)[0]
        numCols = np.shape(self.placementGrid)[1]

        for row in range(numRows):
            for col in range(numCols):
                if isinstance(self.placementGrid[row,col],StandardCell):
                    text+= self.placementGrid[row,col].name
                else:
                    text+= str(self.placementGrid[row,col])
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
            if p.isVector():
                return True
            
        return False
    
    def getPins(self):
        return self.pins
    
    def isEmpty(self):
        """
        Checks if net has more than one pin
        """
        if len(self.pins) > 1:
            return False
        else:
            return True

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
        if self.net.isEmpty() == True:
            return False
        elif self.net.isEmpty() == False:
            return True 
        
    def isVectorConnected(self):
        """
        Checks if any pin in pin vector is connected
        """
        if self.isVector() == False:
            return self.isConnected()
        
        idx = self.getPhysicalPin()

        pinArr = self.port.pins[idx:len(self.port)+1:self.port.numPins()]

        for p in pinArr:
            if p.isConnected() == True:
                return True
                
        return False
            
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
    
    def getPhysicalPin(self):
        """
        Returns physical pin index for given port
        Needed because of Vectors
        """
        idx = self.port.pins.index(self)
        numPrev = idx
        num = idx
        numPins = self.port.numPins()

        while num > -1:
            numPrev = num
            num -= numPins
        
        return numPrev

    def isShorted(self):
        """
        Checks if the pin is shorted
        """
        if self.isVector() == False:
            return True
        
        idx = self.getPhysicalPin()

        pinArr = self.port.pins[idx:len(self.port)+1:self.port.numPins()]

        if len(set(pinArr)) == 1:
            return True
        else:
            return False

    def getNet(self):
        return self.net
    
    def __iadd__(self,operand):
        self.connect(operand)
        return self
    
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
        elif isinstance(connection,Port):
            connection.connectPort(self)

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
    def __init__(self,circuit,cell,name,location,pinNumber,static = False):
        self.circuit = circuit
        self.name = name
        self.location = location
        self.cell = cell
        self.isStatic = static

        # 0 pinNumber not allowed, means MUX cell trying to instantiate with dimension of 0
        if pinNumber == 0:
            pinNumber += 1

        #Generate pins equal to pinNumber
        self.pins = []
        for i in range(int(pinNumber)):
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

    def isShorted(self):
        if len(set(self.pins)) == 1:
            return True
        else:
            return False

    def __iadd__(self,operand):
        self.connectPort(operand)
        return self # Avoid turning self into a "none" type

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
    
    def assignMetal(self,metal):
        self.metal = metal
    
    def __len__(self):
        return len(self.pins)

    def __getitem__(self,key):
        return self.pins[key]
    
    # Should never call directly
    # Uses equality operator
    def __setitem__(self,key,connection):
        #self.pins[key] += connection
        return None
    
    def __call__(self):
        return self.pins
    
    def numPins(self):
        """
        Returns number of physical pins per instance
        Keeps matrix routing in mind

        len(pins) = pinNum * dimension
        """
        
        pinNum = 0
        if self.isStatic == True:
            return len(self.pins)
        elif (self.location == "E" or self.location == "W") and self.cell.dim[0] != 0:
            pinNum = len(self.pins)/self.cell.dim[0]
        elif (self.location == "N" or self.location == "S") and self.cell.dim[1] != 0:
            pinNum = len(self.pins)/self.cell.dim[1]
        else:
            pinNum = len(self.pins)

        return int(pinNum)
    
    def getVectorSize(self):
        """
        Returns size of pin vector for matrix routing

        dimension = len(pins) / pinNum
        """
        return int(len(self.pins)/self.numPins())
    
    def printFlat(self,type = "decode",extraIdx = -1):
        """
        Returns Verilog text for a decoder port
        Decoders are a special case
        - Vectors flattened
        - Indices in pin name
        """

        line = ""
        # For each instance 
        p = 0
        for i in range(self.getVectorSize()):
            # For each pin in instance
            for j in range(self.numPins()):
                pin = self.pins[p]
                if pin.isConnected(): 
                    line += ", ." + type
                    if extraIdx > 0:
                        line += "_n" + str(extraIdx)

                    line += "_n" + str(i) + "_" + self.name

                    # Add pin number for ports with size > 1
                    if self.numPins() > 1:
                        line += "_" + str(j) + "_"

                    line += "("
                    line += pin.print()
                    line += ")"
                p+=1

        return line 

    def print(self):
        """
        Returns Verilog text for each pin in port
        Collapses vectors into original pin dimensions
        """
       
        line = ""
        for i in range(int(self.numPins())):
            pin = self.pins[i]

            if pin.isVectorConnected():
                line += ", ." + self.name
                # Add vector notation for a vectorized port
                if self.numPins() > 1:
                    line +=  "_" + str(i) + "_"

                if self.cell.isMatrix() ==  True or self.cell.isAbutted() == True:
                    if self.cell.isAbutted():
                        line += "row_0"
                    elif self.location == "E":
                        line += "col_" + str(self.cell.dim[1]-1)
                    elif self.location == "W":
                        line += "col_0"
                    elif self.location == "N":
                        line += "row_0"
                    elif self.location == "S":
                        line += "row_" + str(self.cell.dim[0]-1)

                line += "("
                
                if pin.cell.isMatrix() == True:
                    if pin.isShorted() == True:
                        #line += pin.print()
                        idxStart = pin.net.index
                        pinVectorText = "[" + str(idxStart) + ":" + str(idxStart + 1) + "]"
                        line += "net" + str(pin.net.number) + pinVectorText
                    else:
                        idxStart = 0
                        idxEnd = self.getVectorSize()
                        pinVectorText = "[" + str(idxStart) + ":" + str(idxEnd) + "]"
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

    def place(self,loc):
        self.circuit.placeInstance(self,loc)

    def markCABDevice(self):
        self.cabDevice = True

    def markAbut(self):
        self.Abut = True


    def isAbutted(self):
        try:
            if self.Abut == True:
                return True
        except:
            return False
        
    def isMatrix(self):
        if self.dim[0] > 1:
            return True
        elif self.dim[1] > 1:
            return True
        else:
            return False

    def isDecoder(self):
        """
        Identifies special decoder cells
        """
        if isinstance(self,MUX):
            return True
        else:
            return False

    def isCABDevice(self):
        try:
            if self.cabDevice == True:
                return True
        except:
            return False
    
    def addPins(self,pins):
        self.pins += pins

    def addPort(self,port):
        self.ports.append(port)
        
    def __setitem__(self,key,connection):
        for i in self.ports:
            if i.name == key:
                i += connection
        
    def __getitem__(self,key):
        for i in self.ports:
            if i.name == key:
                return i

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

    def print(self,instanceNum,islandNum,row,col,instancePrefix = "I_"):
        """
        Returns Verilog text for instance
        """

        # Prefixes and placement
        #text = processPrefix + "_" + self.name + " I__" + str(instanceNum) + " ("

        if self.isCABDevice() == True:
            instancePrefix = "cab_device"

        #TODO Remove process prefix from auto-generated class library
        text = self.name + " " + instancePrefix +"_" + str(instanceNum) + " ("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".row(" + str(row) + "), "
        text += ".col(" + str(col) + ")"

        # Matrix definition
        if self.dim[0] > 1 or self.dim[1] > 1:
            text += ", .matrix_row(" + str(self.dim[0]) + "), "
            text += ".matrix_col(" + str(self.dim[1]) + ")"

        if self.isAbutted() == True:
            text += ", .matrix_row(" + str(self.dim[0]) + "), "
            text += ".matrix_col(" + str(self.dim[1]) + ")"

        # Pins
        i = 0
        for port in self.ports:
            if port.isEmpty() == False:
                text += port.print()
                i+=1
        text += ");"
        return text
    
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
        
    def getDirection(self):
        if self.dim[0] < 1:
            return "horizontal"
        else:
            return "vertical"

    def print(self,instanceNum,islandNum,row,col,processPrefix):

        if self.type == "decode":
            text = self.name + " " + "decoder" + "("
        else:
            text = self.name + " " + self.type + "("
        text += ".island_num(" + str(islandNum) + "), "
        text += ".direction(" + self.getDirection() + "), "

        if self.type == "decode":
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
                if self.type == "switch_ind":
                    text += port.print()
                else:
                    # Temporary check for south pin on gate decoder to put in double notation
                    if self.type == "decode" and self.getDirection() == "horizontal" and port.location == "S":
                        if self.bits % 2 == 0:
                            lastRow = self.bits-1
                        else:
                            lastRow = self.bits
                        text += port.printFlat(type=self.type,extraIdx=lastRow-1)
                    else:
                        text += port.printFlat(type = self.type)
                i+=1
        text += ");"
        return text
        
class PortDecoderBit(Port):
    """
    Logical grouping of pins
    Contains
    - Pins (list)
    - Cell (single)
    
    *Special case of port for decoder bits - handles unique printing scenario
    """
    def __init__(self,circuit,cell,name,location,pinNumber,static = False):
        self.circuit = circuit
        self.name = name
        self.location = location
        self.cell = cell
        self.isStatic = static

        # 0 pinNumber not allowed, means MUX cell trying to instantiate with dimension of 0
        if pinNumber == 0:
            pinNumber += 1

        #Generate pins equal to pinNumber
        self.pins = []
        for i in range(int(pinNumber)):
            self.pins.append(Pin(circuit,self,cell))

        #If port belongs to a cell
        if cell != None:
            # Add pins to cell's list
            self.cell.addPins(self.pins)
            # Add self to cell's list
            self.cell.addPort(self)

    def printFlat(self,type = "decode",extraIdx = -1):
        """
        Returns Verilog text for a decoder port
        Decoders are a special case
        - Vectors flattened
        - Indices in pin name

        *Handles special case of decoder bits
        """
        line = ""
        idx = 0
        # For each bit in the decoder
        # Assuming b[0] = LSB
        for b in range(self.cell.bits):
            bitNum = self.cell.bits-b # Starting from MSB
            pin = self.pins[bitNum-1]
            if pin.isConnected():
                line += ", ." + type

                if self.cell.getDirection() == "horizontal":
                    line += "_n" + str(idx) + "_n0_" + self.name
                elif self.cell.getDirection() == "vertical":
                    line += "_n" + str(idx) + "_" + self.name

                line += "_" + str((bitNum+1)%2) + "_"

                line += "("
                line += pin.print()
                line += ")"

            # Check if we're moving onto next row/column
            if bitNum%2 == 1:
                idx += 2

        return line 
        
class FakeStandardCell(StandardCell):
    def __init__(self,circuit,island,num=1):
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


    def print(self,instanceNum,islandNum,row,col):

        return ''
    
