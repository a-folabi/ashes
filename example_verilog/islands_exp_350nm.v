module TOP(port1);
	/*Tile Verilog*/
	/* C, S, C blocks of the tile */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(7), .Vs_b_0_row_4(c_net60[0:7]), .Vs_b_1_row_4(c_net61[0:7]), .Vsel_b_0_row_4(c_net64[0:7]), .Vsel_b_1_row_4(c_net65[0:7]), .Vg_b_0_row_4(c_net70[0:7]), .Vg_b_1_row_4(c_net71[0:7]), .VTUN_brow_4(c_net72[0:7]), .VINJ_b_1_row_4(c_net79[0:7]), .GND_b_1_row_4(c_net80[0:7]));
	S_BLOCK_SEC1_PINS I__1 (.island_num(0), .row(0), .col(7), .matrix_row(5), .matrix_col(1), .VINJ_brow_4(c_net81[0:1]), .GND_b_1_row_4(c_net82[0:1]), .Vsel_b_1_row_4(c_net66[0:1]), .Vsel_b_0_row_4(c_net67[0:1]), .Vg_b_1_row_4(c_net73[0:1]), .Vg_b_0_row_4(c_net74[0:1]), .VTUN_brow_4(c_net75[0:1]));
	/* , .w_0_col_0(f_net57[0:5]), .w_1_col_0(f_net58[0:5]), .w_2_col_0(f_net59[0:5]), .w_3_col_0(f_net60[0:5])*/
	S_BLOCK_BUFFER I__3 (.island_num(0), .row(0), .col(8), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SPACE_UP_PINS I__4 (.island_num(0), .row(0), .col(9), .matrix_row(4), .matrix_col(1), .n_0_row_0(f_net10), .n_1_row_0(f_net11), .n_2_row_0(f_net12), .n_3_row_0(f_net13));
	S_BLOCK_CONN_PINS I__5 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1), .s_0_row_0(f_net10b), .s_1_row_0(f_net11b), .s_2_row_0(f_net12b), .s_3_row_0(f_net13b));
	S_BLOCK_SPACE_UP_PINS I__6 (.island_num(0), .row(0), .col(10), .matrix_row(3), .matrix_col(1), .n_0_row_0(f_net14), .n_1_row_0(f_net15), .n_2_row_0(f_net16), .n_3_row_0(f_net17));
	S_BLOCK_CONN_PINS I__7 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__8 (.island_num(0), .row(4), .col(10), .matrix_row(1), .matrix_col(1), .s_0_row_0(f_net14b), .s_1_row_0(f_net15b), .s_2_row_0(f_net16b), .s_3_row_0(f_net17b));
	S_BLOCK_SPACE_UP_PINS I__9 (.island_num(0), .row(0), .col(11), .matrix_row(2), .matrix_col(1), .n_0_row_0(f_net18), .n_1_row_0(f_net19), .n_2_row_0(f_net20), .n_3_row_0(f_net21));
	S_BLOCK_CONN_PINS I__10 (.island_num(0), .row(2), .col(11), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__11 (.island_num(0), .row(3), .col(11), .matrix_row(2), .matrix_col(1), .s_0_row_1(f_net18b), .s_1_row_1(f_net19b), .s_2_row_1(f_net20b), .s_3_row_1(f_net21b));
	S_BLOCK_SPACE_UP_PINS I__12 (.island_num(0), .row(0), .col(12), .matrix_row(1), .matrix_col(1), .n_0_row_0(f_net22), .n_1_row_0(f_net23), .n_2_row_0(f_net24), .n_3_row_0(f_net25));
	S_BLOCK_CONN_PINS I__13 (.island_num(0), .row(1), .col(12), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__14 (.island_num(0), .row(2), .col(12), .matrix_row(3), .matrix_col(1), .s_0_row_2(f_net22b), .s_1_row_2(f_net23b), .s_2_row_2(f_net24b), .s_3_row_2(f_net25b));
	S_BLOCK_CONN_PINS I__15 (.island_num(0), .row(0), .col(13), .matrix_row(1), .matrix_col(1), .n_0_row_0(f_net26), .n_1_row_0(f_net27), .n_2_row_0(f_net28), .n_3_row_0(f_net29));
	S_BLOCK_SPACE_DOWN_PINS I__16 (.island_num(0), .row(1), .col(13), .matrix_row(4), .matrix_col(1), .s_0_row_3(f_net26b), .s_1_row_3(f_net27b), .s_2_row_3(f_net28b), .s_3_row_3(f_net29b));
	S_BLOCK_SEC2_PINS I__17 (.island_num(0), .row(0), .col(14), .matrix_row(5), .matrix_col(1), .VINJ_brow_4(c_net81a[0:1]), .GND_b_1_row_4(c_net82a[0:1]), .Vsel_b_1_row_4(c_net66a[0:1]), .Vsel_b_0_row_4(c_net67a[0:1]), .Vg_b_1_row_4(c_net73a[0:1]), .Vg_b_0_row_4(c_net74a[0:1]), .VTUN_brow_4(c_net75a[0:1]));
	S_BLOCK_23CONN I__18 (.island_num(0), .row(0), .col(15), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SEC3_PINS I__19 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(1), .VINJ_brow_4(c_net81b[0:1]), .GND_b_1_row_4(c_net82b[0:1]), .Vsel_b_1_row_4(c_net66b[0:1]), .Vsel_b_0_row_4(c_net67b[0:1]), .Vg_b_1_row_4(c_net73b[0:1]), .Vg_b_0_row_4(c_net74b[0:1]), .VTUN_brow_4(c_net75b[0:1]));

	TSMC350nm_4x2_Indirect I__2 (.island_num(0), .row(0), .col(17), .matrix_row(5), .matrix_col(9), .Vs_b_0_row_4(c_net62[0:9]), .Vs_b_1_row_4(c_net63[0:9]), .Vsel_b_0_row_4(c_net68[0:9]), .Vsel_b_1_row_4(c_net69[0:9]), .Vg_b_0_row_4(c_net76[0:9]), .Vg_b_1_row_4(c_net77[0:9]), .VTUN_brow_4(c_net78[0:9]), .VINJ_b_1_row_4(c_net83[0:9]), .GND_b_1_row_4(c_net84[0:9]));
	TSMC350nm_4TGate_ST_BMatrix I_20 (.island_num(0), .row(0), .col(26), .matrix_row(5), .matrix_col(1), .A_0_col_0(f_net38[0:5]), .A_1_col_0(f_net39[0:5]), .A_2_col_0(f_net40[0:5]), .A_3_col_0(f_net41[0:5]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5), .decode_n0_IN_0_(f_net33), .decode_n2_IN_0_(f_net34), .decode_n2_IN_1_(f_net35), .decode_n4_IN_0_(f_net36), .decode_n4_IN_1_(f_net37));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select), .switch_n0_prog_drainrail(f_net8), .switch_n0_run_drainrail(f_net9));
    TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));

	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6), .decode_n0_ENABLE(f_net1), .decode_n0_n0_IN_0_(f_net2), .decode_n0_n0_IN_1_(f_net3), .decode_n2_n0_IN_0_(f_net4), .decode_n2_n0_IN_1_(f_net5), .decode_n4_n0_IN_0_(f_net6), .decode_n4_n0_IN_1_(f_net7), .decode_n0_VINJV(p_net1) , .decode_n0_GNDV(p_net2), .decode_n10_VGRUN_0_(f_net48), .decode_n10_VGRUN_1_(f_net49), .decode_n10_VGRUN_2_(f_net50), .decode_n10_VGRUN_3_(f_net51), .decode_n2_VGRUN_0_(f_net52), .decode_n2_VGRUN_1_(f_net53), .decode_n2_VGRUN_2_(f_net54), .decode_n2_VGRUN_3_(f_net55), .decode_n4_n4_OUT_0_(d_net0), .decode_n4_n4_OUT_1_(d_net1), .decode_n4_n4_OUT_2_(d_net2), .decode_n4_n4_OUT_3_(d_net3), .decode_n4_n5_OUT_0_(d_net4), .decode_n4_n5_OUT_1_(d_net5), .decode_n4_n5_OUT_2_(d_net6), .decode_n4_n5_OUT_3_(d_net7), .decode_n4_n6_OUT_0_(d_net8), .decode_n4_n6_OUT_1_(d_net9), .decode_n4_n6_OUT_2_(d_net10), .decode_n4_n6_OUT_3_(d_net11), .decode_n4_n7_OUT_0_(d_net12), .decode_n4_n7_OUT_1_(d_net13), .decode_n4_n7_OUT_2_(d_net14), .decode_n4_n7_OUT_3_(d_net15), .decode_n4_n8_OUT_0_(d_net16), .decode_n4_n8_OUT_1_(d_net17), .decode_n4_n8_OUT_2_(d_net18), .decode_n4_n8_OUT_3_(d_net19));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(26), .switch_n0_VTUN_T(p_net0), .switch_n14_decode_0_(d_net0), .switch_n14_VPWR_0_(fake_net1), .switch_n14_decode_1_(d_net1), .switch_n14_VPWR_1_(fake_net2), .switch_n15_decode_0_(d_net2), .switch_n15_VPWR_0_(fake_net4), .switch_n15_decode_1_(d_net3), .switch_n15_VPWR_1_(fake_net5), .switch_n16_decode_0_(d_net4), .switch_n16_VPWR_0_(fake_net6), .switch_n16_decode_1_(d_net5), .switch_n16_VPWR_1_(fake_net7), .switch_n17_decode_0_(d_net6), .switch_n17_VPWR_0_(fake_net8), .switch_n17_decode_1_(d_net7), .switch_n17_VPWR_1_(fake_net9), .switch_n18_decode_0_(d_net8), .switch_n18_VPWR_0_(fake_net10), .switch_n18_decode_1_(d_net9), .switch_n18_VPWR_1_(fake_net11), .switch_n19_decode_0_(d_net10), .switch_n19_VPWR_0_(fake_net12), .switch_n19_decode_1_(d_net11), .switch_n19_VPWR_1_(fake_net13), .switch_n20_decode_0_(d_net12), .switch_n20_VPWR_0_(fake_net14), .switch_n20_decode_1_(d_net13), .switch_n20_VPWR_1_(fake_net15), .switch_n21_decode_0_(d_net14), .switch_n21_VPWR_0_(fake_net16), .switch_n21_decode_1_(d_net15), .switch_n21_VPWR_1_(fake_net17), .switch_n22_decode_0_(d_net16), .switch_n22_VPWR_0_(fake_net18), .switch_n22_decode_1_(d_net17), .switch_n22_VPWR_1_(fake_net19), .switch_n23_decode_0_(d_net18), .switch_n23_VPWR_0_(fake_net20), .switch_n23_decode_1_(d_net19), .switch_n23_VPWR_1_(fake_net21));

	none switch_ind (.island_num(0), .direction(horizontal), .col(8));
	none switch_ind (.island_num(0), .direction(horizontal), .col(9));
	none switch_ind (.island_num(0), .direction(horizontal), .col(10));
	none switch_ind (.island_num(0), .direction(horizontal), .col(11));
	none switch_ind (.island_num(0), .direction(horizontal), .col(12));
	none switch_ind (.island_num(0), .direction(horizontal), .col(13));
	none switch_ind (.island_num(0), .direction(horizontal), .col(15));

	/* CAB elements of tile*/
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__6 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(1), .col(0), .matrix_row(7), .matrix_col(8), .VTUN_brow_6(fake_net0[0:8]));
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__8 (.island_num(1), .row(0), .col(8), .matrix_row(1), .matrix_col(9));
	TSMC350nm_4x2_Indirect I__4 (.island_num(1), .row(1), .col(8), .matrix_row(6), .matrix_col(9));
	TSMC350nm_4x2_Indirect_bot_B_matrx I__9 (.island_num(1), .row(7), .col(8), .matrix_row(1), .matrix_col(9), .fg_purow_0(fake_net3[0:9]));
	TSMC350nm_4TGate_ST_BMatrix I__10(.island_num(1), .row(0), .col(17), .matrix_row(8), .matrix_col(1), .P_0_col_0(c_net18[0:8]), .P_1_col_0(c_net19[0:8]), .P_2_col_0(c_net20[0:8]), .P_3_col_0(c_net21[0:8]), .A_0_col_0(c_net22[0:8]), .A_1_col_0(c_net23[0:8]), .A_2_col_0(c_net24[0:8]), .A_3_col_0(c_net25[0:8]));
	TSMC350nm_OutMtrx_IndrctSwcs I__7 (.island_num(1), .row(9), .col(8), .matrix_row(1), .matrix_col(9));
	TSMC350nm_4x2_Indirect I__5 (.island_num(1), .row(10), .col(8), .matrix_row(2), .matrix_col(9), .Vg_0_row_0(fake_net22[0:9]));
	TSMC350nm_4TGate_ST_BMatrix I__11 (.island_num(1), .row(10), .col(17), .matrix_row(2), .matrix_col(1), .A_0_col_0(f_net30[0:2]), .A_1_col_0(f_net31[0:2]), .A_2_col_0(f_net32[0:2]), .A_3_col_0(f_net56[0:2]));
	TSMC350nm_TA2Cell_Weak cab_device_0 (.island_num(1), .row(2), .col(18), .OUTPUT1(c_net1), .OUTPUT2(c_net2), .VD_P_0_(c_net19[0]), .VD_P_1_(c_net21[0]), .VIN1_PLUS(c_net22[0]), .VIN1_MINUS(c_net23[0]), .VIN2_PLUS(c_net24[0]), .VIN2_MINUS(c_net25[0]), .Vsel_1_(c_net26), .Vg_1_(c_net27), .VTUN(c_net28), .Vg_0_(c_net29), .Vsel_0_(c_net30), .VINJ(c_net31), .GND(c_net32), .VPWR(c_net33), .Vsel_b_0_(c_net34), .RUN_b(c_net35), .Vg_b_0_(c_net36), .PROG_b(c_net37), .VTUN_b(c_net38), .Vg_b_1_(c_net39), .Vsel_b_1_(c_net40), .VINJ_b(c_net41), .GND_b(c_net42), .VPWR_b(c_net43) );
	TSMC350nm_TA2Cell_Weak cab_device_1 (.island_num(1), .row(3), .col(18), .OUTPUT1(c_net2), .OUTPUT2(c_net3), .VD_P_0_(c_net18[1]), .VD_P_1_(c_net21[1]), .VIN1_PLUS(c_net22[1]), .VIN1_MINUS(c_net23[1]), .VIN2_PLUS(c_net24[1]), .VIN2_MINUS(c_net25[1]), .Vsel_0_(c_net34), .RUN(c_net35), .Vg_0_(c_net36), .PROG(c_net37), .VTUN(c_net38), .Vg_1_(c_net39), .Vsel_1_(c_net40), .VINJ(c_net41), .GND(c_net42), .VPWR(c_net43), .COLSEL2_b(c_net44), .RUN_b(c_net45), .GATE2_b(c_net46), .PROG_b(c_net47), .VTUN_b(c_net48), .GATE1_b(c_net49), .COLSEL1_b(c_net50), .VINJ_b(c_net51), .GND_b(c_net52), .VPWR_b(c_net53));
	TSMC350nm_TA2Cell_Strong cab_device_2 (.island_num(1), .row(4), .col(18), .OUTPUT1(c_net4), .OUTPUT2(c_net5), .VD_P_0_(c_net18[2]), .VD_P_1_(c_net21[2]), .VIN1_PLUS(c_net22[2]), .VIN1_MINUS(c_net23[2]), .VIN2_PLUS(c_net24[2]), .VIN2_MINUS(c_net25[2]), .COLSEL2(c_net44), .RUN(c_net45), .GATE2(c_net46), .PROG(c_net47), .VTUN(c_net48), .GATE1(c_net49), .COLSEL1(c_net50), .VINJ(c_net51), .GND(c_net52), .VPWR(c_net53), .VTUN_b(c_net54), .GATE1_b(c_net55), .COLSEL1_b(c_net56), .VINJ_b(c_net57), .GND_b(c_net58), .VPWR_b(c_net59));
	TSMC350nm_4WTA_IndirectProg cab_device_3 (.island_num(1), .row(5), .col(18), .Vout_0_(c_net8), .Vout_1_(c_net9), .Vout_2_(c_net10), .Vout_3_(c_net11), .Vmid(c_net12), .vbias(c_net13), .Iin_0_(c_net22[3]), .Iin_1_(c_net23[3]), .Iin_2_(c_net24[3]), .Iin_3_(c_net25[3]), .Vd_P_0_(c_net18[3]), .Vd_P_1_(c_net19[3]), .Vd_P_2_(c_net20[3]), .Vd_P_3_(c_net21[3]));
	TSMC350nm_Cap_Bank cab_device_4 (.island_num(1), .row(6), .col(18), .OUT_0_(c_net14), .OUT_1_(c_net15), .VD_P_0_(c_net18[4]), .VD_P_1_(c_net19[4]), .VD_P_2_(c_net20[4]), .VD_P_3_(c_net21[4]), .VIN_0_(c_net22[4]), .VIN_1_(c_net23[4]));
	TSMC350nm_NandPfets cab_device_5 (.island_num(1), .row(7), .col(18), .GATE_N(c_net22[5]), .SOURCE_N(c_net23[5]), .GATE_P(c_net24[5]), .SOURCE_P(c_net25[5]));
	TSMC350nm_TGate_2nMirror cab_device_6 (.island_num(1), .row(8), .col(18), .IN_CM_0_(c_net22[6]), .IN_CM_1_(c_net23[6]), .SelN(c_net24[6]), .IN_TG(c_net25[6]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6), .decode_n0_IN_0_(f_net42), .decode_n0_IN_1_(f_net43), .decode_n2_IN_0_(f_net44), .decode_n2_IN_1_(f_net45), .decode_n4_IN_0_(f_net46), .decode_n4_IN_1_(f_net47));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(1), .direction(vertical), .num(12), .type(drain_select), .switch_n0_prog_drainrail(f_net8), .switch_n0_run_drainrail(f_net9));
    TSMC350nm_4TGate_ST_draincutoff switch(.island_num(1), .direction(vertical), .num(12), .type(prog_switch));

	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(19), .switch_n8_Input_0_(reserved_net), .switch_n8_Input_1_(c_net0), .switch_n9_Input_0_(c_net2), .switch_n9_Input_1_(c_net3), .switch_n10_Input_0_(c_net4), .switch_n10_Input_1_(c_net5), .switch_n11_Input_0_(c_net6), .switch_n11_Input_1_(c_net7), .switch_n12_Input_0_(c_net8), .switch_n12_Input_1_(c_net9), .switch_n13_Input_0_(c_net10), .switch_n13_Input_1_(c_net11), .switch_n14_Input_0_(c_net12), .switch_n14_Input_1_(c_net13), .switch_n15_Input_0_(c_net14), .switch_n15_Input_1_(c_net15), .switch_n0_Input_0_(p_net3), .switch_n0_Input_1_(c_net80[0]), .switch_n1_Input_0_(c_net60[1]), .switch_n1_Input_1_(c_net61[1]), .switch_n2_Input_0_(c_net60[2]), .switch_n2_Input_1_(c_net61[2]), .switch_n3_Input_0_(c_net60[3]), .switch_n3_Input_1_(c_net61[3]), .switch_n4_Input_0_(c_net62[0]), .switch_n4_Input_1_(c_net63[0]), .switch_n5_Input_0_(c_net62[1]), .switch_n5_Input_1_(c_net63[1]), .switch_n6_Input_0_(c_net62[2]), .switch_n6_Input_1_(c_net63[2]), .switch_n7_Input_0_(c_net62[3]), .switch_n7_Input_1_(c_net63[3]), .switch_n0_Vsel_0_(c_net64[0]), .switch_n0_Vsel_1_(c_net65[0]), .switch_n1_Vsel_0_(c_net64[1]), .switch_n1_Vsel_1_(c_net65[1]), .switch_n2_Vsel_0_(c_net64[2]), .switch_n2_Vsel_1_(c_net65[2]), .switch_n3_Vsel_0_(c_net64[3]), .switch_n3_Vsel_1_(c_net65[3]), .switch_n4_Vsel_0_(c_net64[4]), .switch_n4_Vsel_1_(c_net65[4]), .switch_n5_Vsel_0_(c_net64[5]), .switch_n5_Vsel_1_(c_net65[5]), .switch_n6_Vsel_0_(c_net64[6]), .switch_n6_Vsel_1_(c_net65[6]), .switch_n7_Vsel_0_(c_net66[0]), .switch_n7_Vsel_1_(c_net67[0]), .switch_n8_Vsel_0_(c_net66a[0]), .switch_n8_Vsel_1_(c_net67a[0]), .switch_n9_Vsel_0_(c_net66b[0]), .switch_n9_Vsel_1_(c_net67b[0]), .switch_n10_Vsel_0_(c_net62[0]), .switch_n10_Vsel_1_(c_net63[0]), .switch_n11_Vsel_0_(c_net62[1]), .switch_n11_Vsel_1_(c_net63[1]), .switch_n12_Vsel_0_(c_net62[2]), .switch_n12_Vsel_1_(c_net63[2]), .switch_n13_Vsel_0_(c_net62[3]), .switch_n13_Vsel_1_(c_net63[3]), .switch_n14_Vsel_0_(c_net62[4]), .switch_n14_Vsel_1_(c_net63[4]), .switch_n15_Vsel_0_(c_net62[5]), .switch_n15_Vsel_1_(c_net63[5]), .switch_n16_Vsel_0_(c_net68[6]), .switch_n16_Vsel_1_(c_net69[6]), .switch_n0_Vg_global_0_(c_net70[0]), .switch_n0_Vg_global_1_(c_net71[0]), .switch_n0_VTUN(c_net72[0]), .switch_n1_Vg_global_0_(c_net70[1]), .switch_n1_Vg_global_1_(c_net71[1]), .switch_n1_VTUN(c_net72[1]), .switch_n2_Vg_global_0_(c_net70[2]), .switch_n2_Vg_global_1_(c_net71[2]), .switch_n2_VTUN(c_net72[2]), .switch_n3_Vg_global_0_(c_net70[3]), .switch_n3_Vg_global_1_(c_net71[3]), .switch_n3_VTUN(c_net72[3]), .switch_n4_Vg_global_0_(c_net70[4]), .switch_n4_Vg_global_1_(c_net71[4]), .switch_n4_VTUN(c_net72[4]), .switch_n5_Vg_global_0_(c_net70[5]), .switch_n5_Vg_global_1_(c_net71[5]), .switch_n5_VTUN(c_net72[5]), .switch_n6_Vg_global_0_(c_net70[6]), .switch_n6_Vg_global_1_(c_net71[6]), .switch_n6_VTUN(c_net72[6]), .switch_n7_Vg_global_0_(c_net73[0]), .switch_n7_Vg_global_1_(c_net74[0]), .switch_n7_VTUN(c_net75[0]), .switch_n8_Vg_global_0_(c_net73a[0]), .switch_n8_Vg_global_1_(c_net74a[0]), .switch_n8_VTUN(c_net75a[0]), .switch_n9_Vg_global_0_(c_net73b[0]), .switch_n9_Vg_global_1_(c_net74b[0]), .switch_n9_VTUN(c_net75b[0]), .switch_n10_Vg_global_0_(c_net76[0]), .switch_n10_Vg_global_1_(c_net77[0]), .switch_n10_VTUN(c_net78[0]), .switch_n11_Vg_global_0_(c_net76[1]), .switch_n11_Vg_global_1_(c_net77[1]), .switch_n11_VTUN(c_net78[1]), .switch_n12_Vg_global_0_(c_net76[2]), .switch_n12_Vg_global_1_(c_net77[2]), .switch_n12_VTUN(c_net78[2]), .switch_n13_Vg_global_0_(c_net76[3]), .switch_n13_Vg_global_1_(c_net77[3]), .switch_n13_VTUN(c_net78[3]), .switch_n14_Vg_global_0_(c_net76[4]), .switch_n14_Vg_global_1_(c_net77[4]), .switch_n14_VTUN(c_net78[4]), .switch_n15_Vg_global_0_(c_net76[5]), .switch_n15_Vg_global_1_(c_net77[5]), .switch_n15_VTUN(c_net78[5]), .switch_n16_Vg_global_0_(c_net76[6]), .switch_n16_Vg_global_1_(c_net77[6]), .switch_n16_VTUN(c_net78[6]), .switch_n0_VINJ(c_net79[0]), .switch_n0_GND(c_net80[0]), .switch_n1_VINJ(c_net79[1]), .switch_n1_GND(c_net80[1]), .switch_n2_VINJ(c_net79[2]), .switch_n2_GND(c_net80[2]), .switch_n3_VINJ(c_net79[3]), .switch_n3_GND(c_net80[3]), .switch_n4_VINJ(c_net79[4]), .switch_n4_GND(c_net80[4]), .switch_n5_VINJ(c_net79[5]), .switch_n5_GND(c_net80[5]), .switch_n6_VINJ(c_net79[6]), .switch_n6_GND(c_net80[6]), .switch_n7_VINJ(c_net81[0]), .switch_n7_GND(c_net82[0]), .switch_n8_VINJ(c_net81a[0]), .switch_n8_GND(c_net82a[0]), .switch_n9_VINJ(c_net81b[0]), .switch_n9_GND(c_net82b[0]), .switch_n10_VINJ(c_net83[0]), .switch_n10_GND(c_net84[0]), .switch_n11_VINJ(c_net83[1]), .switch_n11_GND(c_net84[1]), .switch_n12_VINJ(c_net83[2]), .switch_n12_GND(c_net84[2]), .switch_n13_VINJ(c_net83[3]), .switch_n13_GND(c_net84[3]), .switch_n14_VINJ(c_net83[4]), .switch_n14_GND(c_net84[4]), .switch_n15_VINJ(c_net83[5]), .switch_n15_GND(c_net84[5]), .switch_n16_VINJ(c_net83[6]), .switch_n16_GND(c_net84[6]));
	none switch_ind (.island_num(1), .direction(horizontal), .col(17));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(18), .CTRL_B_0_(c_net26), .Vg_0_(c_net27), .VTUN(c_net28), .Vg_1_(c_net29), .CTRL_B_1_(c_net30), .VINJ(c_net31), .GND_0_(c_net32), .VDD_1_(c_net33), .VPWR_1_(p_net3), .decode_0_(c_net68[7]), .decode_1_(c_net69[7]), .VTUN_T(c_net78[7]));

	/*
	- Generate a frame with cab_frame instance name 
	- Specify frame edge with first letter in name
	- Specify a default pin layer and optionally modify individual pins with _metal#_ eg N_metal2_name()
	- Specify the pin name last and pass in the net */
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_gateEN(f_net1), .S_s_gateEN(f_net1), .N_n_gatebit5(f_net2), .N_n_gatebit4(f_net3), .N_n_gatebit3(f_net4), .N_n_gatebit2(f_net5), .N_n_gatebit1(f_net6), .N_n_gatebit0(f_net7), .S_s_gatebit5(f_net2), .S_s_gatebit4(f_net3), .S_s_gatebit3(f_net4), .S_s_gatebit2(f_net5), .S_s_gatebit1(f_net6), .S_s_gatebit0(f_net7), .N_n_progdrain(f_net8), .S_s_progdrain(f_net8), .N_n_rundrain(f_net9), .S_s_rundrain(f_net9), .N_n_cew0(f_net52), .S_s_cew0(f_net30[0]), .N_n_cew1(f_net53), .S_s_cew1(f_net31[0]), .N_n_cew2(f_net54), .S_s_cew2(f_net32[0]), .N_n_cew3(f_net55), .S_s_cew3(f_net56[0]), .N_n_vtun(p_net0), .S_s_vtun(p_net0), .N_n_vinj(p_net1), .S_s_vinj(p_net1), .N_n_gnd(p_net2), .S_s_gnd(p_net2), .N_n_avdd(p_net3), .S_s_avdd(p_net3), .W_w_cns0(f_net30[1]), .E_e_cns0(f_net48), .W_w_cns1(f_net31[1]), .E_e_cns1(f_net49), .W_w_cns2(f_net32[1]), .E_e_cns2(f_net50), .W_w_cns3(f_net56[1]), .E_e_cns3(f_net51), .N_n_s0(f_net10), .S_s_s0(f_net10b), .N_n_s1(f_net11), .S_s_s1(f_net11b), .N_n_s2(f_net12), .S_s_s2(f_net12b), .N_n_s3(f_net13), .S_s_s3(f_net13b), .N_n_s4(f_net14), .S_s_s4(f_net14b), .N_n_s5(f_net15), .S_s_s5(f_net15b), .N_n_s6(f_net16), .S_s_s6(f_net16b), .N_n_s7(f_net17), .S_s_s7(f_net17b), .N_n_s8(f_net18), .S_s_s8(f_net18b), .N_n_s9(f_net19), .S_s_s9(f_net19b), .N_n_s10(f_net20), .S_s_s10(f_net20b), .N_n_s11(f_net21), .S_s_s11(f_net21b), .N_n_s12(f_net22), .S_s_s12(f_net22b), .N_n_s13(f_net23), .S_s_s13(f_net23b), .N_n_s14(f_net24), .S_s_s14(f_net24b), .N_n_s15(f_net25), .S_s_s15(f_net25b), .N_n_s16(f_net26), .S_s_s16(f_net26b), .N_n_s17(f_net27), .S_s_s17(f_net27b), .N_n_s18(f_net28), .S_s_s18(f_net28b), .N_n_s19(f_net29), .S_s_s19(f_net29b), .W_w_vtun(p_net0), .E_e_vtun(p_net0), .W_w_vinj(p_net1), .E_e_vinj(p_net1), .W_w_gnd(p_net2), .E_e_gnd(p_net2), .W_w_avdd(p_net3), .E_e_avdd(p_net3), .W_w_drainbit4(f_net33), .E_e_drainbit4(f_net33), .W_w_drainbit3(f_net34), .E_e_drainbit3(f_net34), .W_w_drainbit2(f_net35), .E_e_drainbit2(f_net35), .W_w_drainbit1(f_net36), .E_e_drainbit1(f_net36), .W_w_drainbit0(f_net37), .E_e_drainbit0(f_net37), .W_w_s0(f_net57[0]), .E_e_s0(f_net38[0]), .W_w_s1(f_net58[0]), .E_e_s1(f_net39[0]), .W_w_s2(f_net59[0]), .E_e_s2(f_net40[0]), .W_w_s3(f_net60[0]), .E_e_s3(f_net41[0]), .W_w_s4(f_net57[1]), .E_e_s4(f_net38[1]), .W_w_s5(f_net58[1]), .E_e_s5(f_net39[1]), .W_w_s6(f_net59[1]), .E_e_s6(f_net40[1]), .W_w_s7(f_net60[1]), .E_e_s7(f_net41[1]), .W_w_s8(f_net57[2]), .E_e_s8(f_net38[2]), .W_w_s9(f_net58[2]), .E_e_s9(f_net39[2]), .W_w_s10(f_net59[2]), .E_e_s10(f_net40[2]), .W_w_s11(f_net60[2]), .E_e_s11(f_net41[2]), .W_w_s12(f_net57[3]), .E_e_s12(f_net38[3]), .W_w_s13(f_net58[3]), .E_e_s13(f_net39[3]), .W_w_s14(f_net59[3]), .E_e_s14(f_net40[3]), .W_w_s15(f_net60[3]), .E_e_s15(f_net41[3]), .W_w_s16(f_net57[4]), .E_e_s16(f_net38[4]), .W_w_s17(f_net58[4]), .E_e_s17(f_net39[4]), .W_w_s18(f_net59[4]), .E_e_s18(f_net40[4]), .W_w_s19(f_net60[4]), .E_e_s19(f_net41[4]), .W_w_drainbit10(f_net42), .E_e_drainbit10(f_net42), .W_w_drainbit9(f_net43), .E_e_drainbit9(f_net43), .W_w_drainbit8(f_net44), .E_e_drainbit8(f_net44), .W_w_drainbit7(f_net45), .E_e_drainbit7(f_net45), .W_w_drainbit6(f_net46), .E_e_drainbit6(f_net46), .W_w_drainbit5(f_net47), .E_e_drainbit5(f_net47));

