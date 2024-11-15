module TOP(cells); 
    TSMC350nm_4x2_Direct I__0 (.island_num(0), .row(1), .col(1), .Vg_0_(c_net2), .Vd_3_(c_net3));
    TSMC350nm_4x2_Indirect I__1 (.island_num(1), .row(1), .col(1), .Vg_0_(c_net2), .Vd_P_2_(c_net4), .Vd_P_3_(c_net3));
    TSMC350nm_VerticalScanner I__2 (.island_num(2), .row(1), .col(1));
    TSMC350nm_TA2Cell_NoFG I__3 (.island_num(3), .row(1), .col(1), .DRAIN2(c_net1), .DRAIN1(c_net3));
    TSMC350nm_TA2Cell_Weak I__4 (.island_num(4), .row(1), .col(1), .DRAIN1(c_net4), .DRAIN2(c_net1));
    TSMC350nm_C4 I__5 (.island_num(5), .row(1), .col(1), .DRAIN1(a_net1), .OUTPUT(c_net5));
    TSMC350nm_TA2Cell_Strong I__6 (.island_num(6), .row(1), .col(1));
    TSMC350nm_voltage_DAC_6bit I__7 (.island_num(7), .row(1), .col(1), .BIT_2_(c_net5));
    TSMC350nm_VMMWTA I__8 (.island_num(8), .row(1), .col(1), .Vg_1_(a_net2));
    frame_10p_10p FRAME (.p_3_(a_net1), .p_27_(a_net2));
    
endmodule

module other2(port1); 
    TSMC350nm_4x2_Direct I__0 (.island_num(0), .row(1), .col(1), .Vg_0_(c_net2), .Vs_0_(c_net3));
    TSMC350nm_4x2_Indirect I__1 (.island_num(1), .row(1), .col(1), .Vg_0_(c_net2), .Vd_P_2_(c_net4), .Vd_P_3_(c_net3));
    TSMC350nm_VerticalScanner I__2 (.island_num(2), .row(1), .col(1), .In_3_(c_net6));
    TSMC350nm_TA2Cell_NoFG I__3 (.island_num(3), .row(1), .col(1), .DRAIN2(c_net1), .DRAIN1(c_net3));
    TSMC350nm_TA2Cell_Weak I__4 (.island_num(4), .row(1), .col(1), .DRAIN1(c_net4), .DRAIN2(c_net1));
    TSMC350nm_C4 I__5 (.island_num(5), .row(1), .col(1), .DRAIN1(a_net1), .OUTPUT(c_net5));
    TSMC350nm_TA2Cell_Strong I__6 (.island_num(6), .row(1), .col(1));
    TSMC350nm_voltage_DAC_6bit I__7 (.island_num(7), .row(1), .col(1), .BIT_3_(c_net6), .BIT_2_(c_net5));
    TSMC350nm_VMMWTA I__8 (.island_num(8), .row(1), .col(1), .Vg_1_(a_net2));
    frame_10p_10p FRAME (.p_3_(a_net1), .p_27_(a_net2));
    
    
endmodule

