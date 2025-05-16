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

    EPOTs = lib_dc.TSMC350nm_EPOT(Top,QDACIsland,dim=[numStages,1])
    EPOTs.place([0,0])

    InvertingAmp = lib_dc.TSMC350nm_Amplifier9T_FGBias(Top,QDACIsland)
    InvertingAmp.place([numStages+1,0])

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

    drainLineNum = numStages*2+1
    drainBits = int(np.ceil(np.log2(drainLineNum)))

    DrainDecoder = lib_mux.STD_DrainDecoder(Top,QDACIsland,bits=drainBits)
    DrainSelect = lib_mux.RunDrainSwitch(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))
    DrainSwitch = lib_cab.DrainCutoff(Top,QDACIsland,num=int(np.ceil(drainLineNum/4)))

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

    location_islands = ((XEPOT,YEPOT),(XTGate0,YIslands2),(XTGate1,YIslands2),(XEPOTCap,YIslands2),(XAmpRST,YEPOT),(XCap,YEPOT))

    return location_islands


Top = ac.Circuit()

location_islands = QDAC(Top,5)

design_limits = [5e5, 5e5]


ac.compile_asic(Top,process="TSMC350nm",fileName="QDAC",p_and_r = True,design_limits = design_limits, location_islands = location_islands,drainSpaceIdx=0,drainSpace = 15,gateSpaceIdx=0,gateSpace=10)