endmodule

module Tile_v11(port1);
	/*Tile Verilog*/
	/* C, S, C blocks of the tile */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(6), .Vs_b_0_row_4(c_net60[0:6]), .Vs_b_1_row_4(c_net61[0:6]), .Vsel_b_0_row_4(c_net64[0:6]), .Vsel_b_1_row_4(c_net65[0:6]), .Vg_b_0_row_4(c_net70[0:6]), .Vg_b_1_row_4(c_net71[0:6]), .VTUN_brow_4(c_net72[0:6]), .VINJ_b_1_row_4(c_net79[0:6]), .GND_b_1_row_4(c_net80[0:6]));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(6), .matrix_row(5), .matrix_col(10), .Vsel_b_0_row_4(c_net66[0:10]), .Vsel_b_1_row_4(c_net67[0:10]), .Vg_b_0_row_4(c_net73[0:10]), .Vg_b_1_row_4(c_net74[0:10]), .VTUN_brow_4(c_net75[0:10]), .VINJ_b_1_row_4(c_net81[0:10]), .GND_b_1_row_4(c_net82[0:10]));
	TSMC350nm_4x2_Indirect I__2 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(6), .Vs_b_0_row_4(c_net62[0:6]), .Vs_b_1_row_4(c_net63[0:6]), .Vsel_b_0_row_4(c_net68[0:6]), .Vsel_b_1_row_4(c_net69[0:6]), .Vg_b_0_row_4(c_net76[0:5]), .Vg_b_1_row_4(c_net77[0:5]), .VTUN_brow_4(c_net78[0:6]), .VINJ_b_1_row_4(c_net83[0:5]), .GND_b_1_row_4(c_net84[0:5]), .Vd_R_0_col_5(f_net38[0:5]), .Vd_R_1_col_5(f_net39[0:5]), .Vd_R_2_col_5(f_net40[0:5]), .Vd_R_3_col_5(f_net41[0:5]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5), .decode_n0_IN_0_(f_net33), .decode_n2_IN_0_(f_net34), .decode_n2_IN_1_(f_net35), .decode_n4_IN_0_(f_net36), .decode_n4_IN_1_(f_net37));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select), .switch_n0_prog_drainrail(f_net8), .switch_n0_run_drainrail(f_net9));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));

	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6), .decode_n0_ENABLE(f_net1), .decode_n0_n0_IN_0_(f_net2), .decode_n0_n0_IN_1_(f_net3), .decode_n2_n0_IN_0_(f_net4), .decode_n2_n0_IN_1_(f_net5), .decode_n4_n0_IN_0_(f_net6), .decode_n4_n0_IN_1_(f_net7), .decode_n0_VINJV(p_net1) , .decode_n0_GNDV(p_net2), .decode_n3_VGRUN_0_(f_net10), .decode_n3_VGRUN_1_(f_net11), .decode_n3_VGRUN_2_(f_net12), .decode_n3_VGRUN_3_(f_net13), .decode_n4_VGRUN_0_(f_net14), .decode_n4_VGRUN_1_(f_net15), .decode_n4_VGRUN_2_(f_net16), .decode_n4_VGRUN_3_(f_net17), .decode_n5_VGRUN_0_(f_net18), .decode_n5_VGRUN_1_(f_net19), .decode_n5_VGRUN_2_(f_net20), .decode_n5_VGRUN_3_(f_net21), .decode_n6_VGRUN_0_(f_net22), .decode_n6_VGRUN_1_(f_net23), .decode_n6_VGRUN_2_(f_net24), .decode_n6_VGRUN_3_(f_net25), .decode_n7_VGRUN_0_(f_net26), .decode_n7_VGRUN_1_(f_net27), .decode_n7_VGRUN_2_(f_net28), .decode_n7_VGRUN_3_(f_net29), .decode_n10_VGRUN_0_(f_net48), .decode_n10_VGRUN_1_(f_net49), .decode_n10_VGRUN_2_(f_net50), .decode_n10_VGRUN_3_(f_net51), .decode_n2_VGRUN_0_(f_net52), .decode_n2_VGRUN_1_(f_net53), .decode_n2_VGRUN_2_(f_net54), .decode_n2_VGRUN_3_(f_net55));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(22), .switch_n0_VTUN_T(p_net0));

	/* CAB elements of tile*/
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__6 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(1), .col(0), .matrix_row(7), .matrix_col(8), .VTUN_brow_8(fake_net0[0:8]));
	TSMC350nm_4x2_Indirect I__4 (.island_num(1), .row(0), .col(8), .matrix_row(8), .matrix_col(9), .Vd_P_0_col_8(c_net18[0:8]), .Vd_P_1_col_8(c_net19[0:8]), .Vd_P_2_col_8(c_net20[0:8]), .Vd_P_3_col_8(c_net21[0:8]), .Vd_R_0_col_8(c_net22[0:8]), .Vd_R_1_col_8(c_net23[0:8]), .Vd_R_2_col_8(c_net24[0:8]), .Vd_R_3_col_8(c_net25[0:8]));
	TSMC350nm_OutMtrx_IndrctSwcs I__7 (.island_num(1), .row(9), .col(8), .matrix_row(1), .matrix_col(9));
	TSMC350nm_4x2_Indirect I__5 (.island_num(1), .row(10), .col(8), .matrix_row(2), .matrix_col(9), .Vd_R_0_col_8(f_net30[0:2]), .Vd_R_1_col_8(f_net31[0:2]), .Vd_R_2_col_8(f_net32[0:2]), .Vd_R_3_col_8(f_net56[0:2]));
	TSMC350nm_TA2Cell_Strong cab_device_0 (.island_num(1), .row(2), .col(17), .OUTPUT1(c_net0), .OUTPUT2(c_net1), .DRAIN1(c_net18[0]), .DRAIN2(c_net21[0]), .VIN1_PLUS(c_net22[0]), .VIN1_MINUS(c_net23[0]), .VIN2_PLUS(c_net24[0]), .VIN2_MINUS(c_net25[0]), .COLSEL2(c_net26), .GATE2(c_net27), .VTUN(c_net28), .GATE1(c_net29), .COLSEL1(c_net30), .VINJ(c_net31), .GND(c_net32), .VPWR(c_net33), .COLSEL2_b(c_net34), .RUN_b(c_net35), .GATE2_b(c_net36), .PROG_b(c_net37), .VTUN_b(c_net38), .GATE1_b(c_net39), .COLSEL1_b(c_net40), .VINJ_b(c_net41), .GND_b(c_net42), .VPWR_b(c_net43));
	TSMC350nm_TA2Cell_LongL_Cab cab_device_1 (.island_num(1), .row(3), .col(17), .OUTPUT1(c_net2), .OUTPUT2(c_net3), .DRAIN1(c_net18[1]), .DRAIN2(c_net21[1]), .VIN1_PLUS(c_net22[1]), .VIN1_MINUS(c_net23[1]), .VIN2_PLUS(c_net24[1]), .VIN2_MINUS(c_net25[1]), .COLSEL2(c_net34), .RUN(c_net35), .GATE2(c_net36), .PROG(c_net37), .VTUN(c_net38), .GATE1(c_net39), .COLSEL1(c_net40), .VINJ(c_net41), .GND(c_net42), .VPWR(c_net43), .COLSEL2_b(c_net44), .RUN_b(c_net45), .GATE2_b(c_net46), .PROG_b(c_net47), .VTUN_b(c_net48), .GATE1_b(c_net49), .COLSEL1_b(c_net50), .VINJ_b(c_net51), .GND_b(c_net52), .VPWR_b(c_net53));
	TSMC350nm_TA2Cell_Weak cab_device_2 (.island_num(1), .row(4), .col(17), .OUTPUT1(c_net4), .OUTPUT2(c_net5), .DRAIN1(c_net18[2]), .DRAIN2(c_net21[2]), .VIN1_PLUS(c_net22[2]), .VIN1_MINUS(c_net23[2]), .VIN2_PLUS(c_net24[2]), .VIN2_MINUS(c_net25[2]), .COLSEL2(c_net44), .RUN(c_net45), .GATE2(c_net46), .PROG(c_net47), .VTUN(c_net48), .GATE1(c_net49), .COLSEL1(c_net50), .VINJ(c_net51), .GND(c_net52), .VPWR(c_net53), .VTUN_b(c_net54), .GATE1_b(c_net55), .COLSEL1_b(c_net56), .VINJ_b(c_net57), .GND_b(c_net58), .VPWR_b(c_net59));
	TSMC350nm_TA2Cell_NoFG cab_device_3 (.island_num(1), .row(5), .col(17), .OUTPUT1(c_net6), .OUTPUT2(c_net7), .DRAIN1(c_net18[3]), .DRAIN2(c_net21[3]), .VIN1_PLUS(c_net22[3]), .VIN1_MINUS(c_net23[3]), .VIN2_PLUS(c_net24[3]), .VIN2_MINUS(c_net25[3]), .VTUN(c_net54), .GATE1(c_net55), .COLSEL1(c_net56), .VINJ(c_net57), .GND(c_net58), .VPWR(c_net59));
	TSMC350nm_4WTA_IndirectProg cab_device_4 (.island_num(1), .row(6), .col(17), .Vout_0_(c_net8), .Vout_1_(c_net9), .Vout_2_(c_net10), .Vout_3_(c_net11), .Vmid(c_net12), .vbias(c_net13), .Iin_0_(c_net22[4]), .Iin_1_(c_net23[4]), .Iin_2_(c_net24[4]), .Iin_3_(c_net25[4]), .Vd_P_0_(c_net18[4]), .Vd_P_1_(c_net19[4]), .Vd_P_2_(c_net20[4]), .Vd_P_3_(c_net21[4]));
	TSMC350nm_Cap_Bank cab_device_5 (.island_num(1), .row(7), .col(17), .OUT_0_(c_net14), .OUT_1_(c_net15), .VD_P_0_(c_net18[5]), .VD_P_1_(c_net19[5]), .VD_P_2_(c_net20[5]), .VD_P_3_(c_net21[5]), .VIN_0_(c_net22[5]), .VIN_1_(c_net23[5]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6), .decode_n0_IN_0_(f_net42), .decode_n0_IN_1_(f_net43), .decode_n2_IN_0_(f_net44), .decode_n2_IN_1_(f_net45), .decode_n4_IN_0_(f_net46), .decode_n4_IN_1_(f_net47));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(1), .direction(vertical), .num(12), .type(drain_select), .switch_n0_prog_drainrail(f_net8), .switch_n0_run_drainrail(f_net9));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(1), .direction(vertical), .num(12), .type(prog_switch));

	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(18), .switch_n8_Input_0_(c_net0), .switch_n8_Input_1_(c_net1), .switch_n9_Input_0_(c_net2), .switch_n9_Input_1_(c_net3), .switch_n10_Input_0_(c_net4), .switch_n10_Input_1_(c_net5), .switch_n11_Input_0_(c_net6), .switch_n11_Input_1_(c_net7), .switch_n12_Input_0_(c_net8), .switch_n12_Input_1_(c_net9), .switch_n13_Input_0_(c_net10), .switch_n13_Input_1_(c_net11), .switch_n14_Input_0_(c_net12), .switch_n14_Input_1_(c_net13), .switch_n15_Input_0_(c_net14), .switch_n15_Input_1_(c_net15), .switch_n0_Input_0_(c_net60[0]), .switch_n0_Input_1_(c_net61[0]), .switch_n1_Input_0_(c_net60[1]), .switch_n1_Input_1_(c_net61[1]), .switch_n2_Input_0_(c_net60[2]), .switch_n2_Input_1_(c_net61[2]), .switch_n3_Input_0_(c_net60[3]), .switch_n3_Input_1_(c_net61[3]), .switch_n4_Input_0_(c_net62[0]), .switch_n4_Input_1_(c_net63[0]), .switch_n5_Input_0_(c_net62[1]), .switch_n5_Input_1_(c_net63[1]), .switch_n6_Input_0_(c_net62[2]), .switch_n6_Input_1_(c_net63[2]), .switch_n7_Input_0_(c_net62[3]), .switch_n7_Input_1_(c_net63[3]), .switch_n0_Vsel_0_(c_net64[0]), .switch_n0_Vsel_1_(c_net65[0]), .switch_n1_Vsel_0_(c_net64[1]), .switch_n1_Vsel_1_(c_net65[1]), .switch_n2_Vsel_0_(c_net64[2]), .switch_n2_Vsel_1_(c_net65[2]), .switch_n3_Vsel_0_(c_net64[3]), .switch_n3_Vsel_1_(c_net65[3]), .switch_n4_Vsel_0_(c_net64[4]), .switch_n4_Vsel_1_(c_net65[4]), .switch_n5_Vsel_0_(c_net64[5]), .switch_n5_Vsel_1_(c_net65[5]), .switch_n6_Vsel_0_(c_net66[0]), .switch_n6_Vsel_1_(c_net67[0]), .switch_n7_Vsel_0_(c_net66[1]), .switch_n7_Vsel_1_(c_net67[1]), .switch_n8_Vsel_0_(c_net66[2]), .switch_n8_Vsel_1_(c_net67[2]), .switch_n9_Vsel_0_(c_net66[3]), .switch_n9_Vsel_1_(c_net67[3]), .switch_n10_Vsel_0_(c_net66[4]), .switch_n10_Vsel_1_(c_net67[4]), .switch_n11_Vsel_0_(c_net66[5]), .switch_n11_Vsel_1_(c_net67[5]), .switch_n12_Vsel_0_(c_net66[6]), .switch_n12_Vsel_1_(c_net67[6]), .switch_n13_Vsel_0_(c_net66[7]), .switch_n13_Vsel_1_(c_net67[7]), .switch_n14_Vsel_0_(c_net66[8]), .switch_n14_Vsel_1_(c_net67[8]), .switch_n15_Vsel_0_(c_net66[9]), .switch_n15_Vsel_1_(c_net67[9]), .switch_n16_Vsel_0_(c_net68[0]), .switch_n16_Vsel_1_(c_net69[0]), .switch_n0_Vg_global_0_(c_net70[0]), .switch_n0_Vg_global_1_(c_net71[0]), .switch_n0_VTUN(c_net72[0]), .switch_n1_Vg_global_0_(c_net70[1]), .switch_n1_Vg_global_1_(c_net71[1]), .switch_n1_VTUN(c_net72[1]), .switch_n2_Vg_global_0_(c_net70[2]), .switch_n2_Vg_global_1_(c_net71[2]), .switch_n2_VTUN(c_net72[2]), .switch_n3_Vg_global_0_(c_net70[3]), .switch_n3_Vg_global_1_(c_net71[3]), .switch_n3_VTUN(c_net72[3]), .switch_n4_Vg_global_0_(c_net70[4]), .switch_n4_Vg_global_1_(c_net71[4]), .switch_n4_VTUN(c_net72[4]), .switch_n5_Vg_global_0_(c_net70[5]), .switch_n5_Vg_global_1_(c_net71[5]), .switch_n5_VTUN(c_net72[5]), .switch_n6_Vg_global_0_(c_net73[0]), .switch_n6_Vg_global_1_(c_net74[0]), .switch_n6_VTUN(c_net75[0]), .switch_n7_Vg_global_0_(c_net73[1]), .switch_n7_Vg_global_1_(c_net74[1]), .switch_n7_VTUN(c_net75[1]), .switch_n8_Vg_global_0_(c_net73[2]), .switch_n8_Vg_global_1_(c_net74[2]), .switch_n8_VTUN(c_net75[2]), .switch_n9_Vg_global_0_(c_net73[3]), .switch_n9_Vg_global_1_(c_net74[3]), .switch_n9_VTUN(c_net75[3]), .switch_n10_Vg_global_0_(c_net73[4]), .switch_n10_Vg_global_1_(c_net74[4]), .switch_n10_VTUN(c_net75[4]), .switch_n11_Vg_global_0_(c_net73[5]), .switch_n11_Vg_global_1_(c_net74[5]), .switch_n11_VTUN(c_net75[5]), .switch_n12_Vg_global_0_(c_net73[6]), .switch_n12_Vg_global_1_(c_net74[6]), .switch_n12_VTUN(c_net75[6]), .switch_n13_Vg_global_0_(c_net73[7]), .switch_n13_Vg_global_1_(c_net74[7]), .switch_n13_VTUN(c_net75[7]), .switch_n14_Vg_global_0_(c_net73[8]), .switch_n14_Vg_global_1_(c_net74[8]), .switch_n14_VTUN(c_net75[8]), .switch_n15_Vg_global_0_(c_net73[9]), .switch_n15_Vg_global_1_(c_net74[9]), .switch_n15_VTUN(c_net75[9]), .switch_n16_Vg_global_0_(c_net76[0]), .switch_n16_Vg_global_1_(c_net77[0]), .switch_n16_VTUN(c_net78[0]), .switch_n0_VINJ(c_net79[0]), .switch_n0_GND(c_net80[0]), .switch_n1_VINJ(c_net79[1]), .switch_n1_GND(c_net80[1]), .switch_n2_VINJ(c_net79[2]), .switch_n2_GND(c_net80[2]), .switch_n3_VINJ(c_net79[3]), .switch_n3_GND(c_net80[3]), .switch_n4_VINJ(c_net79[4]), .switch_n4_GND(c_net80[4]), .switch_n5_VINJ(c_net79[5]), .switch_n5_GND(c_net80[5]), .switch_n6_VINJ(c_net81[0]), .switch_n6_GND(c_net82[0]), .switch_n7_VINJ(c_net81[1]), .switch_n7_GND(c_net82[1]), .switch_n8_VINJ(c_net81[2]), .switch_n8_GND(c_net82[2]), .switch_n9_VINJ(c_net81[3]), .switch_n9_GND(c_net82[3]), .switch_n10_VINJ(c_net81[4]), .switch_n10_GND(c_net82[4]), .switch_n11_VINJ(c_net81[5]), .switch_n11_GND(c_net82[5]), .switch_n12_VINJ(c_net81[6]), .switch_n12_GND(c_net82[6]), .switch_n13_VINJ(c_net81[7]), .switch_n13_GND(c_net82[7]), .switch_n14_VINJ(c_net81[8]), .switch_n14_GND(c_net82[8]), .switch_n15_VINJ(c_net81[9]), .switch_n15_GND(c_net82[9]), .switch_n16_VINJ(c_net83[0]), .switch_n16_GND(c_net84[0]));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(17), .CTRL_B_0_(c_net26), .Vg_0_(c_net27), .VTUN(c_net28), .Vg_1_(c_net29), .CTRL_B_1_(c_net30), .VINJ(c_net31), .GND_0_(c_net32), .VDD_1_(c_net33), .VPWR_1_(p_net3), .decode_0_(c_net68[2]), .decode_1_(c_net69[2]), .VTUN_T(c_net78[2]));

	/*
	- Generate a frame with cab_frame instance name 
	- Specify frame edge with first letter in name
	- Specify a default pin layer and optionally modify individual pins with _metal#_ eg N_metal2_name()
	- Specify the pin name last and pass in the net */
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_gateEN(f_net1), .S_s_gateEN(f_net1), .N_n_gatebit5(f_net2), .N_n_gatebit4(f_net3), .N_n_gatebit3(f_net4), .N_n_gatebit2(f_net5), .N_n_gatebit1(f_net6), .N_n_gatebit0(f_net7), .S_s_gatebit5(f_net2), .S_s_gatebit4(f_net3), .S_s_gatebit3(f_net4), .S_s_gatebit2(f_net5), .S_s_gatebit1(f_net6), .S_s_gatebit0(f_net7), .N_n_progdrain(f_net8), .S_s_progdrain(f_net8), .N_n_rundrain(f_net9), .S_s_rundrain(f_net9), .N_n_cew0(f_net52), .S_s_cew0(f_net30[0]), .N_n_cew1(f_net53), .S_s_cew1(f_net31[0]), .N_n_cew2(f_net54), .S_s_cew2(f_net32[0]), .N_n_cew3(f_net55), .S_s_cew3(f_net56[0]), .N_n_vtun(p_net0), .S_s_vtun(p_net0), .N_n_vinj(p_net1), .S_s_vinj(p_net1), .N_n_gnd(p_net2), .S_s_gnd(p_net2), .N_n_avdd(p_net3), .S_s_avdd(p_net3), .W_w_cns0(f_net30[1]), .E_e_cns0(f_net48), .W_w_cns1(f_net31[1]), .E_e_cns1(f_net49), .W_w_cns2(f_net32[1]), .E_e_cns2(f_net50), .W_w_cns3(f_net56[1]), .E_e_cns3(f_net51), .N_n_s0(f_net10), .S_s_s0(f_net10), .N_n_s1(f_net11), .S_s_s1(f_net11), .N_n_s2(f_net12), .S_s_s2(f_net12), .N_n_s3(f_net13), .S_s_s3(f_net13), .N_n_s4(f_net14), .S_s_s4(f_net14), .N_n_s5(f_net15), .S_s_s5(f_net15), .N_n_s6(f_net16), .S_s_s6(f_net16), .N_n_s7(f_net17), .S_s_s7(f_net17), .N_n_s8(f_net18), .S_s_s8(f_net18), .N_n_s9(f_net19), .S_s_s9(f_net19), .N_n_s10(f_net20), .S_s_s10(f_net20), .N_n_s11(f_net21), .S_s_s11(f_net21), .N_n_s12(f_net22), .S_s_s12(f_net22), .N_n_s13(f_net23), .S_s_s13(f_net23), .N_n_s14(f_net24), .S_s_s14(f_net24), .N_n_s15(f_net25), .S_s_s15(f_net25), .N_n_s16(f_net26), .S_s_s16(f_net26), .N_n_s17(f_net27), .S_s_s17(f_net27), .N_n_s18(f_net28), .S_s_s18(f_net28), .N_n_s19(f_net29), .S_s_s19(f_net29), .W_w_vtun(p_net0), .E_e_vtun(p_net0), .W_w_vinj(p_net1), .E_e_vinj(p_net1), .W_w_gnd(p_net2), .E_e_gnd(p_net2), .W_w_avdd(p_net3), .E_e_avdd(p_net3), .W_w_drainbit4(f_net33), .E_e_drainbit4(f_net33), .W_w_drainbit3(f_net34), .E_e_drainbit3(f_net34), .W_w_drainbit2(f_net35), .E_e_drainbit2(f_net35), .W_w_drainbit1(f_net36), .E_e_drainbit1(f_net36), .W_w_drainbit0(f_net37), .E_e_drainbit0(f_net37), .W_w_s0(f_net38[0]), .E_e_s0(f_net38[0]), .W_w_s1(f_net39[0]), .E_e_s1(f_net39[0]), .W_w_s2(f_net40[0]), .E_e_s2(f_net40[0]), .W_w_s3(f_net41[0]), .E_e_s3(f_net41[0]), .W_w_s4(f_net38[1]), .E_e_s4(f_net38[1]), .W_w_s5(f_net39[1]), .E_e_s5(f_net39[1]), .W_w_s6(f_net40[1]), .E_e_s6(f_net40[1]), .W_w_s7(f_net41[1]), .E_e_s7(f_net41[1]), .W_w_s8(f_net38[2]), .E_e_s8(f_net38[2]), .W_w_s9(f_net39[2]), .E_e_s9(f_net39[2]), .W_w_s10(f_net40[2]), .E_e_s10(f_net40[2]), .W_w_s11(f_net41[2]), .E_e_s11(f_net41[2]), .W_w_s12(f_net38[3]), .E_e_s12(f_net38[3]), .W_w_s13(f_net39[3]), .E_e_s13(f_net39[3]), .W_w_s14(f_net40[3]), .E_e_s14(f_net40[3]), .W_w_s15(f_net41[3]), .E_e_s15(f_net41[3]), .W_w_s16(f_net38[4]), .E_e_s16(f_net38[4]), .W_w_s17(f_net39[4]), .E_e_s17(f_net39[4]), .W_w_s18(f_net40[4]), .E_e_s18(f_net40[4]), .W_w_s19(f_net41[4]), .E_e_s19(f_net41[4]), .W_w_drainbit10(f_net42), .E_e_drainbit10(f_net42), .W_w_drainbit9(f_net43), .E_e_drainbit9(f_net43), .W_w_drainbit8(f_net44), .E_e_drainbit8(f_net44), .W_w_drainbit7(f_net45), .E_e_drainbit7(f_net45), .W_w_drainbit6(f_net46), .E_e_drainbit6(f_net46), .W_w_drainbit5(f_net47), .E_e_drainbit5(f_net47));
endmodule