module cells_only(port1);
    TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(1), .col(1), .Vd_Pl_0_(d_net5), .Vd_Pl_1_(d_net6), .Vd_Pl_2_(d_net7), .Vd_Pl_3_(d_net8), .Vs_0_(c_net0), .VINJ_0_(c_net1), .Vsel_0_(c_net1a), .Vg_0_(c_net2), .GND_0_(c_net3), .VTUN(c_net4), .GND_1_(c_net5), .Vg_1_(c_net6), .Vsel_1_(c_net6a), .VINJ_1_(c_net1), .Vs_1_(c_net6b), .Vd_P_0_(d_net9), .Vd_P_1_(d_net9a), .Vd_P_2_(d_net9b), .Vd_P_3_(d_net12), .Vd_R_0_(f_net29), .Vd_R_1_(f_net30), .Vd_R_2_(f_net31), .Vd_R_3_(f_net32));
    TSMC350nm_4x2_Direct I__1 (.island_num(0), .row(1), .col(2), .Vd_l_0_(d_net1), .Vd_l_1_(d_net2), .Vd_l_2_(d_net3), .Vd_l_3_(d_net4), .Vs_0_(c_net7), .VINJ_0_(c_net7a), .Vg_0_(c_net8), .GND_0_(c_net9), .VTUN(c_net9a), .GND_1_(c_net9b), .Vg_1_(c_net9c), .VINJ_1_(c_net9d), .Vs_1_(c_net9e), .Vd_0_(d_net13), .Vd_1_(d_net14), .Vd_2_(d_net15), .Vd_3_(d_net16));
    TSMC350nm_VMMWTA_withNFET I__2 (.island_num(0), .row(1), .col(3), .Vd_0_(d_net9), .Vd_1_(d_net9a), .Vd_2_(d_net9b), .Vd_3_(d_net12), .VMM_Vs_0_(c_net15a), .VINJ(c_net16), .VMM_Vg_0_(c_net17), .GND(c_net18), .VTUN_0_(c_net19), .VMM_Vg_1_(c_net20), .VMM_Vs_1_(c_net22), .Ibias_Vs(c_net23), .Ibias_Vg(c_net25), .VTUN_1_(c_net19), .Vout_0_(f_net33), .Vout_1_(f_net34), .Vout_2_(f_net35), .Vout_3_(f_net36), .Vbias(f_net37));
    TSMC350nm_TA2Cell_NoFG I__3 (.island_num(0), .row(1), .col(4), .DRAIN1(d_net13), .DRAIN2(d_net16), .VTUN(c_net10), .GATE1(c_net11), .COLSEL1(c_net12), .VINJ(c_net12a), .GND(c_net13), .VPWR(c_net15), .VIN1_PLUS(f_net38), .VIN1_MINUS(f_net39), .VIN2_PLUS(f_net40), .VIN2_MINUS(f_net41), .OUTPUT1(f_net42), .OUTPUT2(f_net43));
    TSMC350nm_TA2Cell_Weak I__4 (.island_num(0), .row(1), .col(5), .DRAIN1(d_net9), .DRAIN2(d_net12), .VINJ(c_net28), .COLSEL2(c_net28a), .GATE2(c_net29), .VTUN(c_net30), .GND(c_net31), .GATE1(c_net32), .COLSEL1(c_net32a), .VPWR(c_net32b), .VIN1_PLUS(f_net38), .VIN1_MINUS(f_net39), .VIN2_PLUS(f_net40), .VIN2_MINUS(f_net41), .OUTPUT1(f_net44), .OUTPUT2(f_net45));
    TSMC350nm_TA2Cell_Strong I__5 (.island_num(0), .row(1), .col(6), .DRAIN1(d_net13), .DRAIN2(d_net16), .VINJ(c_net39), .COLSEL2(c_net40), .GATE2(c_net41), .VTUN(c_net42), .GND(c_net43), .GATE1(c_net44), .VPWR(c_net44a), .COLSEL1(c_net41a), .VIN1_PLUS(f_net38), .VIN1_MINUS(f_net39), .VIN2_PLUS(f_net40), .VIN2_MINUS(f_net41), .OUTPUT1(f_net46), .OUTPUT2(f_net47));
    TSMC350nm_TA2Cell_LongL I__6 (.island_num(0), .row(1), .col(7), .DRAIN1(d_net9), .DRAIN2(d_net12), .VINJ(c_net46), .COLSEL2(c_net47), .GATE2(c_net48), .VTUN(c_net49), .GND(c_net50), .GATE1(c_net51), .COLSEL1(c_net52), .VPWR(c_net53), .VIN1_PLUS(f_net38), .VIN1_MINUS(f_net39), .VIN2_PLUS(f_net40), .VIN2_MINUS(f_net41), .OUTPUT1(f_net48), .OUTPUT2(f_net49));
    TSMC350nm_ThreePfets I__7 (.island_num(0), .row(1), .col(8), .BODY(s_net1), .SOURCE_SMALL(f_net50), .SOURCE_MED(f_net51), .SOURCE_LARGE(f_net52), .GATE(f_net56), .DRAIN(f_net57));
    TSMC350nm_VerticalScanner I__8 (.island_num(0), .row(1), .col(9), .VDD(s_net1));
    TSMC350nm_ThreeNfets I__9 (.island_num(0), .row(1), .col(10), .SOURCE_SMALL(f_net53), .SOURCE_MED(f_net54), .SOURCE_LARGE(f_net55), .GATE(f_net56), .DRAIN(f_net57));
    

    frame_5mm_1mm FRAME(.VTUN(s_net2), .IO_W_0_(s_net1), .IO_N_0_(f_net1), .IO_N_1_(f_net2), .IO_N_2_(f_net3), .IO_N_3_(f_net4), .IO_N_4_(f_net5), .IO_N_5_(f_net6), .IO_N_6_(f_net7), .IO_N_7_(f_net8), .IO_N_8_(f_net9), .IO_N_9_(f_net10), .IO_N_10_(f_net25), .IO_N_11_(f_net25), .IO_N_12_(f_net26), .IO_N_13_(f_net27), .IO_N_14_(f_net28), .IO_S_4_(f_net29), .IO_S_5_(f_net30), .IO_S_6_(f_net31), .IO_S_7_(f_net32), .IO_S_9_(f_net33), .IO_S_10_(f_net34), .IO_S_11_(f_net35), .IO_S_12_(f_net36), .IO_S_13_(f_net37), .IO_S_14_(f_net38), .IO_S_15_(f_net39), .IO_S_16_(f_net40), .IO_S_17_(f_net41), .IO_S_18_(f_net42), .IO_S_19_(f_net43), .IO_S_20_(f_net44), .IO_S_21_(f_net45), .IO_S_22_(f_net46), .IO_S_23_(f_net47), .IO_S_24_(f_net48), .IO_S_25_(f_net49), .IO_N_15_(f_net50), .IO_N_16_(f_net51), .IO_N_17_(f_net52), .IO_N_18_(f_net53), .IO_N_19_(f_net54), .IO_N_20_(f_net55), .IO_N_21_(f_net56), .IO_N_22_(f_net57));

    TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4), .decode_n0_ENABLE(f_net23), .decode_n0_VGRUN_0_(f_net24), .decode_n0_VGRUN_1_(f_net25), .decode_n0_VGRUN_2_(f_net26), .decode_n0_VGRUN_3_(f_net27), .decode_n1_VGRUN_0_(f_net24), .decode_n1_VGRUN_1_(f_net25), .decode_n1_VGRUN_2_(f_net26), .decode_n1_VGRUN_3_(f_net27), .decode_n2_VGRUN_0_(f_net24), .decode_n2_VGRUN_1_(f_net25), .decode_n2_VGRUN_2_(f_net26), .decode_n2_VGRUN_3_(f_net27), .decode_n3_VGRUN_0_(f_net24), .decode_n3_VGRUN_1_(f_net25), .decode_n3_VGRUN_2_(f_net26), .decode_n3_VGRUN_3_(f_net27), .decode_n0_n0_IN_0_(f_net19), .decode_n0_n0_IN_1_(f_net20), .decode_n2_n0_IN_0_(f_net21), .decode_n2_n0_IN_1_(f_net22), .decode_n2_n3_RUN_OUT_3_(net_ext0), .decode_n2_n3_OUT_3_(net_ext1));
    TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(7), .switch_n1_VVINJ_0_(c_net7), .switch_n1_VINJV_0_(c_net7a), .switch_n1_VG_0_(c_net8), .switch_n1_GNDV_0_(c_net9), .switch_n1_VTUN(c_net9a), .switch_n1_GNDV_1_(c_net9b), .switch_n1_VG_1_(c_net9c), .switch_n1_VINJV_1_(c_net9d), .switch_n1_VVINJ_1_(c_net9e), .switch_n1_VTUN_T(s_net2));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(1), .VDD_0_(c_net0), .VINJ(c_net1), .CTRL_B_0_(c_net1a), .Vg_0_(c_net2), .GND_0_(c_net3), .VTUN(c_net4), .GNDV_1_(c_net5), .Vg_1_(c_net6), .CTRL_B_1_(c_net6a), .VDD_1_(c_net6b), .VPWR_0_(s_net1), .VPWR_1_(s_net1), .VTUN_T(s_net2));
    TSMC350nm_IndirectSwc_VMMWTA switch_ind(.island_num(0), .direction(horizontal), .col(3), .VVINJ_0_(c_net15a), .VINJV_0_(c_net16), .VG_0_(c_net17), .GNDV_0_(c_net18), .VTUN(c_net19), .VG_1_(c_net20), .VVINJ_1_(c_net22), .VVINJ_2_(c_net23), .VG_2_(c_net25), .VTUN_T(s_net2), .RUN_IN_2_(net_ext0), .decode_2_(net_ext1));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(4), .VTUN(c_net10), .Vg_1_(c_net11), .CTRL_B_1_(c_net12), .VINJ(c_net12a), .GNDV_1_(c_net13), .VDD_1_(c_net15), .VPWR_0_(s_net1), .VPWR_1_(s_net1), .VTUN_T(s_net2));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(5), .VINJ(c_net28), .CTRL_B_0_(c_net28a), .Vg_0_(c_net29), .VTUN(c_net30), .GNDV_1_(c_net31), .Vg_1_(c_net32), .CTRL_B_1_(c_net32a), .VDD_1_(c_net32b), .VPWR_0_(s_net1), .VPWR_1_(s_net1), .VTUN_T(s_net2));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(6), .VINJ(c_net39), .CTRL_B_0_(c_net40), .Vg_0_(c_net41), .VTUN(c_net42), .GNDV_1_(c_net43), .Vg_1_(c_net44), .VDD_1_(c_net44a), .CTRL_B_1_(c_net41a), .VPWR_0_(s_net1), .VPWR_1_(s_net1), .VTUN_T(s_net2));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(7), .VINJ(c_net46), .CTRL_B_0_(c_net47), .Vg_0_(c_net48), .VTUN(c_net49), .GNDV_1_(c_net50), .Vg_1_(c_net51), .CTRL_B_1_(c_net52), .VDD_1_(c_net53), .VPWR_0_(s_net1), .VPWR_1_(s_net1), .VTUN_T(s_net2));

    TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(3), .decode_n0_ENABLE(f_net18), .decode_n0_IN_0_(f_net15), .decode_n2_IN_0_(f_net16), .decode_n2_IN_1_(f_net17));
    TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(2), .type(drain_select), .switch_n0_DRAINRAIL(f_net1));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(2), .type(prog_switch), .switch_n0_B_0_(d_net1), .switch_n0_B_1_(d_net2), .switch_n0_B_2_(d_net3), .switch_n0_B_3_(d_net4), .switch_n1_B_0_(d_net5), .switch_n1_B_1_(d_net6), .switch_n1_B_2_(d_net7), .switch_n1_B_3_(d_net8));

    TSMC350nm_cellFrame_digitalHelperCells I__10 (.island_num(1), .row(1), .col(1), .LVL_IN_0_(f_net2), .LVL_OUT_0_(f_net15), .LVL_IN_1_(f_net3), .LVL_OUT_1_(f_net16), .LVL_IN_2_(f_net4), .LVL_OUT_2_(f_net17), .LVL_IN_3_(f_net5), .LVL_OUT_3_(f_net18), .LVL_IN_4_(f_net6), .LVL_OUT_4_(f_net19), .LVL_IN_5_(f_net7), .LVL_OUT_5_(f_net20), .LVL_IN_6_(f_net8), .LVL_OUT_6_(f_net21), .LVL_IN_7_(f_net9), .LVL_OUT_7_(f_net22), .LVL_IN_8_(f_net10), .LVL_OUT_8_(f_net23), .LVL_IN_13_(f_net28));


