module cells_only(port1);
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