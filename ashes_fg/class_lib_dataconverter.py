from ashes_fg.asic.asic_compile import *

class TSMC350nm_EPOT(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VDD=None,VDD_b=None,VINJ=None,VINJ_b=None,GND=None,GND_b=None,VTUN=None,VTUN_b=None,Prog=None,Prog_b=None,Vg=None,Vg_b=None,Vsel=None,Vsel_b=None,VD_P=None,VINPLUS=None,Vout=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'EPOT'
        self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
        self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
        self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
        self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

        self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
        self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])

        self.Prog = Port(circuit,self,'Prog','N',1*self.dim[1])
        self.Prog_b = Port(circuit,self,'Prog_b','S',1*self.dim[1])

        self.Vg = Port(circuit,self,'Vg','N',2*self.dim[1])
        self.Vg_b = Port(circuit,self,'Vg_b','S',2*self.dim[1])

        self.Vsel = Port(circuit,self,'Vsel','N',2*self.dim[1])
        self.Vsel_b = Port(circuit,self,'Vsel_b','S',2*self.dim[1])

        self.VD_P = Port(circuit,self,'VD_P','W',2*self.dim[0])

        self.VINPLUS = Port(circuit,self,'Vin+','W',1*self.dim[0])
        self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])

		
        # Initialize ports with given values
        portsInit = [VDD,VDD_b,VINJ,VINJ_b,GND,GND_b,VTUN,VTUN_b,Prog,Prog_b,Vg,Vg_b,Vsel,Vsel_b,VD_P,VINPLUS,Vout]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TSMC350nm_Amplifier9T_FGBias(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VPWR=None,VPWR_b=None,VINJ=None,VINJ_b=None,GND=None,GND_b=None,VTUN=None,VTUN_b=None,Vg=None,Vg_b=None,VD_P=None,VD_R=None,Vsel=None,Vsel_b=None,PROG=None,PROG_b=None,VIN_PLUS=None,VIN_MINUS=None,Vout=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'TSMC350nm_Amplifier9T_FGBias'
        self.VPWR = Port(circuit,self,'VDD','N',1*self.dim[1])
        self.VPWR_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
        self.VINJ = Port(circuit,self,'VINJ','N',1*self.dim[1])
        self.VINJ_b = Port(circuit,self,'VINJ_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

        self.VTUN = Port(circuit,self,'VTUN','N',1*self.dim[1])
        self.VTUN_b = Port(circuit,self,'VTUN_b','S',1*self.dim[1])

        self.Vg = Port(circuit,self,'Vg','N',1*self.dim[1])
        self.Vg_b = Port(circuit,self,'Vg_b','S',1*self.dim[1])

        self.VD_P = Port(circuit,self,'VD_P','W',1*self.dim[0])
        self.VD_R = Port(circuit,self,'VD_R','W',1*self.dim[0])

        self.Vsel = Port(circuit,self,'Vsel','N',1*self.dim[1])
        self.Vsel_b = Port(circuit,self,'Vsel_b','S',1*self.dim[1])

        self.PROG = Port(circuit,self,'PROG','N',1*self.dim[1])
        self.PROG_b = Port(circuit,self,'PROG_b','S',1*self.dim[1])

        self.VIN_PLUS = Port(circuit,self,'VIN_PLUS','W',1*self.dim[0])
        self.VIN_MINUS = Port(circuit,self,'VIN_MINUS','W',1*self.dim[0])

        self.Vout = Port(circuit,self,'Vout','E',1*self.dim[0])


        # Initialize ports with given values
        portsInit = [VPWR,VPWR_b,VINJ,VINJ_b,GND,GND_b,VTUN,VTUN_b,Vg,Vg_b,VD_P,VD_R,Vsel,Vsel_b,PROG,PROG_b,VIN_PLUS,VIN_MINUS,Vout]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TSMC350nm_Capacitor_80ff(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),Top=None,Bot=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'Capacitor_80ff'
        self.Top = Port(circuit,self,'Top','W',1*self.dim[0])
        self.Bot = Port(circuit,self,'Bot','E',1*self.dim[0])
      

        # Initialize ports with given values
        portsInit = [Top,Bot]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)

class TSMC350nm_TGate_DT(StandardCell):
    def __init__(self,circuit,island=None,dim=(1,1),VDD=None,VDD_b=None,GND=None,GND_b=None,SELA=None,C=None,A=None,B=None):
        # Define variables
        self.circuit = circuit
        self.pins = []
        self.ports = []
        self.island = island
        self.dim = dim


        # Define cell information
        self.name = 'TGate_DT'
        self.VDD = Port(circuit,self,'VDD','N',1*self.dim[1])
        self.VDD_b = Port(circuit,self,'VDD_b','S',1*self.dim[1])
        self.GND = Port(circuit,self,'GND','N',1*self.dim[1])
        self.GND_b = Port(circuit,self,'GND_b','S',1*self.dim[1])

        self.SELA = Port(circuit,self,'SELA','W',1*self.dim[0])
        self.C = Port(circuit,self,'C','W',1*self.dim[0])

        self.A = Port(circuit,self,'A','E',1*self.dim[0])
        self.B = Port(circuit,self,'B','E',1*self.dim[0])

        # Initialize ports with given values
        portsInit = [VDD,VDD_b,GND,GND_b,SELA,C,A,B]
        i=0
        for p in self.ports:
            self.assignPort(p,portsInit[i])
            i+=1

        # Add cell to circuit
        circuit.addInstance(self,self.island)