endmodule

module synthesized_cell_island_v1(port1);
    TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(1), .col(1), .Vd_Pl_0_(d_net5), .Vd_Pl_1_(d_net6), .Vd_Pl_2_(d_net7), .Vd_Pl_3_(d_net8), .Vd_P_0_(d_net9), .Vd_P_1_(d_net10), .Vd_P_2_(d_net11), .Vd_P_3_(d_net12), .Vs_0_(c_net0), .VINJ_0_(c_net1), .Vsel_0_(c_net1a), .Vg_0_(c_net2), .GND_0_(c_net3), .VTUN(c_net4), .GND_1_(c_net5), .Vg_1_(c_net6), .Vsel_1_(c_net6a), .VINJ_1_(c_net1), .Vs_1_(c_net6b), .Vd_R_0_(o_net1), .Vd_R_1_(o_net2), .Vd_R_2_(o_net3), .Vd_R_3_(o_net4));
    TSMC350nm_4x2_Direct I__1 (.island_num(0), .row(1), .col(2), .Vd_l_0_(d_net1), .Vd_l_1_(d_net2), .Vd_l_2_(d_net3), .Vd_l_3_(d_net4), .Vd_0_(d_net13), .Vd_1_(d_net14), .Vd_2_(d_net15), .Vd_3_(d_net16), .Vs_0_(c_net7), .VINJ_0_(c_net7a), .Vg_0_(c_net8), .GND_0_(c_net9), .VTUN(c_net9a), .GND_1_(c_net9b), .Vg_1_(c_net9c), .VINJ_1_(c_net9d), .Vs_1_(c_net9e));
    TSMC350nm_TA2Cell_NoFG I__3 (.island_num(0), .row(1), .col(3), .DRAIN2(d_net9), .DRAIN1(d_net10), .VTUN(c_net10), .GATE1(c_net11), .COLSEL1(c_net12), .VINJ(c_net12a), .GND(c_net13), .VPWR(c_net15), .OUTPUT1(o_net10), .OUTPUT2(o_net11));
    TSMC350nm_VMMWTA I__2 (.island_num(0), .row(1), .col(4), .Vd_0_(d_net13), .Vd_1_(d_net14), .Vd_2_(d_net15), .Vd_3_(d_net16), .Vs_0_(c_net15a), .VINJ_0_(c_net16), .Vg_0_(c_net17), .GND(c_net18), .VTUN_0_(c_net19), .GND_1_(c_net19a), .Vg_1_(c_net20), .VINJ_1_(c_net21), .Vs_1_(c_net22), .VINJ_2_(c_net21), .Vs_2_(c_net23), .VINJ_3_(c_net24), .Vg_2_(c_net25), .VTUN_1_(c_net19), .VINJ_4_(c_net24), .Prog_0_(s_net2));
    TSMC350nm_TA2Cell_Weak I__4 (.island_num(0), .row(1), .col(5), .DRAIN1(d_net9), .DRAIN2(d_net12), .VINJ_1_(c_net28), .COLSEL2(c_net28a), .GATE2(c_net29), .VTUN(c_net30), .GND(c_net31), .GATE1(c_net32), .COLSEL1(c_net32a), .VINJ_0_(c_net28), .RUN(s_net1), .PROG(s_net2), .VPWR(c_net32b), .OUTPUT1(o_net12), .OUTPUT2(o_net5));
    TSMC350nm_C4 I__5 (.island_num(0), .row(1), .col(6), .DRAIN1(d_net13), .DRAIN2(d_net14), .VINJ1(c_net34), .COLSEL2(c_net34a), .GATE2(c_net35), .VTUN(c_net36), .GND(c_net37), .GATE1(c_net38), .COLSEL1(c_net38a), .VINJ0(c_net34), .RUN(s_net1), .PROG(s_net2), .VPWR(c_net38b), .OUTPUT(o_net6));
    TSMC350nm_TA2Cell_Strong I__6 (.island_num(0), .row(1), .col(7), .DRAIN1(d_net9), .DRAIN2(d_net12), .VINJ_1_(c_net39), .COLSEL2(c_net40), .GATE2(c_net41), .VTUN(c_net42), .GND(c_net43), .GATE1(c_net44), .VINJ_0_(c_net39), .RUN(s_net1), .PROG(s_net2), .VPWR(c_net44a), .OUTPUT1(o_net7), .OUTPUT2(o_net8));
    TSMC350nm_VerticalScanner I__7 (.island_num(0), .row(1), .col(8), .VDD(s_net3), .Qout(o_net9));

    TSMC350nm_16out_AnalogMux I__8 (.island_num(1), .row(1), .col(1), .TG_IN_0_(o_net1), .TG_IN_1_(o_net2), .TG_IN_2_(o_net3), .TG_IN_3_(o_net4), .TG_IN_4_(d_net13), .TG_IN_5_(d_net14), .TG_IN_6_(d_net15), .TG_IN_7_(d_net16), .TG_IN_8_(o_net12), .TG_IN_9_(o_net6), .TG_IN_10_(o_net5), .TG_IN_11_(o_net7), .TG_IN_12_(o_net8), .TG_IN_13_(o_net9), .TG_IN_14_(o_net10), .TG_IN_15_(o_net11), .TG_OUT(f_net1));
    /*TSMC350nm_voltage_DAC_6bit I__9 (.island_num(2), .row(1), .col(1), .DAC_OUT(f_net2));*/
    
    frame_5mm_1mm FRAME (.IO_S_6_(s_net2), .IO_S_7_(s_net3), .IO_S_11_(f_net1), .N_IO_11_(f_net2), .N_IO_1_(f_net3), .IO_W_0_(f_net4));
    
    TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4), .decode_n0_VGRUN_0_(f_net3));
    TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(8), .switch_n1_VVINJ_0_(c_net7), .switch_n1_VINJV_0_(c_net7a), .switch_n1_VG_0_(c_net8), .switch_n1_GNDV_0_(c_net9), .switch_n1_VTUN(c_net9a), .switch_n1_GNDV_1_(c_net9b), .switch_n1_VG_1_(c_net9c), .switch_n1_VINJV_1_(c_net9d), .switch_n1_VVINJ_1_(c_net9e));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(1), .VDD_0_(c_net0), .VINJ(c_net1), .CTRL_B_0_(c_net1a), .Vg_0_(c_net2), .GND_0_(c_net3), .VTUN(c_net4), .GNDV_1_(c_net5), .Vg_1_(c_net6), .CTRL_B_1_(c_net6a), .VDD_1_(c_net6b), .PROG(s_net2));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(3), .VTUN(c_net10), .Vg_1_(c_net11), .CTRL_B_1_(c_net12), .VINJ(c_net12a), .GNDV_1_(c_net13), .VDD_1_(c_net15));
    TSMC350nm_IndirectSwc_VMMWTA switch_ind(.island_num(0), .direction(horizontal), .col(4), .VVINJ_0_(c_net15a), .VINJV_0_(c_net16), .VG_0_(c_net17), .GNDV_0_(c_net18), .VTUN(c_net19), .GNDV_1_(c_net19a), .VG_1_(c_net20), .VINJV_1_(c_net21), .VVINJ_1_(c_net22), .VVINJ_2_(c_net23), .VINJV_2_(c_net24), .VG_2_(c_net25));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(5), .VINJ(c_net28), .CTRL_B_0_(c_net28a), .Vg_0_(c_net29), .VTUN(c_net30), .GNDV_1_(c_net31), .Vg_1_(c_net32), .CTRL_B_1_(c_net32a), .VDD_1_(c_net32b));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(6), .VINJ(c_net34), .CTRL_B_0_(c_net34a), .Vg_0_(c_net35), .VTUN(c_net36), .GNDV_1_(c_net37), .Vg_1_(c_net38), .CTRL_B_1_(c_net38a), .VDD_1_(c_net38b));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(7), .VINJ(c_net39), .CTRL_B_0_(c_net40), .Vg_0_(c_net41), .VTUN(c_net42), .GNDV_1_(c_net43), .Vg_1_(c_net44), .VDD_1_(c_net44a));
    TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(3), .decode_n0_IN_0_(f_net4));
    TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(2), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(2), .type(prog_switch), .switch_n0_B_0_(d_net1), .switch_n0_B_1_(d_net2), .switch_n0_B_2_(d_net3), .switch_n0_B_3_(d_net4), .switch_n1_B_0_(d_net5), .switch_n1_B_1_(d_net6), .switch_n1_B_2_(d_net7), .switch_n1_B_3_(d_net8));