module Tile_v5(port1);
	/*Tile Verilog*/
	/* C, S, C blocks of the tile */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(6), .Vs_b_0_row_4(c_net60[0:4]), .Vs_b_1_row_4(c_net61[0:4]));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(6), .matrix_row(5), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__2 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(6), .Vs_b_0_row_4(c_net62[0:4]), .Vs_b_1_row_4(c_net63[0:4]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));

	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6), .decode_n0_ENABLE(a_net1), .decode_n0_VGRUN_0_(a_net2), .decode_n0_VGRUN_1_(a_net5), .decode_n10_VGRUN_3_(a_net3));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(22));

	/* CAB elements of tile*/
	TSMC350nm_4x2_Indirect I__2 (.island_num(1), .row(0), .col(0), .matrix_row(8), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(0), .col(8), .matrix_row(8), .matrix_col(9), .Vd_P_0_col_8(c_net18[0:8]), .Vd_P_1_col_8(c_net19[0:8]), .Vd_P_2_col_8(c_net20[0:8]), .Vd_P_3_col_8(c_net21[0:8]), .Vd_R_0_col_8(c_net22[0:8]), .Vd_R_1_col_8(c_net23[0:8]), .Vd_R_2_col_8(c_net24[0:8]), .Vd_R_3_col_8(c_net25[0:8]));
	TSMC350nm_4x2_Indirect I__4 (.island_num(1), .row(8), .col(8), .matrix_row(2), .matrix_col(9), .Vs_b_0_row_1(a_net4[0:8]));
	TSMC350nm_TA2Cell_Strong cab_device_0 (.island_num(1), .row(2), .col(17), .OUTPUT1(c_net0), .OUTPUT2(c_net1), .DRAIN1(c_net18[0]), .DRAIN2(c_net21[0]), .VIN1_PLUS(c_net22[0]), .VIN1_MINUS(c_net23[0]), .VIN2_PLUS(c_net24[0]), .VIN2_MINUS(c_net25[0]), .COLSEL2(c_net26), .GATE2(c_net27), .VTUN(c_net28), .GATE1(c_net29), .COLSEL1(c_net30), .VINJ(c_net31), .GND(c_net32), .VPWR(c_net33), .COLSEL2_b(c_net34), .RUN_b(c_net35), .GATE2_b(c_net36), .PROG_b(c_net37), .VTUN_b(c_net38), .GATE1_b(c_net39), .COLSEL1_b(c_net40), .VINJ_b(c_net41), .GND_b(c_net42), .VPWR_b(c_net43));
	TSMC350nm_TA2Cell_LongL_Cab cab_device_1 (.island_num(1), .row(3), .col(17), .OUTPUT1(c_net2), .OUTPUT2(c_net3), .DRAIN1(c_net18[1]), .DRAIN2(c_net21[1]), .VIN1_PLUS(c_net22[1]), .VIN1_MINUS(c_net23[1]), .VIN2_PLUS(c_net24[1]), .VIN2_MINUS(c_net25[1]), .COLSEL2(c_net34), .RUN(c_net35), .GATE2(c_net36), .PROG(c_net37), .VTUN(c_net38), .GATE1(c_net39), .COLSEL1(c_net40), .VINJ(c_net41), .GND(c_net42), .VPWR(c_net43), .COLSEL2_b(c_net44), .RUN_b(c_net45), .GATE2_b(c_net46), .PROG_b(c_net47), .VTUN_b(c_net48), .GATE1_b(c_net49), .COLSEL1_b(c_net50), .VINJ_b(c_net51), .GND_b(c_net52), .VPWR_b(c_net53));
	TSMC350nm_TA2Cell_Weak cab_device_2 (.island_num(1), .row(4), .col(17), .OUTPUT1(c_net4), .OUTPUT2(c_net5), .DRAIN1(c_net18[2]), .DRAIN2(c_net21[2]), .VIN1_PLUS(c_net22[2]), .VIN1_MINUS(c_net23[2]), .VIN2_PLUS(c_net24[2]), .VIN2_MINUS(c_net25[2]), .COLSEL2(c_net44), .RUN(c_net45), .GATE2(c_net46), .PROG(c_net47), .VTUN(c_net48), .GATE1(c_net49), .COLSEL1(c_net50), .VINJ(c_net51), .GND(c_net52), .VPWR(c_net53), .VTUN_b(c_net54), .GATE1_b(c_net55), .COLSEL1_b(c_net56), .VINJ_b(c_net57), .GND_b(c_net58), .VPWR_b(c_net59));
	TSMC350nm_TA2Cell_NoFG cab_device_3 (.island_num(1), .row(5), .col(17), .OUTPUT1(c_net6), .OUTPUT2(c_net7), .DRAIN1(c_net18[3]), .DRAIN2(c_net21[3]), .VIN1_PLUS(c_net22[3]), .VIN1_MINUS(c_net23[3]), .VIN2_PLUS(c_net24[3]), .VIN2_MINUS(c_net25[3]), .VTUN(c_net54), .GATE1(c_net55), .COLSEL1(c_net56), .VINJ(c_net57), .GND(c_net58), .VPWR(c_net59));
	TSMC350nm_4WTA cab_device_4 (.island_num(1), .row(6), .col(17), .Vout_0_(c_net8), .Vout_1_(c_net9), .Vout_2_(c_net10), .Vout_3_(c_net11), .Iin_0_(c_net18[4]), .Iin_1_(c_net19[4]), .Iin_2_(c_net20[4]), .Iin_3_(c_net21[4]));
	TSMC350nm_4WTA cab_device_5 (.island_num(1), .row(7), .col(17), .Vout_0_(c_net12), .Vout_1_(c_net13), .Vout_2_(c_net14), .Vout_3_(c_net15), .Iin_0_(c_net18[5]), .Iin_1_(c_net19[5]), .Iin_2_(c_net20[5]), .Iin_3_(c_net21[5]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(10), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(1), .direction(vertical), .num(10), .type(prog_switch));

	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(18), .switch_n8_Input_0_(c_net0), .switch_n8_Input_1_(c_net1), .switch_n9_Input_0_(c_net2), .switch_n9_Input_1_(c_net3), .switch_n10_Input_0_(c_net4), .switch_n10_Input_1_(c_net5), .switch_n11_Input_0_(c_net6), .switch_n11_Input_1_(c_net7), .switch_n12_Input_0_(c_net8), .switch_n12_Input_1_(c_net9), .switch_n13_Input_0_(c_net10), .switch_n13_Input_1_(c_net11), .switch_n14_Input_0_(c_net12), .switch_n14_Input_1_(c_net13), .switch_n15_Input_0_(c_net14), .switch_n15_Input_1_(c_net15), .switch_n0_Input_0_(c_net60[0]), .switch_n0_Input_1_(c_net61[0]), .switch_n1_Input_0_(c_net60[1]), .switch_n1_Input_1_(c_net61[1]), .switch_n2_Input_0_(c_net60[2]), .switch_n2_Input_1_(c_net61[2]), .switch_n3_Input_0_(c_net60[3]), .switch_n3_Input_1_(c_net61[3]), .switch_n4_Input_0_(c_net62[0]), .switch_n4_Input_1_(c_net63[0]), .switch_n5_Input_0_(c_net62[1]), .switch_n5_Input_1_(c_net63[1]), .switch_n6_Input_0_(c_net62[2]), .switch_n6_Input_1_(c_net63[2]), .switch_n7_Input_0_(c_net62[3]), .switch_n7_Input_1_(c_net63[3]));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(17), .CTRL_B_0_(c_net26), .Vg_0_(c_net27), .VTUN(c_net28), .Vg_1_(c_net29), .CTRL_B_1_(c_net30), .VINJ(c_net31), .GND_0_(c_net32), .VDD_1_(c_net33));

	/*
	- Generate a frame with cab_frame instance name 
	- Specify frame edge with first letter in name
	- Specify a default pin layer and optionally modify individual pins with _metal#_ eg _metal2_
	- Specify the pin name last and pass in the net
	*/
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_p1(a_net1), .N_p5(a_net5), .E_metal2_p2(a_net2), .W_p3(a_net3), .S_p4(a_net4[0]));

