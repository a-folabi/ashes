import ashes_fg as af

import ashes_fg.asic.asic_compile as ac

import ashes_fg.class_lib_new as lib_new
import ashes_fg.class_lib_mux as lib_mux
import ashes_fg.class_lib_cab as lib_cab
import ashes_fg.class_lib_dataconverter as lib_dc
import ashes_fg.asic.asic_systems as algs

import numpy as np


def QDAC(circuit,numStages=1,QDACIsland=None,islandLoc = [0,0]):
    Top = circuit

    QDACIsland = ac.Island(Top)
    EPOTs = lib_dc.TSMC350nm_EPOT(Top,QDACIsland,dim=[numStages+1,1])
    EPOTs.place([0,0])

    InvertingAmp = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,QDACIsland)
    InvertingAmp.place([numStages+2,0])

    TgateIsland0 = ac.Island(Top)
    SEL_Code = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland0,dim=[numStages,1])
    SEL_Code.place([0,0])

    TgateIsland1 = ac.Island(Top)
    SEL_RST = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland1,dim=[numStages,1])
    SEL_RST.place([0,0])

    EPOTCapIsland = ac.Island(Top)
    EPOTCap = lib_dc.TSMC350nm_Capacitor_80ff(Top,EPOTCapIsland,dim=[numStages,1])
    EPOTCap.place([0,0])

    TgateIsland2 = ac.Island(Top)
    Amp_RST = lib_dc.TSMC350nm_TGate_DT(Top,TgateIsland2)
    Amp_RST.place([0,0])

    CapFBIsland = ac.Island(Top)
    CapFB = lib_dc.TSMC350nm_Capacitor_80ff(Top,CapFBIsland)
    CapFB.place([0,0])

    # FG Programming
    # -------------------------------------------------------------------------------
    GateDecoder = lib_mux.STD_IndirectGateDecoder(Top,QDACIsland,2)
    GateSwitches0 = lib_mux.STD_IndirectGateSwitch(Top,QDACIsland,1)
    GateSwitches = lib_mux.STD_IndirectGateSwitch(Top,QDACIsland,1,col=0)

    drainLineNum = (numStages+1)*2+1
    drainBits = int(np.ceil(np.log2(drainLineNum)))

    DrainDecoder = lib_mux.STD_DrainDecoder(Top,QDACIsland,bits=drainBits)
    DrainSelect = lib_mux.RunDrainSwitch(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))
    DrainSwitch = lib_cab.DrainCutoff(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))

    for i in range(numStages+1):
        DrainSwitch.PR[2*i] += EPOTs.VD_P[2*i]
        DrainSwitch.PR[2*i+1] += EPOTs.VD_P[2*i+1]

    DrainSwitch.PR[2*(numStages+1)] += InvertingAmp.VD_P
    DrainSwitch.In[2*(numStages+1)] += InvertingAmp.VD_R 

    # Pins
    # -------------------------------------------------------------------------------
    outerPins = lib_mux.frame(Top)

    PROG = outerPins.createPort("N","Prog")
    RUN = outerPins.createPort("N","Run")
    VGRUN = outerPins.createPort("N","VGRUN")
    VGPROG = outerPins.createPort("N","VGPROG")
    VTUN = outerPins.createPort("N","VTUN")
    AVDD = outerPins.createPort("N","AVDD")
    GND_N = outerPins.createPort("N","gnd")
    GND_S = outerPins.createPort("S","gnd")
    VINJ_N = outerPins.createPort("N","vinj")
    VINJ_S = outerPins.createPort("S","vinj")

    DrainBits = outerPins.createPort("W","DrainB",dimension=drainBits)
    DrainEnable = outerPins.createPort("W","DrainEnable")
    GateBits = outerPins.createPort("W","GateB",dimension=2)
    GateEnable = outerPins.createPort("W","GateEnable")
    
    VOUT = outerPins.createPort("S","Vout")
    RST = outerPins.createPort("N","RST")
    Code = outerPins.createPort("N","Code",dimension=numStages)

    # Pin Connections
    # -------------------------------------------------------------------------------
    EPOTs.VDD += AVDD
    EPOTs.VINJ += VINJ_N
    EPOTs.VINJ_b += VINJ_S
    EPOTs.GND += GND_N
    EPOTs.GND_b += GND_S
    EPOTs.Prog += PROG

    Vref = ac.Wire(Top)
    EPOTs.Vout[numStages-1] += Vref

    EPOTs.Vout[0:numStages-2] += SEL_Code.A

    SEL_Code.VDD += VINJ_N
    SEL_Code.VDD_b += VINJ_S
    SEL_Code.GND += GND_N
    SEL_Code.GND_b += GND_S
    SEL_Code.C += SEL_RST.B
    SEL_Code.SELA += Code
    SEL_Code.A += EPOTs.Vout[0:numStages]
    SEL_Code.B += Vref

    SEL_RST.VDD_b += VINJ_S
    SEL_RST.GND += GND_N
    SEL_RST.C += EPOTCap.Top
    SEL_RST.SELA += RST[0]
    SEL_RST.A += Vref

    EPOTCap.Bot += InvertingAmp.VIN_PLUS[0]

    Amp_RST.VDD_b += VINJ_S
    Amp_RST.GND_b += GND_S
    Amp_RST.SELA += RST[0]
    Amp_RST.C += VOUT[0]
    Amp_RST.A += Vref

    InvertingAmp.VINJ += EPOTs.VINJ_b
    InvertingAmp.VPWR += EPOTs.VDD_b
    InvertingAmp.PROG += EPOTs.Prog_b
    InvertingAmp.Vg += EPOTs.Vg_b[0]
    InvertingAmp.Vsel += EPOTs.Vsel_b[0]
    InvertingAmp.VIN_MINUS += Amp_RST.A
    InvertingAmp.VIN_MINUS += CapFB.Top
    InvertingAmp.Vout += CapFB.Bot
    InvertingAmp.Vout += VOUT

    GateSwitches.VINJ_T += VINJ_N[0]
    GateSwitches.VINJ += EPOTs.VINJ
    GateSwitches.PROG += PROG
    GateSwitches.GND_T += GND_N[0]
    GateSwitches.GND += GND_S[0]
    GateSwitches.CTRL_B += EPOTs.Vg

    DrainSwitch.RUN += RUN

    DrainDecoder.VINJ += VINJ_S
    DrainDecoder.GND += GND_S
    DrainDecoder.IN += DrainBits
    DrainDecoder.ENABLE += DrainEnable

    GateDecoder.VINJV += VINJ_N
    GateDecoder.GNDV += GND_N
    GateDecoder.ENABLE += GateEnable
    GateDecoder.IN += GateBits

    # Island Placement
    # -------------------------------------------------------------------------------

    EPOTWidth = 85000
    TGateWidth = 10000
    XSpace = 1000
    Pitch = 22000
    DecoderWidth = int(43000 + ((drainBits/2)*25000))

    XEPOT = islandLoc[0]
    XTGate0 = DecoderWidth+15000+XEPOT+EPOTWidth+5*XSpace
    XTGate1 = XTGate0 + TGateWidth + 2*XSpace
    XEPOTCap = XTGate1 + TGateWidth + 2*XSpace
    XAmpRST = DecoderWidth+15000+XEPOT+75000
    XCap = XAmpRST+2*XSpace+TGateWidth

    YEPOT = islandLoc[1]
    YIslands2 = YEPOT + 2*Pitch
    Ybottom = YEPOT

    location_islands = ((XEPOT,YEPOT),(XTGate0,YIslands2),(XTGate1,YIslands2),(XEPOTCap,YIslands2),(XAmpRST,Ybottom),(XCap,Ybottom))

    return location_islands


Top = ac.Circuit()

location_islands = QDAC(Top,5,islandLoc=[50000,25000])

design_limits = [5e5, 5e5]


ac.compile_asic(Top,process="TSMC350nm",fileName="QDAC",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 15,gateSpaceIdx=0,gateSpace=10)