endmodule

module pre_macro_cell_island(port1);
    TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(1), .col(1), .Vd_Pl_0_(d_net5), .Vd_Pl_1_(d_net6), .Vd_Pl_2_(d_net7), .Vd_Pl_3_(d_net8), .Vs_0_(c_net0), .VINJ_0_(c_net1), .Vsel_0_(c_net1a), .Vg_0_(c_net2), .GND_0_(c_net3), .VTUN(c_net4), .GND_1_(c_net5), .Vg_1_(c_net6), .Vsel_1_(c_net6a), .VINJ_1_(c_net1), .Vs_1_(c_net6b), .Vd_P_0_(d_net9), .Vd_P_3_(d_net12));
    TSMC350nm_4x2_Direct I__1 (.island_num(0), .row(1), .col(2), .Vd_l_0_(d_net1), .Vd_l_1_(d_net2), .Vd_l_2_(d_net3), .Vd_l_3_(d_net4), .Vs_0_(c_net7), .VINJ_0_(c_net7a), .Vg_0_(c_net8), .GND_0_(c_net9), .VTUN(c_net9a), .GND_1_(c_net9b), .Vg_1_(c_net9c), .VINJ_1_(c_net9d), .Vs_1_(c_net9e), .Vd_0_(d_net13), .Vd_1_(d_net14), .Vd_2_(d_net15), .Vd_3_(d_net16));
    TSMC350nm_TA2Cell_NoFG I__2 (.island_num(0), .row(1), .col(3), .DRAIN1(d_net9), .DRAIN2(d_net12), .VTUN(c_net10), .GATE1(c_net11), .COLSEL1(c_net12), .VINJ(c_net12a), .GND(c_net13), .VPWR(c_net15));
    TSMC350nm_VMMWTA_withNFET I__3 (.island_num(0), .row(1), .col(4), .Vd_0_(d_net13), .Vd_1_(d_net14), .Vd_2_(d_net15), .Vd_3_(d_net16), .VMM_Vs_0_(c_net15a), .VINJ(c_net16), .VMM_Vg_0_(c_net17), .GND(c_net18), .VTUN_0_(c_net19), .VMM_Vg_1_(c_net20), .VMM_Vs_1_(c_net22), .Ibias_Vs(c_net23), .Ibias_Vg(c_net25), .VTUN_1_(c_net19));
    TSMC350nm_TA2Cell_Weak I__4 (.island_num(0), .row(1), .col(5), .DRAIN1(d_net9), .DRAIN2(d_net12), .VINJ(c_net28), .COLSEL2(c_net28a), .GATE2(c_net29), .VTUN(c_net30), .GND(c_net31), .GATE1(c_net32), .COLSEL1(c_net32a), .VPWR(c_net32b));
    TSMC350nm_TA2Cell_Strong I__5 (.island_num(0), .row(1), .col(6), .DRAIN1(d_net13), .DRAIN2(d_net16), .VINJ(c_net39), .COLSEL2(c_net40), .GATE2(c_net41), .VTUN(c_net42), .GND(c_net43), .GATE1(c_net44), .VPWR(c_net44a), .COLSEL1(c_net41a));
    TSMC350nm_TA2Cell_LongL I__6 (.island_num(0), .row(1), .col(7), .DRAIN1(d_net9), .DRAIN2(d_net12), .VINJ(c_net46), .COLSEL2(c_net47), .GATE2(c_net48), .VTUN(c_net49), .GND(c_net50), .GATE1(c_net51), .COLSEL1(c_net52), .VPWR(c_net53));
    TSMC350nm_ThreePfets I__7 (.island_num(0), .row(1), .col(8));
    TSMC350nm_VerticalScanner I__8 (.island_num(0), .row(1), .col(9));
    TSMC350nm_ThreeNfets I__9 (.island_num(0), .row(1), .col(10));
    

    frame_5mm_1mm FRAME(.IO_S_6_(s_net2));

    TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
    TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(7), .switch_n1_VVINJ_0_(c_net7), .switch_n1_VINJV_0_(c_net7a), .switch_n1_VG_0_(c_net8), .switch_n1_GNDV_0_(c_net9), .switch_n1_VTUN(c_net9a), .switch_n1_GNDV_1_(c_net9b), .switch_n1_VG_1_(c_net9c), .switch_n1_VINJV_1_(c_net9d), .switch_n1_VVINJ_1_(c_net9e));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(1), .VDD_0_(c_net0), .VINJ(c_net1), .CTRL_B_0_(c_net1a), .Vg_0_(c_net2), .GND_0_(c_net3), .VTUN(c_net4), .GNDV_1_(c_net5), .Vg_1_(c_net6), .CTRL_B_1_(c_net6a), .VDD_1_(c_net6b));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(3), .VTUN(c_net10), .Vg_1_(c_net11), .CTRL_B_1_(c_net12), .VINJ(c_net12a), .GNDV_1_(c_net13), .VDD_1_(c_net15));
    TSMC350nm_IndirectSwc_VMMWTA switch_ind(.island_num(0), .direction(horizontal), .col(4), .VVINJ_0_(c_net15a), .VINJV_0_(c_net16), .VG_0_(c_net17), .GNDV_0_(c_net18), .VTUN(c_net19), .VG_1_(c_net20), .VVINJ_1_(c_net22), .VVINJ_2_(c_net23), .VG_2_(c_net25));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(5), .VINJ(c_net28), .CTRL_B_0_(c_net28a), .Vg_0_(c_net29), .VTUN(c_net30), .GNDV_1_(c_net31), .Vg_1_(c_net32), .CTRL_B_1_(c_net32a), .VDD_1_(c_net32b));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(6), .VINJ(c_net39), .CTRL_B_0_(c_net40), .Vg_0_(c_net41), .VTUN(c_net42), .GNDV_1_(c_net43), .Vg_1_(c_net44), .VDD_1_(c_net44a), .CTRL_B_1_(c_net41a));
    TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(7), .VINJ(c_net46), .CTRL_B_0_(c_net47), .Vg_0_(c_net48), .VTUN(c_net49), .GNDV_1_(c_net50), .Vg_1_(c_net51), .CTRL_B_1_(c_net52), .VDD_1_(c_net53));

    TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(3));
    TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(2), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(2), .type(prog_switch), .switch_n0_B_0_(d_net1), .switch_n0_B_1_(d_net2), .switch_n0_B_2_(d_net3), .switch_n0_B_3_(d_net4), .switch_n1_B_0_(d_net5), .switch_n1_B_1_(d_net6), .switch_n1_B_2_(d_net7), .switch_n1_B_3_(d_net8));


endmodule