endmodule

module Tile_v4(port1);
	/*Tile Verilog*/
	/* C, S, C blocks of the tile */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(6));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(6), .matrix_row(5), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__2 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(6));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));

	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(22));

	/* CAB elements of tile*/
	TSMC350nm_4x2_Indirect I__2 (.island_num(1), .row(0), .col(0), .matrix_row(8), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(0), .col(8), .matrix_row(8), .matrix_col(9), .Vd_P_0_col_8(c_net18[0:8]), .Vd_P_1_col_8(c_net19[0:8]), .Vd_P_2_col_8(c_net20[0:8]), .Vd_P_3_col_8(c_net21[0:8]), .Vd_R_0_col_8(c_net22[0:8]), .Vd_R_1_col_8(c_net23[0:8]), .Vd_R_2_col_8(c_net24[0:8]), .Vd_R_3_col_8(c_net25[0:8]));
	TSMC350nm_4x2_Indirect I__4 (.island_num(1), .row(8), .col(8), .matrix_row(2), .matrix_col(9));
	TSMC350nm_4WTA cab_device_0 (.island_num(1), .row(2), .col(17), .Vout_0_(c_net0), .Vout_1_(c_net1), .Vout_2_(c_net2), .Vout_3_(c_net3), .Iin_0_(c_net18[0]), .Iin_1_(c_net19[0]), .Iin_2_(c_net20[0]), .Iin_3_(c_net21[0]));
	TSMC350nm_TA2Cell_NoFG cab_device_1 (.island_num(1), .row(3), .col(17), .OUTPUT1(c_net4), .OUTPUT2(c_net5), .DRAIN1(c_net18[1]), .DRAIN2(c_net21[1]), .VIN1_PLUS(c_net22[1]), .VIN1_MINUS(c_net23[1]), .VIN2_PLUS(c_net24[1]), .VIN2_MINUS(c_net25[1]));
	TSMC350nm_4WTA cab_device_2 (.island_num(1), .row(4), .col(17), .Vout_0_(c_net6), .Vout_1_(c_net7), .Vout_2_(c_net8), .Vout_3_(c_net9), .Iin_0_(c_net18[2]), .Iin_1_(c_net19[2]), .Iin_2_(c_net20[2]), .Iin_3_(c_net21[2]));
	TSMC350nm_TA2Cell_Weak cab_device_3 (.island_num(1), .row(5), .col(17), .OUTPUT1(c_net10), .OUTPUT2(c_net11), .DRAIN1(c_net18[3]), .DRAIN2(c_net21[3]), .VIN1_PLUS(c_net22[3]), .VIN1_MINUS(c_net23[3]), .VIN2_PLUS(c_net24[3]), .VIN2_MINUS(c_net25[3]));
	TSMC350nm_4WTA cab_device_4 (.island_num(1), .row(6), .col(17), .Vout_0_(c_net12), .Vout_1_(c_net13), .Vout_2_(c_net14), .Vout_3_(c_net15), .Iin_0_(c_net18[4]), .Iin_1_(c_net19[4]), .Iin_2_(c_net20[4]), .Iin_3_(c_net21[4]));
	TSMC350nm_TA2Cell_Weak cab_device_5 (.island_num(1), .row(7), .col(17), .OUTPUT1(c_net16), .OUTPUT2(c_net17), .DRAIN1(c_net18[5]), .DRAIN2(c_net21[5]), .VIN1_PLUS(c_net22[5]), .VIN1_MINUS(c_net23[5]), .VIN2_PLUS(c_net24[5]), .VIN2_MINUS(c_net25[5]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(10), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(1), .direction(vertical), .num(10), .type(prog_switch));

	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(18), .switch_n8_Input_0_(c_net0), .switch_n8_Input_1_(c_net1), .switch_n9_Input_0_(c_net2), .switch_n9_Input_1_(c_net3), .switch_n10_Input_0_(c_net4), .switch_n10_Input_1_(c_net5), .switch_n11_Input_0_(c_net6), .switch_n11_Input_1_(c_net7), .switch_n12_Input_0_(c_net8), .switch_n12_Input_1_(c_net9), .switch_n13_Input_0_(c_net10), .switch_n13_Input_1_(c_net11), .switch_n14_Input_0_(c_net12), .switch_n14_Input_1_(c_net13), .switch_n15_Input_0_(c_net14), .switch_n15_Input_1_(c_net15), .switch_n16_Input_0_(c_net16), .switch_n16_Input_1_(c_net17));

endmodule

module Tile_v2(port1);
	/*Tile Verilog checkpoint*/
	/* C, S, C blocks of the tile */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(6));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(6), .matrix_row(5), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__2 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(6));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));

	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(22));

	/* CAB elements of tile*/
	TSMC350nm_4x2_Indirect I__2 (.island_num(1), .row(0), .col(0), .matrix_row(8), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(0), .col(8), .matrix_row(8), .matrix_col(9));
	TSMC350nm_4x2_Indirect I__4 (.island_num(1), .row(8), .col(8), .matrix_row(2), .matrix_col(9));
	TSMC350nm_4WTA cab_device_0 (.island_num(1), .row(2), .col(17), .Vout_0_(c_net0), .Vout_1_(c_net1), .Vout_2_(c_net2), .Vout_3_(c_net3));
	TSMC350nm_TA2Cell_NoFG cab_device_1 (.island_num(1), .row(3), .col(17), .OUTPUT1(c_net4), .OUTPUT2(c_net5));
	TSMC350nm_4WTA cab_device_2 (.island_num(1), .row(4), .col(17), .Vout_0_(c_net6), .Vout_1_(c_net7), .Vout_2_(c_net8), .Vout_3_(c_net9));
	TSMC350nm_TA2Cell_Weak cab_device_3 (.island_num(1), .row(5), .col(17), .OUTPUT1(c_net10), .OUTPUT2(c_net11));
	TSMC350nm_4WTA cab_device_4 (.island_num(1), .row(6), .col(17), .Vout_0_(c_net12), .Vout_1_(c_net13), .Vout_2_(c_net14), .Vout_3_(c_net15));
	TSMC350nm_TA2Cell_Weak cab_device_5 (.island_num(1), .row(7), .col(17), .OUTPUT1(c_net16), .OUTPUT2(c_net17));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(10), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(1), .direction(vertical), .num(10), .type(prog_switch));

	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(18), .switch_n8_Input_0_(c_net0), .switch_n8_Input_1_(c_net1), .switch_n9_Input_0_(c_net2), .switch_n9_Input_1_(c_net3), .switch_n10_Input_0_(c_net4), .switch_n10_Input_1_(c_net5), .switch_n11_Input_0_(c_net6), .switch_n11_Input_1_(c_net7), .switch_n12_Input_0_(c_net8), .switch_n12_Input_1_(c_net9), .switch_n13_Input_0_(c_net10), .switch_n13_Input_1_(c_net11), .switch_n14_Input_0_(c_net12), .switch_n14_Input_1_(c_net13), .switch_n15_Input_0_(c_net14), .switch_n15_Input_1_(c_net15), .switch_n16_Input_0_(c_net16), .switch_n16_Input_1_(c_net17));

endmodule

module Tile_v1(port1);
	/* Synthesizing a Tile */
	TSMC350nm_4x2_Indirect I__10 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(8));
	TSMC350nm_CAB_feedback_horz I__11 (.island_num(1), .row(3), .col(8), .matrix_row(1), .matrix_col(1));
	TSMC350nm_GorS_IndrctSwcs I__9 (.island_num(1), .row(5), .col(0), .matrix_row(1), .matrix_col(24));
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(6), .col(0), .matrix_row(8), .matrix_col(18));
	TSMC350nm_4WTA I__1 (.island_num(1), .row(6), .col(18));
	TSMC350nm_TA2Cell_NoFG I__2 (.island_num(1), .row(7), .col(19));
	TSMC350nm_4WTA I__3 (.island_num(1), .row(8), .col(18));
	TSMC350nm_TA2Cell_LongL I__8 (.island_num(1), .row(9), .col(19));
	TSMC350nm_4WTA I__5 (.island_num(1), .row(10), .col(18));
	TSMC350nm_TA2Cell_Weak I__4 (.island_num(1), .row(11), .col(19));
	TSMC350nm_4WTA I__7 (.island_num(1), .row(12), .col(18));
	TSMC350nm_TA2Cell_LongL I__6 (.island_num(1), .row(13), .col(19));
	TSMC350nm_CAB_feedback_vert I__12 (.island_num(1), .row(13), .col(20));
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(0), .col(21), .matrix_row(14), .matrix_col(10));

endmodule

module isle_v1(port1);
	/* AWG like island*/
    TSMC350nm_4x2_Direct I__0 (.island_num(0), .row(0), .col(0), .matrix_row(8), .matrix_col(8));
	ArbGen_I2V_Buffer_Tile_4x1 I__1 (.island_num(0), .row(0), .col(8), .matrix_row(8), .matrix_col(1));

	/* Do mux stuff */
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(8));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
    TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(8), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(8), .type(prog_switch));
	
	/* CAB like island */
	TSMC350nm_4x2_Direct I__0 (.island_num(1), .row(0), .col(0), .matrix_row(8), .matrix_col(14), .Vd_0_col_13(c_net7[0:8]), .Vs_0_row_0(c_net8[0:14]), .VTUNrow_0(c_net_vtun), .Vd_1_col_13(c_net9[0:2]), .Vd_1_col_13(c_net9[2:4]), .Vd_3_col_13(c_net10[1]));
	TSMC350nm_4WTA I__1 (.island_num(1), .row(0), .col(14), .Iin_0_(c_net7[0]), .Iin_1_(c_net9[0]));
	TSMC350nm_TA2Cell_NoFG I__2 (.island_num(1), .row(1), .col(15), .VTUN(c_net1), .GATE1(c_net2), .COLSEL1(c_net3), .VINJ(c_net4), .GND(c_net5), .VPWR(c_net6), .DRAIN2(c_net10[1]));
	TSMC350nm_4WTA I__3 (.island_num(1), .row(2), .col(14), .Iin_0_(c_net7[2]));
	TSMC350nm_TA2Cell_Strong I__2 (.island_num(1), .row(3), .col(15));
	TSMC350nm_4WTA I__5 (.island_num(1), .row(4), .col(14), .Iin_0_(c_net7[4]));
	TSMC350nm_TA2Cell_Weak I__4 (.island_num(1), .row(5), .col(15));
	TSMC350nm_4WTA I__7 (.island_num(1), .row(6), .col(14), .Iin_0_(c_net7[6]));
	TSMC350nm_TA2Cell_LongL I__6 (.island_num(1), .row(7), .col(15));

	/* Do mux stuff*/
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(5));
	TSMC350nm_GateMuxSwcTile switch(.island_num(1), .direction(horizontal), .num(16), .switch_n0_VVINJ_0_(c_net8[0]));
	/*TSMC350nm_IndirectSwc_VMMWTA switch_ind(.island_num(1), .direction(horizontal), .col(14));*/
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(15), .VTUN(c_net1), .Vg_0_(c_net2), .CTRL_B_0_(c_net3), .VINJ(c_net4), .GNDV_1_(c_net5), .VDD_1_(c_net6));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(5));
    TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(8), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(1), .direction(vertical), .num(8), .type(prog_switch));

	/* Test with & without mux synthesis. Test routing between islands. Test abutting stuff to an island*/
endmodule

module exp_TOP(port1);
	/* Testing 128 wide matrices*/
    TSMC350nm_4x2_Direct I__0 (.island_num(0), .row(0), .col(0), .matrix_row(32), .matrix_col(64));

	/* Do mux stuff */
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(7));
	TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(64));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(7));
    TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(32), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(32), .type(prog_switch));
endmodule

module asic_test_pranav(port1);
	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(8), .Vd_R_0_col_7(net232[0:4]),.Vd_R_1_col_7(net233[0:4]),.Vd_R_2_col_7(net234[0:4]),.Vd_R_3_col_7(net235[0:4]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(8));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(8));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(4), .decode_n0_VGRUN_0_(net232[0]), .decode_n0_VGRUN_1_(net233[0]), .decode_n0_VGRUN_2_(net234[0]), .decode_n0_VGRUN_3_(net235[0]), .decode_n1_VGRUN_0_(net232[1]), .decode_n1_VGRUN_1_(net233[1]), .decode_n1_VGRUN_2_(net234[1]), .decode_n1_VGRUN_3_(net235[1]), .decode_n2_VGRUN_0_(net232[2]), .decode_n2_VGRUN_1_(net233[2]), .decode_n2_VGRUN_2_(net234[2]), .decode_n2_VGRUN_3_(net235[2]), .decode_n3_VGRUN_0_(net232[3]), .decode_n3_VGRUN_1_(net233[3]), .decode_n3_VGRUN_2_(net234[3]), .decode_n3_VGRUN_3_(net235[3]));
	TSMC350nm_GateMuxSwcTile switch(.island_num(1), .direction(horizontal), .num(8));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(1), .direction(vertical), .num(4), .type(prog_switch));
endmodule